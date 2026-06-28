# Formato observado de los snapshots principales

Para saber qué significa cada sigla, qué tipo lógico tiene, qué valores especiales
admite y cómo se codifica `CUN`, véase el
[diccionario de datos](./data_dictionary.md). Este documento se centra en la
estructura física y en las observaciones generales.

## Fuentes

- Diseño base: `@upstream/dis_registro.pdf`
- Diseño ampliado: `@upstream/Dis_nuevo.xlsx`
- Validación empírica: `@upstream/caj_esp_072025/` y `@upstream/caj_esp_012026/`

## Rasgos comunes

- Codificación observada: `ISO-8859-1`
- Final de línea observado: `CRLF`
- Relleno: espacios a la derecha en campos alfanuméricos
- Todos los ficheros observados son de anchura fija exacta

## Anchuras

| Fichero | Anchura observada |
| --- | ---: |
| `VIAS` | 132 |
| `PSEU` | 127 |
| `TRAM` | 273 |
| `UP` | 604 |
| `SECC` | 11 |

## `VIAS`

Campos según `Dis_nuevo.xlsx`:

| Campo | Longitud | Posiciones |
| --- | ---: | --- |
| `CPRO` | 2 | 1-2 |
| `CMUN` | 3 | 3-5 |
| `CVIA` | 5 | 6-10 |
| `NVIAC` | 25 | 11-35 |
| `TIPOINF` | 1 | 36 |
| `CDEV` | 2 | 37-38 |
| `FVAR` | 8 | 39-46 |
| `CVAR` | 1 | 47 |
| `CVIA` | 5 | 48-52 |
| `TVIA` | 5 | 53-57 |
| `NVIA` | 50 | 58-107 |
| `NVIAC` | 25 | 108-132 |

Observación empírica:

- En snapshots, la mitad de identificación y la mitad "de variación" están duplicadas y contienen el mismo valor real.
- `TIPOINF`, `CDEV` y `CVAR` van en blanco en todos los registros observados.

## `PSEU`

Campos según `Dis_nuevo.xlsx`:

| Campo | Longitud | Posiciones |
| --- | ---: | --- |
| `CPRO` | 2 | 1-2 |
| `CMUN` | 3 | 3-5 |
| `CPSVIA` | 5 | 6-10 |
| `NPSVIA` | 50 | 11-60 |
| `TIPOINF` | 1 | 61 |
| `CDEV` | 2 | 62-63 |
| `FVAR` | 8 | 64-71 |
| `CVAR` | 1 | 72 |
| `CPSVIA` | 5 | 73-77 |
| `DPSVIA` | 50 | 78-127 |

Observación empírica:

- Igual que en `VIAS`, la parte de identificación y la de datos finales aparecen duplicadas en snapshots.
- `TIPOINF`, `CDEV` y `CVAR` van vacíos en todos los registros observados.

## `TRAM`

Campos según `Dis_nuevo.xlsx`: 39 campos, 273 posiciones.

Aspecto importante:

- La primera mitad describe la clave del tramo.
- La segunda mitad vuelve a exponer la situación final del tramo, añadiendo nombres cortos y descripción de pseudovía.

Observación empírica:

- Los pares duplicados de clave coinciden al 100 % en el snapshot de enero de 2026 (`DIST`, `SECC`, `LSECC`, `SUBSC`, `CUN`, `CVIA`, `CPSVIA`, `MANZ`, `CPOS`, `TINUM`, `EIN`, `CEIN`, `ESN`, `CESN`).
- `TINUM` sólo toma los valores `0`, `1` y `2`, coherentes con "sin numeración", "impar" y "par".

## `UP`

Campos según `Dis_nuevo.xlsx`: 19 campos, 604 posiciones.

Claves:

- `CPRO` 1-2
- `CMUN` 3-5
- `CUN` 6-12

Los nombres no se usan de forma homogénea. Uso observado por tipo de `CUN`:

- Municipio (`CUN = 0000000`): se rellena `NMUN50`, no `NMUN`
- Entidad colectiva (`CC00000`): se rellena `NENTCO`, `NENTCO50`, `NENTCOC`
- Entidad singular (`CCSSD00`): se rellena siempre `NENTSI*`
- Núcleo/diseminado (`CCSSDNN`): se rellena siempre `NNUCLE*`

Distribución observada en enero de 2026:

- Municipios: 8132
- Entidades colectivas: 4904
- Entidades singulares: 62190
- Núcleos/diseminados: 78917

## `SECC`

`SECC` es muy pequeño:

| Campo | Longitud | Posiciones |
| --- | ---: | --- |
| `CPRO` | 2 | 1-2 |
| `CMUN` | 3 | 3-5 |
| `DIST` | 2 | 6-7 |
| `SECC` | 3 | 8-10 |
| `LSECC` | 1 | 11 |

Observación empírica:

- En enero de 2026, `LSECC` aparece siempre en blanco en todos los registros observados.
