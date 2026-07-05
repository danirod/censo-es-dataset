# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

from .database import Database
from .errors import BuildSqliteError


def validate_database(database: Database) -> None:
    validate_foreign_keys(database)
    validate_tramo_vias(database)
    validate_tramo_pseudovias(database)


def validate_foreign_keys(database: Database) -> None:
    foreign_key_errors = database.foreign_key_errors()
    if foreign_key_errors:
        raise BuildSqliteError(f"foreign key validation failed: {foreign_key_errors[:5]!r}")


def validate_tramo_vias(database: Database) -> None:
    missing_vias = database.scalar("validate/missing_vias.sql")
    if missing_vias:
        raise BuildSqliteError(f"tramo references {missing_vias} missing via rows")


def validate_tramo_pseudovias(database: Database) -> None:
    missing_pseudovias = database.scalar("validate/missing_pseudovias.sql")
    if missing_pseudovias:
        raise BuildSqliteError(f"tramo references {missing_pseudovias} missing pseudovia rows")
