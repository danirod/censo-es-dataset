# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from scripts.cajesp.rows import CensusSectionRow, PopulationUnitRow, PseudoRoadRow, SegmentRow, ViaRow

from .errors import BuildSqliteError


@dataclass(frozen=True)
class ComunidadAutonomaRecord:
    codigo_autonomia: str
    nombre: str


@dataclass(frozen=True)
class ProvinciaRecord:
    codigo_provincia: str
    nombre: str


@dataclass(frozen=True)
class MunicipioRecord:
    codigo_autonomia: str
    codigo_provincia: str
    codigo_municipio: str
    digito_control: str
    nombre: str


@dataclass(frozen=True)
class TipoViaSinonimoRecord:
    tipo_via: str
    sinonimo: str
    descripcion: str
    comentario: str


@dataclass(frozen=True)
class UnidadPoblacionalRecord:
    codigo_provincia: str
    codigo_municipio: str
    codigo_unidad_poblacional: str
    tipo_informacion: str
    causa_devolucion: str
    causa_variacion: str
    nombre_municipio_largo: str
    nombre_municipio: str
    nombre_municipio_corto: str
    nombre_entidad_colectiva_largo: str
    nombre_entidad_colectiva: str
    nombre_entidad_colectiva_corto: str
    nombre_entidad_singular_largo: str
    nombre_entidad_singular: str
    nombre_entidad_singular_corto: str
    nombre_nucleo_largo: str
    nombre_nucleo: str
    nombre_nucleo_corto: str

    @classmethod
    def from_row(cls, row: PopulationUnitRow) -> Self:
        return cls(
            codigo_provincia=row.cpro,
            codigo_municipio=row.cmun,
            codigo_unidad_poblacional=row.cun,
            tipo_informacion=row.tipoinf,
            causa_devolucion=row.cdev,
            causa_variacion=row.cvar,
            nombre_municipio_largo=row.nmun,
            nombre_municipio=row.nmun50,
            nombre_municipio_corto=row.nmunc,
            nombre_entidad_colectiva_largo=row.nentco,
            nombre_entidad_colectiva=row.nentco50,
            nombre_entidad_colectiva_corto=row.nentcoc,
            nombre_entidad_singular_largo=row.nentsi,
            nombre_entidad_singular=row.nentsi50,
            nombre_entidad_singular_corto=row.nentsic,
            nombre_nucleo_largo=row.nnucle,
            nombre_nucleo=row.nnucle50,
            nombre_nucleo_corto=row.nnuclec,
        )


@dataclass(frozen=True)
class SeccionCensalRecord:
    codigo_provincia: str
    codigo_municipio: str
    distrito: str
    seccion: str
    letra_seccion: str

    @classmethod
    def from_row(cls, row: CensusSectionRow) -> Self:
        return cls(
            codigo_provincia=row.cpro,
            codigo_municipio=row.cmun,
            distrito=row.dist,
            seccion=row.secc,
            letra_seccion=row.lsecc,
        )


@dataclass(frozen=True)
class ViaRecord:
    codigo_provincia: str
    codigo_municipio: str
    codigo_via: str
    tipo_informacion: str
    causa_devolucion: str
    causa_variacion: str
    tipo_via: str
    nombre: str
    nombre_corto: str

    @classmethod
    def from_row(cls, row: ViaRow) -> Self:
        require_same("VIAS", "cvia", row.cvia_previous, row.cvia)
        require_same("VIAS", "nviac", row.nviac_previous, row.nviac)
        return cls(
            codigo_provincia=row.cpro,
            codigo_municipio=row.cmun,
            codigo_via=row.cvia,
            tipo_informacion=row.tipoinf,
            causa_devolucion=row.cdev,
            causa_variacion=row.cvar,
            tipo_via=row.tvia,
            nombre=row.nvia,
            nombre_corto=row.nviac,
        )


