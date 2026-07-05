# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Dani Rodríguez

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from scripts.cajesp import Cajesp
from scripts.cajesp.layouts import ALL_LAYOUTS, Layout


def write_references(folder: Path) -> None:
    folder.mkdir(exist_ok=True)
    (folder / "cod_ccaa.csv").write_text("CODIGO;LITERAL\n13;Comunidad de Madrid\n", encoding="utf-8")
    (folder / "cod_provincia.csv").write_text("CODIGO;LITERAL\n28;Madrid\n", encoding="utf-8")
    (folder / "cod_mun.csv").write_text("CODAUTO;CPRO;CMUN;DC;NOMBRE\n13;28;079;6;Madrid\n", encoding="utf-8")
    (folder / "TiposVia.csv").write_text(
        "TIPO_VIA;SINONIMO;DESCRIPCION;COMENTARIO\nCALLE;CALLE;CALLE;\n",
        encoding="utf-8",
    )


def write_snapshot(folder: Path, *, fvar: str = "20260131", overrides: dict[str, str] | None = None) -> None:
    folder.mkdir(exist_ok=True)
    values = {
        "cpro": "28",
        "cmun": "079",
        "dist": "01",
        "dist_previous": "01",
        "secc": "001",
        "secc_previous": "001",
        "fvar": fvar,
        "cvia": "00001",
        "cvia_previous": "00001",
        "cpsvia": "00000",
        "cpsvia_previous": "00000",
        "cun": "0000000",
        "cun_previous": "0000000",
        "cpos": "28001",
        "cpos_previous": "28001",
        "tinum": "0",
        "tinum_previous": "0",
        "ein": "0000",
        "ein_previous": "0000",
        "esn": "0000",
        "esn_previous": "0000",
        "cein": "S",
        "cein_previous": "S",
        "cesn": "S",
        "cesn_previous": "S",
        "tvia": "CALLE",
        "nvia": "CALLE MAYOR",
        "nviac": "MAYOR",
        "nviac_previous": "MAYOR",
        "nmun50": "MADRID",
    }
    if overrides is not None:
        values.update(overrides)
    for layout in ALL_LAYOUTS:
        (folder / f"{layout.prefix}.D260101.G260101").write_bytes(
            f"{line_for(layout, values)}\r\n".encode(Cajesp.ENCODING)
        )


def write_snapshot_zip(folder: Path, snapshot_folder: Path) -> Path:
    zip_file = folder / "caj_esp_test.zip"
    with ZipFile(zip_file, "w") as archive:
        for path in snapshot_folder.iterdir():
            archive.write(path, Path("caj_esp_test") / path.name)
    return zip_file


def line_for(layout: Layout, overrides: dict[str, str]) -> str:
    chars = [" "] * layout.width
    for field in layout.fields:
        width = field.end - field.start
        value = overrides.get(field.name)
        if value is None:
            value = "0" * width if field.kind == "N" else ""
        if len(value) > width:
            raise ValueError(f"test value for {field.name} is wider than {width}: {value!r}")
        padded = value.zfill(width) if field.kind == "N" else value.ljust(width)
        chars[field.start : field.end] = padded
    return "".join(chars)
