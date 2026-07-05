# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.ce2sql import BuildSqliteError, build_sqlite


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a SQLite database from a caj_esp snapshot")
    parser.add_argument("input", type=Path, help="caj_esp snapshot folder or zip file")
    parser.add_argument("output", type=Path, help="SQLite database to create")
    parser.add_argument(
        "--references", type=Path, default=Path("upstream"), help="directory with INE reference CSV files"
    )
    args = parser.parse_args(argv)

    build_sqlite(args.input, args.output, references=args.references)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildSqliteError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error
