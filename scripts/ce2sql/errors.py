# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez


class BuildSqliteError(Exception):
    """Raised when a caj_esp snapshot cannot be converted to SQLite."""
