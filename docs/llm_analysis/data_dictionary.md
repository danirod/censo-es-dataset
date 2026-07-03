# Diccionario de datos: convenciones comunes

Este documento explica las convenciones compartidas por los snapshots. Los campos
específicos están separados por familia:

- [Vías y pseudovías](./fields_vias_pseu.md)
- [Tramos](./fields_tram.md)
- [Unidades poblacionales y secciones](./fields_up_secc.md)
- [Ficheros de variaciones](./variation_layouts.md)
- [Catálogos CSV](./reference_catalogs.md)

## Tipos físicos

| Notación INE | Significado físico | Tratamiento recomendado |
| --- | --- | --- |
| `N(n)` | Exactamente `n` posiciones destinadas a dígitos | Importar como `TEXT`, salvo cantidades que realmente se calculen. |
| `A(n)` | `n` posiciones alfanuméricas | Decodificar y quitar sólo los espacios de relleno de la derecha. |
| Fecha `N(8)` | `AAAAMMDD`, por ejemplo `20251231` | Validar como fecha y convertir opcionalmente a `DATE`. |

Los códigos `N` no son cantidades: `01`, `001`, `00001` y `01008` perderían
información si se convirtieran prematuramente a enteros. En SQLite conviene usar
`TEXT` con comprobaciones de longitud y dígitos. `EIN` y `ESN` sí pueden tener una
columna numérica derivada para comparar portales.

Los campos `A` se justifican a la izquierda y se rellenan con espacios a la
derecha. Un campo vacío ocupa toda su anchura con espacios. No deben eliminarse
espacios interiores ni normalizarse tildes durante la ingesta.

## Campos comunes

| Campo | Significado | Tipo | Notas |
| --- | --- | --- | --- |
| `CPRO` | Código de provincia | `N(2)` | Clave textual; puede empezar por cero. |
| `CMUN` | Código de municipio dentro de la provincia | `N(3)` | Sólo es único junto con `CPRO`. |
| `TIPOINF` | Tipo de información | `A(1)` | Vacío en ambos snapshots y en el bundle analizado. El formato de intercambio histórico admite blanco, `C` (cumplimentada por el INE) y `R` (rechazada). |
| `CDEV` | Causa de devolución | `A(2)` | Reservado para devoluciones/errores; vacío en todos los datos analizados. No hay catálogo local de causas. |
| `FVAR` | Fecha de referencia o de variación | `N(8)` | Su semántica depende del tipo de fichero; véase abajo. |
| `CVAR` | Causa de variación | `A(1)` | Vacío en snapshots. En variaciones usa un dominio enumerado. |
| `CUN` | Código de unidad poblacional | `N(7)` | Estructura `CCSSDNN`; se explica en [unidades poblacionales](./fields_up_secc.md). |

## Dos significados de `FVAR`

- En los **snapshots**, `FVAR` no es la última modificación individual. Es igual a
  la fecha de referencia en todas las filas: `20250630` en julio de 2025 y
  `20251231` en enero de 2026.
- En los **ficheros de variaciones**, `FVAR` es la fecha atribuida al cambio y toma
  múltiples valores dentro del periodo.

Confundir ambos usos produciría una columna `updated_at` falsa en una base de
datos.

## Identificación y resultado

El formato procede de ficheros de intercambio:

1. Datos que identifican el registro anterior.
2. Campos de control.
3. Datos resultantes de la variación.

Los snapshots reutilizan esa estructura aunque no sean eventos. Por eso `VIAS`,
`PSEU` y `TRAM` repiten campos. En los dos snapshots analizados, todos los pares
duplicados coinciden exactamente. Para una tabla canónica basta una copia; para
auditoría conviene conservar también la línea original.

## Vacíos, ceros y `NULL`

- Espacios significan campo físico vacío.
- Ceros pueden ser parte de un código o un centinela documentado; no equivalen de
  forma general a ausencia.
- En `TRAM`, `CVIA=00000` y `CPSVIA=00000` significan que esa referencia no aplica.
- En claves compuestas, convertir blancos a `NULL` puede romper la unicidad de
  SQLite. Es más seguro usar `''` en la tabla canónica o declarar todas las
  columnas de la clave `NOT NULL`.

## Codificación de caracteres

Los ficheros de anchura fija se han validado como `ISO-8859-1`, con `CRLF`. No son
UTF-8. Los CSV auxiliares sí son UTF-8 y no comparten todos el mismo estilo de
final de línea; `TiposVia.csv` incluye además BOM.
