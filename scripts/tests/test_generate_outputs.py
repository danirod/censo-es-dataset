# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

import csv
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.ce2sql import build_sqlite
from scripts.generate_outputs import generate_outputs
from scripts.tests.fixtures import write_references, write_snapshot


class GenerateOutputsTest(unittest.TestCase):
    def test_generates_public_csv_outputs(self) -> None:
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            references = base / "references"
            snapshot = base / "snapshot"
            database = base / "dataset.sqlite"
            output = base / "output"
            write_references(references)
            write_snapshot(snapshot)
            build_sqlite(snapshot, database, references=references)

            generate_outputs(database, output)

            self.assertEqual(
                self.rows(output / "municipios.csv"),
                [
                    {
                        "PROV": "Madrid",
                        "MUNI": "Madrid",
                        "COD_PROV": "28",
                        "COD_MUNI": "079",
                        "DC": "6",
                        "COD_MUNI_COMPLETO": "280796",
                    }
                ],
            )
            self.assertEqual(
                self.rows(output / "codigos_postales.csv"),
                [
                    {
                        "PROV": "Madrid",
                        "MUNI": "Madrid",
                        "COD_PROV": "28",
                        "COD_MUNI": "079",
                        "DC": "6",
                        "COD_MUNI_COMPLETO": "280796",
                        "COD_POSTAL": "28001",
                    }
                ],
            )

    def rows(self, path: Path) -> list[dict[str, str]]:
        with path.open(encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream))


if __name__ == "__main__":
    unittest.main()
