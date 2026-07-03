# Layout de los ficheros de variaciones

Las posiciones son inclusivas y empiezan en 1. Los cuatro ficheros usan
ISO-8859-1, `CRLF` y anchura fija.

## Campos de control

| Campo | Significado | Tipo | Dominio |
| --- | --- | --- | --- |
| `TIPOINF` | Tipo de información | `A(1)` | Vacío en el bundle. |
| `CDEV` | Causa de devolución | `A(2)` | Vacío en el bundle. |
| `FVAR` | Fecha del cambio | `N(8)` | `AAAAMMDD`. |
| `NSEC` | Ordinal auxiliar | `N(4)` | Observados `0001`-`0003`; no es único ni orden global. |
| `CVAR` | Operación | `A(1)` | Depende del fichero. |

## `VIAS`, anchura 112

| Pos. | Campo | Tipo | Parte |
| ---: | --- | --- | --- |
| 1-2 | `CPRO` | `N(2)` | Identificación |
| 3-5 | `CMUN` | `N(3)` | Identificación |
| 6-10 | `CVIA` | `N(5)` | Identificación |
| 11 | `TIPOINF` | `A(1)` | Control |
| 12-13 | `CDEV` | `A(2)` | Control |
| 14-21 | `FVAR` | `N(8)` | Control |
| 22-25 | `NSEC` | `N(4)` | Control |
| 26 | `CVAR` | `A(1)` | Control |
| 27-31 | `CVIA` | `N(5)` | Resultado |
| 32-36 | `TVIA` | `A(5)` | Resultado |
| 37 | `POS` | `N(1)` | Resultado |
| 38-87 | `NVIA` | `A(50)` | Resultado |
| 88-112 | `NVIAC` | `A(25)` | Resultado |

`POS` es “posición del tipo de vía”. El PDF dice que no es necesario y debe ir
vacío; el bundle lo rellena con `0` en las 10.487 filas. Tratarlo como relleno
heredado, no como posición útil.

## `PSEU`, anchura 81

| Pos. | Campo | Tipo | Parte |
| ---: | --- | --- | --- |
| 1-2 | `CPRO` | `N(2)` | Identificación |
| 3-5 | `CMUN` | `N(3)` | Identificación |
| 6-10 | `CPSVIA` | `N(5)` | Identificación |
| 11 | `TIPOINF` | `A(1)` | Control |
| 12-13 | `CDEV` | `A(2)` | Control |
| 14-21 | `FVAR` | `N(8)` | Control |
| 22-25 | `NSEC` | `N(4)` | Control |
| 26 | `CVAR` | `A(1)` | Control |
| 27-31 | `CPSVIA` | `N(5)` | Resultado |
| 32-81 | `DPSVIA` | `A(50)` | Resultado |

## `TRAM`, anchura 127

Las posiciones 1-58 tienen exactamente los campos identificadores definidos en
[campos de TRAM](./fields_tram.md), desde `CPRO` hasta `CESN`.

| Pos. | Campo | Tipo | Parte |
| ---: | --- | --- | --- |
| 1-58 | Bloque anterior | 16 campos | Identificación |
| 59 | `TIPOINF` | `A(1)` | Control |
| 60-61 | `CDEV` | `A(2)` | Control |
| 62-69 | `FVAR` | `N(8)` | Control |
| 70-73 | `NSEC` | `N(4)` | Control |
| 74 | `CVAR` | `A(1)` | Control |
| 75-76 | `DIST` | `N(2)` | Resultado |
| 77-79 | `SECC` | `N(3)` | Resultado |
| 80 | `LSECC` | `A(1)` | Resultado |
| 81-82 | `SUBSC` | `A(2)` | Resultado |
| 83-89 | `CUN` | `N(7)` | Resultado |
| 90-94 | `CVIA` | `N(5)` | Resultado |
| 95-99 | `CPSVIA` | `N(5)` | Resultado |
| 100-111 | `MANZ` | `A(12)` | Resultado |
| 112-116 | `CPOS` | `N(5)` | Resultado |
| 117 | `TINUM` | `N(1)` | Resultado |
| 118-121 | `EIN` | `N(4)` | Resultado |
| 122 | `CEIN` | `A(1)` | Resultado |
| 123-126 | `ESN` | `N(4)` | Resultado |
| 127 | `CESN` | `A(1)` | Resultado |

`MANZ`, `LSECC` y `SUBSC` están vacíos en todo el bundle analizado.

## `UP`, anchura 608

| Pos. | Campo | Tipo | Parte |
| ---: | --- | --- | --- |
| 1-2 | `CPRO` | `N(2)` | Identificación |
| 3-5 | `CMUN` | `N(3)` | Identificación |
| 6-12 | `CUN` | `N(7)` | Identificación |
| 13 | `TIPOINF` | `A(1)` | Control |
| 14-15 | `CDEV` | `A(2)` | Control |
| 16-23 | `FVAR` | `N(8)` | Control |
| 24-27 | `NSEC` | `N(4)` | Control |
| 28 | `CVAR` | `A(1)` | Control |
| 29-98 | `NMUN` | `A(70)` | Resultado |
| 99-148 | `NMUN50` | `A(50)` | Resultado |
| 149-173 | `NMUNC` | `A(25)` | Resultado |
| 174-243 | `NENTCO` | `A(70)` | Resultado |
| 244-293 | `NENTCO50` | `A(50)` | Resultado |
| 294-318 | `NENTCOC` | `A(25)` | Resultado |
| 319-388 | `NENTSI` | `A(70)` | Resultado |
| 389-438 | `NENTSI50` | `A(50)` | Resultado |
| 439-463 | `NENTSIC` | `A(25)` | Resultado |
| 464-533 | `NNUCLE` | `A(70)` | Resultado |
| 534-583 | `NNUCLE50` | `A(50)` | Resultado |
| 584-608 | `NNUCLEC` | `A(25)` | Resultado |

`UP` no repite `CUN` en el resultado. El código está informado incluso en altas;
sólo el bloque de nombres queda vacío en bajas.

## Ceros y blancos por operación

El bundle materializa el principio anterior/resultado así:

| Operación | Identificación | Resultado |
| --- | --- | --- |
| `A` | Centinelas `0` y espacios | Informado |
| `B` | Informado | Centinelas `0` y espacios |
| `M`, `R`, `F`, `S` | Informado | Informado |

La excepción estructural es `UP`, cuyo único `CUN` siempre identifica la unidad.
No hay que exigir espacios literales donde el PDF dice “blanco”: los campos
numéricos ausentes suelen contener ceros.
