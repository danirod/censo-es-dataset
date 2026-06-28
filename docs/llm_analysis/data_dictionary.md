# Diccionario de datos de los snapshots del callejero

Este documento traduce las siglas de los ficheros `VIAS`, `PSEU`, `TRAM`, `UP` y
`SECC` a descripciones legibles y propone tipos adecuados para cargarlos en una
base de datos.

## Cómo leer los tipos

- **Dígitos** (`N` en la documentación del INE): el fichero sólo admite caracteres
  `0`-`9` en esa posición. Salvo las fechas y los límites de portal, deben tratarse
  como texto porque son códigos, pueden empezar por cero y no se calculan.
- **Alfanumérico** (`A`): texto que puede contener letras, dígitos, espacios y
  signos. En el fichero de anchura fija se completa con espacios por la derecha.
- **Fecha `AAAAMMDD`**: ocho dígitos, por ejemplo `20251217`. Conviene convertirla
  a `DATE` al importar, conservando el valor original si se necesita trazabilidad.
- **Vacío**: un campo alfanumérico aparece como espacios. En una base de datos
  suele ser preferible convertirlo a `NULL`.
- Las longitudes son longitudes en caracteres del fichero original, codificado en
  `ISO-8859-1`.

`INTEGER` sólo es recomendable para `EIN` y `ESN`, después de importar. Para todos
los demás campos `N`, el tipo seguro en SQLite es `TEXT` con una restricción de
longitud y, si se desea, otra que exija dígitos.

## Campos comunes

| Campo | Significado en español | Tipo y formato | Dominio y notas |
| --- | --- | --- | --- |
| `CPRO` | Código de provincia | Dígitos, 2 | Identificador territorial con cero inicial posible. Se cruza con `cod_provincia.csv`. |
| `CMUN` | Código de municipio dentro de la provincia | Dígitos, 3 | No es único por sí solo: la clave municipal es `(CPRO, CMUN)`. |
| `TIPOINF` | Tipo de información | Alfanumérico, 1 | Campo de control del formato de intercambio. Está vacío en todos los snapshots analizados. |
| `CDEV` | Causa de devolución | Alfanumérico, 2 | Campo reservado para devoluciones/errores. Está vacío en todos los snapshots analizados. |
| `FVAR` | Fecha de variación | Fecha `AAAAMMDD`, 8 | En los snapshots analizados identifica la fecha asociada al registro. |
| `CVAR` | Código o causa de variación | Enumerado alfanumérico, 1 | En los snapshots está vacío. En ficheros de variaciones: `A` alta, `B` baja, `M` modificación, `R` recodificación, `F` fusión y `S` segregación; no todos aplican a cada fichero. |
| `CUN` | Código de unidad poblacional | Dígitos, 7 | Código jerárquico `CCSSDNN`; se detalla más abajo. |

Cuando un campo aparece dos veces en un registro, la primera aparición pertenece a
los **datos de identificación** y la segunda a los **datos resultantes**. En un
snapshot ambas describen el mismo estado y coinciden en los datos observados. La
duplicación procede del formato de intercambio, que también se usa para comunicar
variaciones.

## `VIAS`: vías o calles

Anchura total: 132 caracteres. Clave lógica recomendada: `(CPRO, CMUN, CVIA)`.

| Pos. | Campo | Significado en español | Tipo y formato | Dominio y notas |
| ---: | --- | --- | --- | --- |
| 1-2 | `CPRO` | Código de provincia | Dígitos, 2 | Véase campos comunes. |
| 3-5 | `CMUN` | Código de municipio | Dígitos, 3 | Véase campos comunes. |
| 6-10 | `CVIA` | Código de vía, identificación | Dígitos, 5 | Identificador local al municipio; conservar ceros iniciales. |
| 11-35 | `NVIAC` | Nombre corto de la vía, identificación | Alfanumérico, 25 | Puede estar abreviado o truncado; no sustituye al nombre completo. El PDF antiguo lo rotula `AVIAC`, aparentemente una errata/prefijo de “anterior”. |
| 36 | `TIPOINF` | Tipo de información | Alfanumérico, 1 | Vacío en los snapshots observados. |
| 37-38 | `CDEV` | Causa de devolución | Alfanumérico, 2 | Vacío en los snapshots observados. |
| 39-46 | `FVAR` | Fecha de variación | Fecha `AAAAMMDD`, 8 | Ocho dígitos. |
| 47 | `CVAR` | Código de variación | Enumerado alfanumérico, 1 | Vacío en snapshots; en variaciones admite `A`, `B`, `M` o `R`. |
| 48-52 | `CVIA` | Código de vía resultante | Dígitos, 5 | Segunda aparición del código. |
| 53-57 | `TVIA` | Tipo de vía | Código alfanumérico, 5 | Ejemplos conceptuales: calle, avenida, plaza. Se normaliza con `TiposVia.csv`; se observaron también `GRNJA` y `DISEM`, ausentes del catálogo. |
| 58-107 | `NVIA` | Nombre completo de la vía | Alfanumérico, 50 | Nombre preferible para mostrar y comparar. No incluye necesariamente el tipo `TVIA`. |
| 108-132 | `NVIAC` | Nombre corto de la vía resultante | Alfanumérico, 25 | Versión abreviada o compacta de `NVIA`. |

