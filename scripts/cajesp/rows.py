# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViaRow:
    cpro: str
    cmun: str
    cvia_previous: str
    nviac_previous: str
    tipoinf: str
    cdev: str
    fvar: str
    cvar: str
    cvia: str
    tvia: str
    nvia: str
    nviac: str


@dataclass(frozen=True)
class PseudoRoadRow:
    cpro: str
    cmun: str
    cpsvia_previous: str
    npsvia_previous: str
    tipoinf: str
    cdev: str
    fvar: str
    cvar: str
    cpsvia: str
    dpsvia: str


@dataclass(frozen=True)
class PopulationUnitRow:
    cpro: str
    cmun: str
    cun: str
    tipoinf: str
    cdev: str
    fvar: str
    cvar: str
    nmun: str
    nmun50: str
    nmunc: str
    nentco: str
    nentco50: str
    nentcoc: str
    nentsi: str
    nentsi50: str
    nentsic: str
    nnucle: str
    nnucle50: str
    nnuclec: str


@dataclass(frozen=True)
class CensusSectionRow:
    cpro: str
    cmun: str
    dist: str
    secc: str
    lsecc: str


@dataclass(frozen=True)
class SegmentRow:
    cpro: str
    cmun: str
    dist_previous: str
    secc_previous: str
    lsecc_previous: str
    subsc_previous: str
    cun_previous: str
    cvia_previous: str
    cpsvia_previous: str
    manz_previous: str
    cpos_previous: str
    tinum_previous: str
    ein_previous: str
    cein_previous: str
    esn_previous: str
    cesn_previous: str
    tipoinf: str
    cdev: str
    fvar: str
    cvar: str
    dist: str
    secc: str
    lsecc: str
    subsc: str
    cun: str
    nentcoc: str
    nentsic: str
    nnuclec: str
    cvia: str
    nviac: str
    cpsvia: str
    dpsvia: str
    manz: str
    cpos: str
    tinum: str
    ein: str
    cein: str
    esn: str
    cesn: str
