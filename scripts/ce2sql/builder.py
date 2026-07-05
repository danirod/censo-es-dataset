# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager, nullcontext
from pathlib import Path

from scripts.cajesp import Cajesp

from .database import Database
from .errors import BuildSqliteError
from .references import load_references
from .snapshot import load_snapshot
from .validate import validate_database


def build_sqlite(input_path: Path, output_path: Path, *, references: Path = Path("upstream")) -> None:
    input_path = Path(input_path)
    output_path = Path(output_path)
    references = Path(references)

    ensure_output_does_not_exist(output_path)

    with temporary_database(output_path) as temporary_path:
        with open_snapshot(input_path) as snapshot:
            create_database(snapshot, temporary_path, references)
        publish_database(temporary_path, output_path)


def ensure_output_does_not_exist(output_path: Path) -> None:
    if output_path.exists():
        raise BuildSqliteError(f"output file already exists: {output_path}")


@contextmanager
def temporary_database(output_path: Path) -> Iterator[Path]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_name(f".{output_path.name}.tmp")
    if temporary_path.exists():
        temporary_path.unlink()
    try:
        yield temporary_path
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def create_database(snapshot: Cajesp, output_path: Path, references: Path) -> None:
    with Database.connect(output_path) as database:
        database.run_script("schema.sql")
        load_references(database, references)
        load_snapshot(database, snapshot)
        database.run_script("indexes.sql")
        validate_database(database)


def open_snapshot(input_path: Path) -> AbstractContextManager[Cajesp]:
    if input_path.is_dir():
        return nullcontext(Cajesp.from_folder(input_path))
    if input_path.is_file():
        return Cajesp.from_zip(input_path)
    raise BuildSqliteError(f"input snapshot does not exist: {input_path}")


def publish_database(temporary_path: Path, output_path: Path) -> None:
    os.replace(temporary_path, output_path)
