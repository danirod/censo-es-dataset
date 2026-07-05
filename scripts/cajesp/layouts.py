# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

FieldKind = Literal["A", "N"]


@dataclass(frozen=True)
class Field:
    name: str
    start: int
    end: int
    kind: FieldKind


@dataclass(frozen=True)
class Layout:
    prefix: str
    width: int
    fields: tuple[Field, ...]


VIAS = Layout(
    prefix="VIAS",
    width=132,
    fields=(
        Field("cpro", 0, 2, "N"),
        Field("cmun", 2, 5, "N"),
        Field("cvia_previous", 5, 10, "N"),
        Field("nviac_previous", 10, 35, "A"),
        Field("tipoinf", 35, 36, "A"),
        Field("cdev", 36, 38, "A"),
        Field("fvar", 38, 46, "N"),
        Field("cvar", 46, 47, "A"),
        Field("cvia", 47, 52, "N"),
        Field("tvia", 52, 57, "A"),
        Field("nvia", 57, 107, "A"),
        Field("nviac", 107, 132, "A"),
    ),
)

PSEU = Layout(
    prefix="PSEU",
    width=127,
    fields=(
        Field("cpro", 0, 2, "N"),
        Field("cmun", 2, 5, "N"),
        Field("cpsvia_previous", 5, 10, "N"),
        Field("npsvia_previous", 10, 60, "A"),
        Field("tipoinf", 60, 61, "A"),
        Field("cdev", 61, 63, "A"),
        Field("fvar", 63, 71, "N"),
        Field("cvar", 71, 72, "A"),
        Field("cpsvia", 72, 77, "N"),
        Field("dpsvia", 77, 127, "A"),
    ),
)

UP = Layout(
    prefix="UP",
    width=604,
    fields=(
        Field("cpro", 0, 2, "N"),
        Field("cmun", 2, 5, "N"),
        Field("cun", 5, 12, "N"),
        Field("tipoinf", 12, 13, "A"),
        Field("cdev", 13, 15, "A"),
        Field("fvar", 15, 23, "N"),
        Field("cvar", 23, 24, "A"),
        Field("nmun", 24, 94, "A"),
        Field("nmun50", 94, 144, "A"),
        Field("nmunc", 144, 169, "A"),
        Field("nentco", 169, 239, "A"),
        Field("nentco50", 239, 289, "A"),
        Field("nentcoc", 289, 314, "A"),
        Field("nentsi", 314, 384, "A"),
        Field("nentsi50", 384, 434, "A"),
        Field("nentsic", 434, 459, "A"),
        Field("nnucle", 459, 529, "A"),
        Field("nnucle50", 529, 579, "A"),
        Field("nnuclec", 579, 604, "A"),
    ),
)

SECC = Layout(
    prefix="SECC",
    width=11,
    fields=(
        Field("cpro", 0, 2, "N"),
        Field("cmun", 2, 5, "N"),
        Field("dist", 5, 7, "N"),
        Field("secc", 7, 10, "N"),
        Field("lsecc", 10, 11, "A"),
    ),
)

TRAM = Layout(
    prefix="TRAM",
    width=273,
    fields=(
        Field("cpro", 0, 2, "N"),
        Field("cmun", 2, 5, "N"),
        Field("dist_previous", 5, 7, "N"),
        Field("secc_previous", 7, 10, "N"),
        Field("lsecc_previous", 10, 11, "A"),
        Field("subsc_previous", 11, 13, "A"),
        Field("cun_previous", 13, 20, "N"),
        Field("cvia_previous", 20, 25, "N"),
        Field("cpsvia_previous", 25, 30, "N"),
        Field("manz_previous", 30, 42, "A"),
        Field("cpos_previous", 42, 47, "N"),
        Field("tinum_previous", 47, 48, "N"),
        Field("ein_previous", 48, 52, "N"),
        Field("cein_previous", 52, 53, "A"),
        Field("esn_previous", 53, 57, "N"),
        Field("cesn_previous", 57, 58, "A"),
        Field("tipoinf", 58, 59, "A"),
        Field("cdev", 59, 61, "A"),
        Field("fvar", 61, 69, "N"),
        Field("cvar", 69, 70, "A"),
        Field("dist", 70, 72, "N"),
        Field("secc", 72, 75, "N"),
        Field("lsecc", 75, 76, "A"),
        Field("subsc", 76, 78, "A"),
        Field("cun", 78, 85, "N"),
        Field("nentcoc", 85, 110, "A"),
        Field("nentsic", 110, 135, "A"),
        Field("nnuclec", 135, 160, "A"),
        Field("cvia", 160, 165, "N"),
        Field("nviac", 165, 190, "A"),
        Field("cpsvia", 190, 195, "N"),
        Field("dpsvia", 195, 245, "A"),
        Field("manz", 245, 257, "A"),
        Field("cpos", 257, 262, "N"),
        Field("tinum", 262, 263, "N"),
        Field("ein", 263, 267, "N"),
        Field("cein", 267, 268, "A"),
        Field("esn", 268, 272, "N"),
        Field("cesn", 272, 273, "A"),
    ),
)

ALL_LAYOUTS = (VIAS, PSEU, UP, SECC, TRAM)
