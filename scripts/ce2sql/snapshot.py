# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

from scripts.cajesp import Cajesp

from .database import Database
from .records import PseudoviaRecord, SeccionCensalRecord, TramoRecord, UnidadPoblacionalRecord, ViaRecord


def load_snapshot(database: Database, snapshot: Cajesp) -> None:
    load_unidades_poblacionales(database, snapshot)
    load_secciones_censales(database, snapshot)
    load_vias(database, snapshot)
    load_pseudovias(database, snapshot)
    load_tramos(database, snapshot)


def load_unidades_poblacionales(database: Database, snapshot: Cajesp) -> None:
    database.insert_many(
        "insert/unidad_poblacional.sql",
        (UnidadPoblacionalRecord.from_row(row) for row in snapshot.up()),
    )


def load_secciones_censales(database: Database, snapshot: Cajesp) -> None:
    database.insert_many(
        "insert/seccion_censal.sql",
        (SeccionCensalRecord.from_row(row) for row in snapshot.secc()),
    )


def load_vias(database: Database, snapshot: Cajesp) -> None:
    database.insert_many("insert/via.sql", (ViaRecord.from_row(row) for row in snapshot.vias()))


def load_pseudovias(database: Database, snapshot: Cajesp) -> None:
    database.insert_many("insert/pseudovia.sql", (PseudoviaRecord.from_row(row) for row in snapshot.pseu()))


def load_tramos(database: Database, snapshot: Cajesp) -> None:
    database.insert_many("insert/tramo.sql", (TramoRecord.from_row(row) for row in snapshot.tram()))
