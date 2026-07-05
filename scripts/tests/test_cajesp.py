# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.cajesp import Cajesp, CajespParseError
from scripts.tests.fixtures import write_snapshot, write_snapshot_zip


class CajespTest(unittest.TestCase):
    def test_reads_rows_from_folder(self) -> None:
        with TemporaryDirectory() as tmp:
            folder = Path(tmp)
            write_snapshot(folder)

            snapshot = Cajesp.from_folder(folder)
            secc = list(snapshot.secc())
            vias = list(snapshot.vias())

            self.assertEqual(len(secc), 1)
            self.assertEqual(secc[0].cpro, "28")
            self.assertEqual(secc[0].cmun, "079")
            self.assertEqual(secc[0].dist, "01")
            self.assertEqual(secc[0].secc, "001")
            self.assertEqual(secc[0].lsecc, "")
            self.assertEqual(vias[0].nvia, "CALLE MAYOR")

    def test_reads_rows_from_nested_zip_and_cleans_temporary_folder(self) -> None:
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "caj_esp_test"
            write_snapshot(source)
            zip_file = write_snapshot_zip(base, source)

            with Cajesp.from_zip(zip_file) as snapshot:
                extracted_folder = snapshot.folder
                self.assertTrue(extracted_folder.exists())
                self.assertEqual(len(list(snapshot.secc())), 1)

            self.assertFalse(extracted_folder.exists())
            self.assertFalse(extracted_folder.parent.exists())

    def test_rejects_wrong_width(self) -> None:
        with TemporaryDirectory() as tmp:
            folder = Path(tmp)
            write_snapshot(folder)
            (folder / "SECC.D260101.G260101").write_bytes(b"280790100\r\n")

            with self.assertRaisesRegex(CajespParseError, "expected width 11, got 9"):
                list(Cajesp.from_folder(folder).secc())

    def test_rejects_non_numeric_fields(self) -> None:
        with TemporaryDirectory() as tmp:
            folder = Path(tmp)
            write_snapshot(folder)
            (folder / "SECC.D260101.G260101").write_bytes(b"2A07901001 \r\n")

            with self.assertRaisesRegex(CajespParseError, "field cpro expected 2 digits"):
                list(Cajesp.from_folder(folder).secc())

    def test_rejects_invalid_fvar(self) -> None:
        with TemporaryDirectory() as tmp:
            folder = Path(tmp)
            write_snapshot(folder, fvar="20260230")

            with self.assertRaisesRegex(CajespParseError, "field fvar expected YYYYMMDD"):
                list(Cajesp.from_folder(folder).vias())


if __name__ == "__main__":
    unittest.main()