## `PSEU`: pseudovías

Una pseudovía identifica agrupaciones de direcciones que no se ajustan a una vía
convencional. Anchura total: 127 caracteres. Clave lógica recomendada:
`(CPRO, CMUN, CPSVIA)`.

| Pos. | Campo | Significado en español | Tipo y formato | Dominio y notas |
| ---: | --- | --- | --- | --- |
| 1-2 | `CPRO` | Código de provincia | Dígitos, 2 | Véase campos comunes. |
| 3-5 | `CMUN` | Código de municipio | Dígitos, 3 | Véase campos comunes. |
| 6-10 | `CPSVIA` | Código de pseudovía, identificación | Dígitos, 5 | Identificador local al municipio; conservar ceros iniciales. |
| 11-60 | `NPSVIA` | Nombre de la pseudovía, identificación | Alfanumérico, 50 | El PDF antiguo lo llama `ANPSVIA`; el diseño actual usa `NPSVIA`. |
| 61 | `TIPOINF` | Tipo de información | Alfanumérico, 1 | Vacío en los snapshots observados. |
| 62-63 | `CDEV` | Causa de devolución | Alfanumérico, 2 | Vacío en los snapshots observados. |
| 64-71 | `FVAR` | Fecha de variación | Fecha `AAAAMMDD`, 8 | Ocho dígitos. |
| 72 | `CVAR` | Código de variación | Enumerado alfanumérico, 1 | Vacío en snapshots; en variaciones admite `A`, `B`, `M` o `R`. |
| 73-77 | `CPSVIA` | Código de pseudovía resultante | Dígitos, 5 | Segunda aparición del código. |
| 78-127 | `DPSVIA` | Descripción de la pseudovía resultante | Alfanumérico, 50 | Equivale al nombre descriptivo final. Coincide con `NPSVIA` en todos los snapshots observados. |

## `TRAM`: tramos de numeración

Cada fila vincula territorio, unidad poblacional, vía o pseudovía, código postal y
un intervalo de portales. Anchura total: 273 caracteres. Los campos de las
posiciones 1-58 identifican el tramo; los de 71-273 describen su estado resultante.

