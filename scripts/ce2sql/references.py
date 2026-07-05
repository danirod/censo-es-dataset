# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

import csv
from collections.abc import Iterable, Sequence
from pathlib import Path

from .database import Database
from .errors import BuildSqliteError
from .records import ComunidadAutonomaRecord, MunicipioRecord, ProvinciaRecord, TipoViaSinonimoRecord


def load_references(database: Database, folder: Path) -> None:
    load_comunidades_autonomas(database, folder / "cod_ccaa.csv")
    load_provincias(database, folder / "cod_provincia.csv")
    load_municipios(database, folder / "cod_mun.csv")
    load_tipos_via(database, folder / "TiposVia.csv")


def load_comunidades_autonomas(database: Database, path: Path) -> None:
    database.insert_many(
        "insert/comunidad_autonoma.sql",
        (
            ComunidadAutonomaRecord(codigo_autonomia=row["CODIGO"], nombre=row["LITERAL"])
            for row in read_reference_csv(path, ("CODIGO", "LITERAL"))
        ),
    )


def load_provincias(database: Database, path: Path) -> None:
    database.insert_many(
        "insert/provincia.sql",
        (
            ProvinciaRecord(codigo_provincia=row["CODIGO"], nombre=row["LITERAL"])
            for row in read_reference_csv(path, ("CODIGO", "LITERAL"))
        ),
    )


def load_municipios(database: Database, path: Path) -> None:
    database.insert_many(
        "insert/municipio.sql",
        (
            MunicipioRecord(
                codigo_autonomia=row["CODAUTO"],
                codigo_provincia=row["CPRO"],
                codigo_municipio=row["CMUN"],
                digito_control=row["DC"],
                nombre=row["NOMBRE"],
            )
            for row in read_reference_csv(path, ("CODAUTO", "CPRO", "CMUN", "DC", "NOMBRE"))
        ),
    )


def load_tipos_via(database: Database, path: Path) -> None:
    database.insert_many(
        "insert/tipo_via_sinonimo.sql",
        (
            TipoViaSinonimoRecord(
                tipo_via=row["TIPO_VIA"],
                sinonimo=row["SINONIMO"],
                descripcion=row["DESCRIPCION"],
                comentario=row["COMENTARIO"],
            )
            for row in read_reference_csv(path, ("TIPO_VIA", "SINONIMO", "DESCRIPCION", "COMENTARIO"))
        ),
    )


def read_reference_csv(path: Path, expected_header: Sequence[str]) -> Iterable[dict[str, str]]:
    if not path.is_file():
        raise BuildSqliteError(f"missing reference file: {path}")
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter=";")
        if reader.fieldnames != list(expected_header):
            raise BuildSqliteError(f"unexpected header in {path}: {reader.fieldnames!r}")
        yield from reader
