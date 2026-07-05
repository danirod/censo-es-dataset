# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

import argparse
import csv
import sqlite3
from collections.abc import Sequence
from pathlib import Path

MUNICIPIOS_QUERY = """
SELECT
    provincia.nombre AS PROV,
    municipio.nombre AS MUNI,
    municipio.codigo_provincia AS COD_PROV,
    municipio.codigo_municipio AS COD_MUNI,
    municipio.digito_control AS DC,
    municipio.codigo_provincia || municipio.codigo_municipio || municipio.digito_control AS COD_MUNI_COMPLETO
FROM municipio
JOIN provincia USING (codigo_provincia)
ORDER BY COD_PROV, COD_MUNI
"""

CODIGOS_POSTALES_QUERY = """
SELECT DISTINCT
    provincia.nombre AS PROV,
    municipio.nombre AS MUNI,
    municipio.codigo_provincia AS COD_PROV,
    municipio.codigo_municipio AS COD_MUNI,
    municipio.digito_control AS DC,
    municipio.codigo_provincia || municipio.codigo_municipio || municipio.digito_control AS COD_MUNI_COMPLETO,
    tramo.codigo_postal AS COD_POSTAL
FROM tramo
JOIN municipio USING (codigo_provincia, codigo_municipio)
JOIN provincia USING (codigo_provincia)
ORDER BY COD_PROV, COD_MUNI, COD_POSTAL
"""


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate committed CSV datasets from a caj_esp SQLite database")
    parser.add_argument("database", type=Path, help="SQLite database created by scripts/build_sqlite.py")
    parser.add_argument(
        "output", type=Path, nargs="?", default=Path("output"), help="directory for generated CSV files"
    )
    args = parser.parse_args(argv)

    generate_outputs(args.database, args.output)
    return 0


def generate_outputs(database: Path, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        write_query(connection, output / "municipios.csv", MUNICIPIOS_QUERY)
        write_query(connection, output / "codigos_postales.csv", CODIGOS_POSTALES_QUERY)


def write_query(connection: sqlite3.Connection, path: Path, query: str) -> None:
    cursor = connection.execute(query)
    columns = [description[0] for description in cursor.description]
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        writer.writerows(cursor)


if __name__ == "__main__":
    raise SystemExit(main())
