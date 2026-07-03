# Campos de `VIAS` y `PSEU`

Las posiciones son inclusivas y empiezan en 1. Para tipos, relleno y campos de
control, véase [convenciones comunes](./data_dictionary.md).

## `VIAS`

Contiene una vía lógica por código municipal. Anchura: 132. Clave:
`(CPRO, CMUN, CVIA)`.

| Pos. | Campo | Significado | Tipo | Notas |
| ---: | --- | --- | --- | --- |
| 1-2 | `CPRO` | Provincia | `N(2)` | Parte de la clave. |
| 3-5 | `CMUN` | Municipio | `N(3)` | Parte de la clave. |
| 6-10 | `CVIA` | Código anterior de vía | `N(5)` | Único dentro del municipio. |
| 11-35 | `NVIAC` | Nombre corto anterior | `A(25)` | Abreviado o truncado; coincide con el segundo `NVIAC` en snapshots. |
| 36 | `TIPOINF` | Tipo de información | `A(1)` | Vacío observado. |
| 37-38 | `CDEV` | Causa de devolución | `A(2)` | Vacío observado. |
| 39-46 | `FVAR` | Fecha de referencia | `N(8)` | Constante para todo el snapshot. |
| 47 | `CVAR` | Causa de variación | `A(1)` | Vacío observado. |
| 48-52 | `CVIA` | Código resultante de vía | `N(5)` | Igual al anterior en snapshots. |
| 53-57 | `TVIA` | Tipo de vía | `A(5)` | Código o grafía, no una descripción libre. |
| 58-107 | `NVIA` | Nombre completo de vía | `A(50)` | Campo preferible para presentación. |
| 108-132 | `NVIAC` | Nombre corto resultante | `A(25)` | Útil para índices compactos, no equivalente semántico a `NVIA`. |

`TVIA` debe contrastarse con `TiposVia.csv`, pero ese CSV expresa relaciones de
sinonimia y no elige siempre un único código canónico. El valor `.` está marcado
en el catálogo como tipo a extinguir. En enero de 2026 también aparecen `GRNJA` y
`DISEM`, no presentes en el catálogo.

El PDF de 2009 llama `AVIAC` al primer nombre corto y tipa el segundo `CVIA` como
alfanumérico. `Dis_nuevo.xlsx` y los datos reales usan `NVIAC` y cinco dígitos,
respectivamente; este diccionario sigue el fichero real.

## `PSEU`

Una pseudovía describe una agrupación de direcciones que no es una unidad
poblacional ni una vía convencional, por ejemplo ciertos barrios o
urbanizaciones. Históricamente puede sustituir o complementar a una vía; en los
snapshots analizados ningún `TRAM` referencia vía y pseudovía a la vez.

Anchura: 127. Clave: `(CPRO, CMUN, CPSVIA)`.

| Pos. | Campo | Significado | Tipo | Notas |
| ---: | --- | --- | --- | --- |
| 1-2 | `CPRO` | Provincia | `N(2)` | Parte de la clave. |
| 3-5 | `CMUN` | Municipio | `N(3)` | Parte de la clave. |
| 6-10 | `CPSVIA` | Código anterior de pseudovía | `N(5)` | Único dentro del municipio. |
| 11-60 | `NPSVIA` | Nombre anterior de pseudovía | `A(50)` | Identificación textual. |
| 61 | `TIPOINF` | Tipo de información | `A(1)` | Vacío observado. |
| 62-63 | `CDEV` | Causa de devolución | `A(2)` | Vacío observado. |
| 64-71 | `FVAR` | Fecha de referencia | `N(8)` | Constante para todo el snapshot. |
| 72 | `CVAR` | Causa de variación | `A(1)` | Vacío observado. |
| 73-77 | `CPSVIA` | Código resultante | `N(5)` | Igual al anterior en snapshots. |
| 78-127 | `DPSVIA` | Descripción resultante | `A(50)` | Coincide exactamente con `NPSVIA` en ambos snapshots. |

El PDF antiguo usa los nombres `ACPSVIA`, `ANPSVIA`, `NCPSVIA` y `NNPSVIA` para
marcar anterior/nuevo. El Excel actual elimina esos prefijos; la posición, no el
nombre alternativo, determina qué aparición es anterior o resultante.