| Pos. | Campo | Significado en español | Tipo y formato | Dominio y notas |
| ---: | --- | --- | --- | --- |
| 1-2 | `CPRO` | Código de provincia | Dígitos, 2 | Siempre informado según la especificación. |
| 3-5 | `CMUN` | Código de municipio | Dígitos, 3 | Siempre informado según la especificación. |
| 6-7 / 71-72 | `DIST` | Código de distrito censal | Dígitos, 2 | Código dentro del municipio. |
| 8-10 / 73-75 | `SECC` | Código de sección censal | Dígitos, 3 | Se cruza con `SECC` usando provincia, municipio y distrito. |
| 11 / 76 | `LSECC` | Letra de sección | Alfanumérico, 1 | Extensión o calificador de la sección; puede estar vacío. |
| 12-13 / 77-78 | `SUBSC` | Código de subsección | Alfanumérico, 2 | Puede contener dígitos o quedar vacío; tratar como texto. |
| 14-20 / 79-85 | `CUN` | Código de unidad poblacional | Dígitos, 7 | Véase la descomposición `CCSSDNN`. |
| 21-25 / 161-165 | `CVIA` | Código de vía | Dígitos, 5 | `00000` significa que el tramo no está asociado a una vía. |
| 26-30 / 191-195 | `CPSVIA` | Código de pseudovía | Dígitos, 5 | `00000` significa que no está asociado a una pseudovía. No se observó ningún tramo con `CVIA` y `CPSVIA` informados simultáneamente. |
| 31-42 / 246-257 | `MANZ` | Manzana | Alfanumérico, 12 | La especificación de variaciones dice que no se informa. Tratar como campo reservado. |
| 43-47 / 258-262 | `CPOS` | Código postal | Dígitos, 5 | Identificador textual, siempre con cinco caracteres y posible cero inicial. No es único por municipio ni el municipio es único por código postal. |
| 48 / 263 | `TINUM` | Tipo o paridad de numeración | Enumerado numérico, 1 | `0` sin numeración, `1` numeración impar, `2` numeración par. Son los únicos valores observados. |
| 49-52 / 264-267 | `EIN` | Extremo inferior numérico del tramo | Dígitos, 4 | Número de portal inicial. Puede convertirse a `INTEGER`; los ceros representan ausencia/sin numeración según el contexto. |
| 53 / 268 | `CEIN` | Calificador del extremo inferior | Alfanumérico, 1 | Sufijo del portal inicial, por ejemplo una letra; puede estar vacío. |
| 54-57 / 269-272 | `ESN` | Extremo superior numérico del tramo | Dígitos, 4 | Número de portal final. Puede convertirse a `INTEGER`. |
| 58 / 273 | `CESN` | Calificador del extremo superior | Alfanumérico, 1 | Sufijo del portal final; puede estar vacío. |
| 59 | `TIPOINF` | Tipo de información | Alfanumérico, 1 | Vacío en los snapshots observados. |
| 60-61 | `CDEV` | Causa de devolución | Alfanumérico, 2 | Vacío en los snapshots observados. |
| 62-69 | `FVAR` | Fecha de variación | Fecha `AAAAMMDD`, 8 | Ocho dígitos. |
| 70 | `CVAR` | Código de variación | Enumerado alfanumérico, 1 | Vacío en snapshots; en variaciones admite `A`, `B`, `M`, `F` o `S`. |
| 86-110 | `NENTCOC` | Nombre corto de entidad colectiva | Alfanumérico, 25 | Nombre contextual de la jerarquía poblacional. Puede estar vacío si ese nivel no aplica. |
| 111-135 | `NENTSIC` | Nombre corto de entidad singular | Alfanumérico, 25 | Nombre contextual de la jerarquía poblacional. |
| 136-160 | `NNUCLEC` | Nombre corto de núcleo o diseminado | Alfanumérico, 25 | Nombre contextual del núcleo/diseminado. |
| 166-190 | `NVIAC` | Nombre corto de vía | Alfanumérico, 25 | Vacío cuando no hay vía. |
| 196-245 | `DPSVIA` | Descripción de pseudovía | Alfanumérico, 50 | Vacío cuando no hay pseudovía. |

En `TRAM`, todos los campos mostrados con dos intervalos de posiciones están
duplicados: primero identificación y después estado resultante. La clave física
completa debe incluir los campos territoriales, la vía/pseudovía y el intervalo; no
debe reducirse sólo a `(CPRO, CMUN, CVIA)`.

## `UP`: unidades poblacionales

Anchura total: 604 caracteres. Clave lógica recomendada: `(CPRO, CMUN, CUN)`.
Los nombres se presentan en tres longitudes: completo (70), medio (50) y corto
(25). No todos los niveles se rellenan en todas las filas.

