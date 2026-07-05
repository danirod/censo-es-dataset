# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.cajesp import CajespParseError
from scripts.ce2sql import BuildSqliteError, build_sqlite
from scripts.tests.fixtures import write_references, write_snapshot, write_snapshot_zip


class BuildSqliteTest(unittest.TestCase):
    def test_builds_sqlite_database_from_folder(self) -> None:
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            references = base / "references"
            snapshot = base / "snapshot"
            output = base / "snapshot.sqlite"
            write_references(references)
            write_snapshot(snapshot)

            build_sqlite(snapshot, output, references=references)

            self.assertTrue(output.is_file())
            with sqlite3.connect(output) as connection:
                self.assertEqual(self.scalar(connection, "SELECT COUNT(*) FROM comunidad_autonoma"), 1)
                self.assertEqual(self.scalar(connection, "SELECT COUNT(*) FROM municipio"), 1)
                self.assertEqual(self.scalar(connection, "SELECT COUNT(*) FROM tramo"), 1)
                self.assertEqual(self.scalar(connection, "SELECT nombre FROM via"), "CALLE MAYOR")
                self.assertEqual(self.scalar(connection, "SELECT codigo_postal FROM tramo"), "28001")

    def test_builds_sqlite_database_from_zip(self) -> None:
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            references = base / "references"
            snapshot = base / "snapshot"
            output = base / "snapshot.sqlite"
            write_references(references)
            write_snapshot(snapshot)
            zip_file = write_snapshot_zip(base, snapshot)

            build_sqlite(zip_file, output, references=references)

            self.assertTrue(output.is_file())
            with sqlite3.connect(output) as connection:
                self.assertEqual(self.scalar(connection, "SELECT COUNT(*) FROM seccion_censal"), 1)

    def test_fails_if_output_exists(self) -> None:
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            references = base / "references"
            snapshot = base / "snapshot"
            output = base / "snapshot.sqlite"
            write_references(references)
            write_snapshot(snapshot)
            output.write_text("keep me", encoding="utf-8")

            with self.assertRaisesRegex(BuildSqliteError, "output file already exists"):
                build_sqlite(snapshot, output, references=references)

            self.assertEqual(output.read_text(encoding="utf-8"), "keep me")

    def test_does_not_leave_output_if_build_fails(self) -> None:
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            references = base / "references"
            snapshot = base / "snapshot"
            output = base / "snapshot.sqlite"
            write_references(references)
            write_snapshot(snapshot, fvar="20260230")

            with self.assertRaises(CajespParseError):
                build_sqlite(snapshot, output, references=references)

            self.assertFalse(output.exists())
            self.assertFalse((base / ".snapshot.sqlite.tmp").exists())

    def scalar(self, connection: sqlite3.Connection, query: str) -> object:
        row = connection.execute(query).fetchone()
        self.assertIsNotNone(row)
        return row[0]


if __name__ == "__main__":
    unittest.main()