@dataclass(frozen=True)
class PseudoviaRecord:
    codigo_provincia: str
    codigo_municipio: str
    codigo_pseudovia: str
    tipo_informacion: str
    causa_devolucion: str
    causa_variacion: str
    descripcion: str

    @classmethod
    def from_row(cls, row: PseudoRoadRow) -> Self:
        require_same("PSEU", "cpsvia", row.cpsvia_previous, row.cpsvia)
        require_same("PSEU", "dpsvia", row.npsvia_previous, row.dpsvia)
        return cls(
            codigo_provincia=row.cpro,
            codigo_municipio=row.cmun,
            codigo_pseudovia=row.cpsvia,
            tipo_informacion=row.tipoinf,
            causa_devolucion=row.cdev,
            causa_variacion=row.cvar,
            descripcion=row.dpsvia,
        )


@dataclass(frozen=True)
class TramoRecord:
    codigo_provincia: str
    codigo_municipio: str
    distrito: str
    seccion: str
    letra_seccion: str
    subseccion: str
    codigo_unidad_poblacional: str
    nombre_entidad_colectiva_corto: str
    nombre_entidad_singular_corto: str
    nombre_nucleo_corto: str
    codigo_via: str
    nombre_via_corto: str
    codigo_pseudovia: str
    descripcion_pseudovia: str
    manzana: str
    codigo_postal: str
    tipo_numeracion: str
    extremo_inferior: str
    calificador_extremo_inferior: str
    extremo_superior: str
    calificador_extremo_superior: str
    tipo_informacion: str
    causa_devolucion: str
    causa_variacion: str

    @classmethod
    def from_row(cls, row: SegmentRow) -> Self:
        require_same("TRAM", "dist", row.dist_previous, row.dist)
        require_same("TRAM", "secc", row.secc_previous, row.secc)
        require_same("TRAM", "lsecc", row.lsecc_previous, row.lsecc)
        require_same("TRAM", "subsc", row.subsc_previous, row.subsc)
        require_same("TRAM", "cun", row.cun_previous, row.cun)
        require_same("TRAM", "cvia", row.cvia_previous, row.cvia)
        require_same("TRAM", "cpsvia", row.cpsvia_previous, row.cpsvia)
        require_same("TRAM", "manz", row.manz_previous, row.manz)
        require_same("TRAM", "cpos", row.cpos_previous, row.cpos)
        require_same("TRAM", "tinum", row.tinum_previous, row.tinum)
        require_same("TRAM", "ein", row.ein_previous, row.ein)
        require_same("TRAM", "cein", row.cein_previous, row.cein)
        require_same("TRAM", "esn", row.esn_previous, row.esn)
        require_same("TRAM", "cesn", row.cesn_previous, row.cesn)
        return cls(
            codigo_provincia=row.cpro,
            codigo_municipio=row.cmun,
            distrito=row.dist,
            seccion=row.secc,
            letra_seccion=row.lsecc,
            subseccion=row.subsc,
            codigo_unidad_poblacional=row.cun,
            nombre_entidad_colectiva_corto=row.nentcoc,
            nombre_entidad_singular_corto=row.nentsic,
            nombre_nucleo_corto=row.nnuclec,
            codigo_via=row.cvia,
            nombre_via_corto=row.nviac,
            codigo_pseudovia=row.cpsvia,
            descripcion_pseudovia=row.dpsvia,
            manzana=row.manz,
            codigo_postal=row.cpos,
            tipo_numeracion=row.tinum,
            extremo_inferior=row.ein,
            calificador_extremo_inferior=row.cein,
            extremo_superior=row.esn,
            calificador_extremo_superior=row.cesn,
            tipo_informacion=row.tipoinf,
            causa_devolucion=row.cdev,
            causa_variacion=row.cvar,
        )


def require_same(source: str, field: str, previous: str, current: str) -> None:
    if previous != current:
        raise BuildSqliteError(f"{source}: previous/result field {field} differs: {previous!r} != {current!r}")