| Pos. | Campo | Significado en español | Tipo y formato | Dominio y notas |
| ---: | --- | --- | --- | --- |
| 1-2 | `CPRO` | Código de provincia | Dígitos, 2 | Véase campos comunes. |
| 3-5 | `CMUN` | Código de municipio | Dígitos, 3 | Véase campos comunes. |
| 6-12 | `CUN` | Código de unidad poblacional | Dígitos, 7 | Determina el nivel jerárquico; véase la sección siguiente. |
| 13 | `TIPOINF` | Tipo de información | Alfanumérico, 1 | Vacío en los snapshots observados. |
| 14-15 | `CDEV` | Causa de devolución | Alfanumérico, 2 | Vacío en los snapshots observados. |
| 16-23 | `FVAR` | Fecha de variación | Fecha `AAAAMMDD`, 8 | Ocho dígitos. |
| 24 | `CVAR` | Código de variación | Enumerado alfanumérico, 1 | Vacío en snapshots; en variaciones admite `A`, `B` o `M`. |
| 25-94 | `NMUN` | Nombre completo del municipio | Alfanumérico, 70 | En los snapshots observados suele estar vacío en la fila municipal. |
| 95-144 | `NMUN50` | Nombre del municipio, hasta 50 caracteres | Alfanumérico, 50 | Es el campo municipal realmente informado en las filas `CUN = 0000000` observadas. |
| 145-169 | `NMUNC` | Nombre corto del municipio | Alfanumérico, 25 | Puede estar vacío. |
| 170-239 | `NENTCO` | Nombre completo de entidad colectiva | Alfanumérico, 70 | Se informa cuando aplica ese nivel. |
| 240-289 | `NENTCO50` | Nombre de entidad colectiva, hasta 50 caracteres | Alfanumérico, 50 | Variante de longitud media. |
| 290-314 | `NENTCOC` | Nombre corto de entidad colectiva | Alfanumérico, 25 | Variante corta. |
| 315-384 | `NENTSI` | Nombre completo de entidad singular | Alfanumérico, 70 | Se informa en filas de entidad singular y niveles inferiores. |
| 385-434 | `NENTSI50` | Nombre de entidad singular, hasta 50 caracteres | Alfanumérico, 50 | Variante de longitud media. |
| 435-459 | `NENTSIC` | Nombre corto de entidad singular | Alfanumérico, 25 | Variante corta. |
| 460-529 | `NNUCLE` | Nombre completo de núcleo o diseminado | Alfanumérico, 70 | Se informa en filas de núcleo/diseminado. |
| 530-579 | `NNUCLE50` | Nombre de núcleo/diseminado, hasta 50 caracteres | Alfanumérico, 50 | Variante de longitud media. |
| 580-604 | `NNUCLEC` | Nombre corto de núcleo/diseminado | Alfanumérico, 25 | Variante corta. |

### Cómo se codifica `CUN`

`CUN` tiene la estructura oficial `CCSSDNN`:

| Parte | Posición | Significado |
| --- | ---: | --- |
| `CC` | 1-2 | Código de entidad colectiva. |
| `SS` | 3-4 | Código de entidad singular. |
| `D` | 5 | Dígito de control de la entidad singular. |
| `NN` | 6-7 | Código de núcleo o diseminado. |

El nivel se reconoce por los bloques puestos a cero:

| Patrón | Nivel representado |
| --- | --- |
| `0000000` | Municipio. |
| `CC00000` | Entidad colectiva. |
| `CCSSD00` | Entidad singular. |
| `CCSSDNN` | Núcleo o diseminado. |

La documentación local identifica `D` como dígito de control, pero no contiene su
algoritmo de cálculo. Por tanto, puede conservarse y compararse como parte del
código oficial, pero no debería recalcularse mediante una fórmula inventada. El PDF
de variaciones escribe una vez `000000` para municipio (seis ceros); dado que
define `CUN` como `N(7)`, el valor coherente y observado es `0000000`.

## `SECC`: secciones censales

Anchura observada: 11 caracteres. Clave lógica recomendada:
`(CPRO, CMUN, DIST, SECC, LSECC)`.

| Pos. | Campo | Significado en español | Tipo y formato | Dominio y notas |
| ---: | --- | --- | --- | --- |
| 1-2 | `CPRO` | Código de provincia | Dígitos, 2 | Véase campos comunes. |
| 3-5 | `CMUN` | Código de municipio | Dígitos, 3 | Véase campos comunes. |
| 6-7 | `DIST` | Código de distrito censal | Dígitos, 2 | Código dentro del municipio. |
| 8-10 | `SECC` | Código de sección censal | Dígitos, 3 | Código dentro del distrito. |
| 11 | `LSECC` | Letra de sección | Alfanumérico, 1 | Siempre vacío en enero de 2026, pero forma parte de la anchura observada y conviene conservarlo. |

Hay una discrepancia de fuente: la hoja `SECC` de `Dis_nuevo.xlsx` termina en la
posición 10 y no enumera `LSECC`, mientras que los ficheros reales miden 11
caracteres y `TRAM` sí define ese campo. La tabla anterior documenta el formato
real observado.

## Fuentes y grado de certeza

- Nombres, formatos y longitudes oficiales: `upstream/Dis_nuevo.xlsx`.
- Descripciones y dominios de variación: `upstream/dis_registro.pdf` y
  `upstream/Variacionesencallejero.pdf`.
- Valores vacíos, duplicación, dominios reales y casos especiales:
  snapshots `upstream/caj_esp_072025/` y `upstream/caj_esp_012026/`.
- Catálogos territoriales y tipos de vía: `upstream/cod_provincia.csv`,
  `upstream/cod_mun.csv` y `upstream/TiposVia.csv`.

