# Campos de `UP` y `SECC`

## `UP`: unidades poblacionales

Anchura: 604. Clave: `(CPRO, CMUN, CUN)`.

| Pos. | Campo | Significado | Tipo | Notas |
| ---: | --- | --- | --- | --- |
| 1-2 | `CPRO` | Provincia | `N(2)` | Parte de la clave. |
| 3-5 | `CMUN` | Municipio | `N(3)` | Parte de la clave. |
| 6-12 | `CUN` | Unidad poblacional | `N(7)` | Parte jerárquica de la clave. |
| 13 | `TIPOINF` | Tipo de información | `A(1)` | Vacío observado. |
| 14-15 | `CDEV` | Causa de devolución | `A(2)` | Vacío observado. |
| 16-23 | `FVAR` | Fecha de referencia | `N(8)` | Constante para todo el snapshot. |
| 24 | `CVAR` | Causa de variación | `A(1)` | Vacío observado. |
| 25-94 | `NMUN` | Nombre municipal largo | `A(70)` | Vacío en todas las filas observadas. |
| 95-144 | `NMUN50` | Nombre municipal de 50 caracteres | `A(50)` | Nombre municipal realmente utilizado. |
| 145-169 | `NMUNC` | Nombre municipal corto | `A(25)` | Vacío en todas las filas observadas. |
| 170-239 | `NENTCO` | Nombre largo de entidad colectiva | `A(70)` | Informado cuando la jerarquía contiene ese nivel. |
| 240-289 | `NENTCO50` | Nombre medio de entidad colectiva | `A(50)` | Igual alcance que `NENTCO`. |
| 290-314 | `NENTCOC` | Nombre corto de entidad colectiva | `A(25)` | Usado también de forma denormalizada en `TRAM`. |
| 315-384 | `NENTSI` | Nombre largo de entidad singular | `A(70)` | Informado para singular y niveles inferiores. |
| 385-434 | `NENTSI50` | Nombre medio de entidad singular | `A(50)` | Variante de longitud. |
| 435-459 | `NENTSIC` | Nombre corto de entidad singular | `A(25)` | Usado también en `TRAM`. |
| 460-529 | `NNUCLE` | Nombre largo de núcleo/diseminado | `A(70)` | Informado sólo en ese nivel. |
| 530-579 | `NNUCLE50` | Nombre medio de núcleo/diseminado | `A(50)` | Variante de longitud. |
| 580-604 | `NNUCLEC` | Nombre corto de núcleo/diseminado | `A(25)` | Usado también en `TRAM`. |

## Estructura de `CUN`

`CUN` se descompone como `CCSSDNN`:

| Parte | Pos. | Significado |
| --- | ---: | --- |
| `CC` | 1-2 | Entidad colectiva. |
| `SS` | 3-4 | Entidad singular. |
| `D` | 5 | Dígito de control de `CCSS`. |
| `NN` | 6-7 | Núcleo o diseminado. |

| Patrón | Nivel |
| --- | --- |
| `0000000` | Municipio |
| `CC00000` | Entidad colectiva |
| `CCSSD00` | Entidad singular |
| `CCSSDNN`, con `NN` distinto de `00` y `99` | Núcleo |
| `CCSSD99` | Diseminado |

El dígito `D` se obtiene oficialmente mediante el método ABC aplicado a `CCSS`.
El INE asigna y distribuye `CUN`; las fuentes de diseño no ofrecen una fórmula
operativa corta y no conviene inventarla. Debe conservarse como parte indivisible
del código.

En enero de 2026 hay 41.348 filas con `NN=99`; todas representan diseminados.
La denominación larga y media es casi siempre `*DISEMINADO*`, pero el nombre corto
presenta algunas variantes editoriales, así que el nivel debe inferirse del código,
no del texto.

El PDF de variaciones imprime una vez `000000` para municipio. Es una errata: el
campo mide siete posiciones y los datos usan `0000000`.

## Matriz real de nombres

Número de filas con cada familia de nombre informada en enero de 2026:

| Nivel | Filas | `NMUN50` | `NENTCO*` | `NENTSI*` | `NNUCLE*` |
| --- | ---: | ---: | ---: | ---: | ---: |
| Municipio | 8.132 | 8.132 | 0 | 0 | 0 |
| Entidad colectiva | 4.904 | 0 | 4.904 | 0 | 0 |
| Entidad singular | 62.190 | 62.190 | 38.500 | 62.190 | 0 |
| Núcleo/diseminado | 78.917 | 78.917 | 40.394 | 78.917 | 78.917 |

Las entidades singulares sin colectiva tienen `CC=00`, por eso sus campos
`NENTCO*` están vacíos. Todos los padres esperables existen: no se encontraron
singulares huérfanas de colectiva ni núcleos huérfanos de singular.

## `SECC`: secciones censales

Anchura real: 11. Clave: `(CPRO, CMUN, DIST, SECC, LSECC)`.

| Pos. | Campo | Significado | Tipo | Notas |
| ---: | --- | --- | --- | --- |
| 1-2 | `CPRO` | Provincia | `N(2)` | Parte de la clave. |
| 3-5 | `CMUN` | Municipio | `N(3)` | Parte de la clave. |
| 6-7 | `DIST` | Distrito censal | `N(2)` | Parte de la clave. |
| 8-10 | `SECC` | Sección censal | `N(3)` | Parte de la clave. |
| 11 | `LSECC` | Letra de sección | `A(1)` | Vacía en ambos snapshots, pero debe conservarse. |

`Dis_nuevo.xlsx` termina `SECC` en la posición 10 y omite `LSECC`. Los ficheros
reales miden 11 y `TRAM` también define esa letra; aquí prevalece la evidencia del
fichero.
