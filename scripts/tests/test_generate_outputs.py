# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

import csv
import sqlite3
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
            self.assertEqual(
                self.rows(output / "localidades.csv"),
                [
                    {
                        "PROV": "Madrid",
                        "MUNI": "Madrid",
                        "COD_PROV": "28",
                        "COD_MUNI": "079",
                        "DC": "6",
                        "COD_MUNI_COMPLETO": "280796",
                        "CUN": "0000000",
                        "ENTIDAD_COLECTIVA": "",
                        "ENTIDAD_SINGULAR": "",
                        "NUCLEO": "",
                        "TIPO": "NUCLEO",
                        "LOCALIDAD": "Madrid",
                        "COD_POSTAL": "28001",
                    }
                ],
            )

    def test_localidades_preserves_canonical_names_and_excludes_units_without_postal_segments(self) -> None:
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            references = base / "references"
            snapshot = base / "snapshot"
            database = base / "dataset.sqlite"
            output = base / "output"
            write_references(references)
            write_snapshot(snapshot)
            build_sqlite(snapshot, database, references=references)

            with sqlite3.connect(database) as connection:
                def insert_unit(cun: str, singular: str, nucleo: str) -> None:
                    connection.execute(
                        "INSERT INTO unidad_poblacional VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        ("28", "079", cun, *([""] * 9), singular, singular, "", nucleo, nucleo, ""),
                    )

                insert_unit("0000101", "ENTIDAD SINGULAR", "NÚCLEO LARGO")
                insert_unit("0000199", "SINGULAR DEL DISEMINADO", "*DISEMINADO*")
                insert_unit("0000102", "SIN TRAMOS", "NÚCLEO SIN TRAMOS")

                def insert_segment(segment: tuple[str, str, str, str, str, str]) -> None:
                    cun, singular, nucleo, via, postal, number = segment
                    connection.execute(
                        "INSERT INTO tramo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            "28",
                            "079",
                            "01",
                            "001",
                            "",
                            "",
                            cun,
                            "",
                            singular,
                            nucleo,
                            via,
                            "CALLE",
                            "00000",
                            "",
                            "0000",
                            postal,
                            "1",
                            number,
                            "",
                            number,
                            "",
                            "",
                            "",
                            "",
                        ),
                    )

                insert_segment(("0000101", "ENTIDAD SINGULAR", "NÚCLEO LARGO", "00001", "28002", "0001"))
                insert_segment(("0000199", "SINGULAR DEL DISEMINADO", "*DISEMINADO*", "00001", "28003", "0001"))
                insert_segment(("0000101", "ENTIDAD SINGULAR", "NÚCLEO LARGO", "00002", "28002", "0002"))
                connection.commit()

            generate_outputs(database, output)

            rows = self.rows(output / "localidades.csv")
            self.assertEqual([row["CUN"] for row in rows], ["0000000", "0000101", "0000199"])
            self.assertEqual(rows[1]["LOCALIDAD"], "NÚCLEO LARGO")
            self.assertEqual(rows[1]["TIPO"], "NUCLEO")
            self.assertEqual(rows[2]["NUCLEO"], "*DISEMINADO*")
            self.assertEqual(rows[2]["LOCALIDAD"], "Diseminado de SINGULAR DEL DISEMINADO")
            self.assertNotIn("0000102", {row["CUN"] for row in rows})

    def rows(self, path: Path) -> list[dict[str, str]]:
        with path.open(encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream))


if __name__ == "__main__":
    unittest.main()
