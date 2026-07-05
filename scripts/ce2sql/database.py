# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

import sqlite3
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path

from .errors import BuildSqliteError

SQL_FOLDER = Path(__file__).with_name("sql")


class Database:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    @classmethod
    @contextmanager
    def connect(cls, path: Path) -> Iterator[Database]:
        connection = sqlite3.connect(path)
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            yield cls(connection)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def run_script(self, name: str) -> None:
        self.connection.executescript(read_sql(name))

    def insert_many(self, statement: str, records: Iterable[object]) -> None:
        self.connection.executemany(read_sql(statement), (vars(record) for record in records))

    def scalar(self, statement: str) -> int:
        row = self.connection.execute(read_sql(statement)).fetchone()
        if row is None:
            raise BuildSqliteError(f"query returned no rows: {statement}")
        return int(row[0])

    def foreign_key_errors(self) -> list[tuple[object, ...]]:
        return self.connection.execute("PRAGMA foreign_key_check").fetchall()


def read_sql(name: str) -> str:
    return (SQL_FOLDER / name).read_text(encoding="utf-8")
