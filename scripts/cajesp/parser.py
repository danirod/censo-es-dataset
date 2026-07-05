# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import ClassVar, TypeVar
from zipfile import ZipFile

from . import layouts
from .layouts import ALL_LAYOUTS, Layout
from .rows import CensusSectionRow, PopulationUnitRow, PseudoRoadRow, SegmentRow, ViaRow

RowT = TypeVar("RowT")


class CajespParseError(Exception):
    """Raised when a snapshot file cannot be parsed as caj_esp data."""


class Cajesp:
    """Read rows from an INE caj_esp snapshot directory or zip file."""

    ENCODING: ClassVar[str] = "iso-8859-1"

    def __init__(self, folder: str | Path):
        self.folder = Path(folder)

    @classmethod
    def from_folder(cls, folder: str | Path) -> Cajesp:
        return cls(folder)

    @classmethod
    def from_zip(cls, zip_file: str | Path) -> AbstractContextManager[Cajesp]:
        return _cajesp_from_zip(cls, zip_file)

    def vias(self) -> Iterator[ViaRow]:
        return self._read_rows(layouts.VIAS, ViaRow)

    def pseu(self) -> Iterator[PseudoRoadRow]:
        return self._read_rows(layouts.PSEU, PseudoRoadRow)

    def up(self) -> Iterator[PopulationUnitRow]:
        return self._read_rows(layouts.UP, PopulationUnitRow)

    def secc(self) -> Iterator[CensusSectionRow]:
        return self._read_rows(layouts.SECC, CensusSectionRow)

    def tram(self) -> Iterator[SegmentRow]:
        return self._read_rows(layouts.TRAM, SegmentRow)

    def _read_rows(self, layout: Layout, row_type: type[RowT]) -> Iterator[RowT]:
        path = self._file_for_layout(layout)
        with path.open("rb") as stream:
            for line_number, raw_line in enumerate(stream, start=1):
                line = self._decode_line(path, line_number, raw_line)
                yield self._parse_line(path, line_number, line, layout, row_type)

    def _file_for_layout(self, layout: Layout) -> Path:
        if not self.folder.is_dir():
            raise CajespParseError(f"{self.folder}: snapshot folder does not exist")
        matches = sorted(
            path for path in self.folder.iterdir() if path.is_file() and path.name.startswith(f"{layout.prefix}.")
        )
        if len(matches) == 1:
            return matches[0]
        if not matches:
            raise CajespParseError(f"{self.folder}: missing {layout.prefix} file")
        choices = ", ".join(path.name for path in matches)
        raise CajespParseError(f"{self.folder}: multiple {layout.prefix} files found: {choices}")

    def _decode_line(self, path: Path, line_number: int, raw_line: bytes) -> str:
        if raw_line.endswith(b"\r\n"):
            raw_line = raw_line[:-2]
        elif raw_line.endswith(b"\n"):
            raw_line = raw_line[:-1]
        try:
            return raw_line.decode(self.ENCODING)
        except UnicodeDecodeError as error:
            raise CajespParseError(f"{path.name}:{line_number}: cannot decode as {self.ENCODING}") from error

    def _parse_line(self, path: Path, line_number: int, line: str, layout: Layout, row_type: type[RowT]) -> RowT:
        if len(line) != layout.width:
            raise CajespParseError(f"{path.name}:{line_number}: expected width {layout.width}, got {len(line)}")
        values: dict[str, str] = {}
        for field in layout.fields:
            value = line[field.start : field.end]
            if field.kind == "N" and not value.isdigit():
                raise CajespParseError(
                    f"{path.name}:{line_number}: field {field.name} expected {field.end - field.start} digits, "
                    f"got {value!r}"
                )
            if field.name == "fvar":
                self._validate_fvar(path, line_number, value)
            values[field.name] = value.rstrip() if field.kind == "A" else value
        return row_type(**values)

    def _validate_fvar(self, path: Path, line_number: int, value: str) -> None:
        try:
            datetime.strptime(value, "%Y%m%d")
        except ValueError as error:
            raise CajespParseError(f"{path.name}:{line_number}: field fvar expected YYYYMMDD, got {value!r}") from error


@contextmanager
def _cajesp_from_zip(reader_type: type[Cajesp], zip_file: str | Path) -> Iterator[Cajesp]:
    with TemporaryDirectory() as temporary_folder:
        folder = Path(temporary_folder)
        with ZipFile(zip_file) as zip_stream:
            zip_stream.extractall(folder)
        yield reader_type.from_folder(_snapshot_folder_in(folder))


def _snapshot_folder_in(folder: Path) -> Path:
    if _looks_like_snapshot_folder(folder):
        return folder
    candidates = [path for path in folder.iterdir() if path.is_dir() and _looks_like_snapshot_folder(path)]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise CajespParseError(f"{folder}: zip does not contain a caj_esp snapshot folder")
    choices = ", ".join(path.name for path in candidates)
    raise CajespParseError(f"{folder}: zip contains multiple caj_esp snapshot folders: {choices}")


def _looks_like_snapshot_folder(folder: Path) -> bool:
    names = [path.name for path in folder.iterdir() if path.is_file()]
    return all(any(name.startswith(f"{layout.prefix}.") for name in names) for layout in ALL_LAYOUTS)
