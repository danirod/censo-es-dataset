# Campos de `TRAM`

`TRAM` vincula una sección censal, una unidad poblacional, una vía o pseudovía, un
código postal y un intervalo de numeración. Anchura: 273.

Las posiciones 1-58 identifican el tramo anterior; 59-70 son control; 71-273
describen el resultado y añaden nombres denormalizados.

## Layout

| Pos. anterior / resultante | Campo | Significado | Tipo | Dominio o valor especial |
| --- | --- | --- | --- | --- |
| 1-2 | `CPRO` | Provincia | `N(2)` | Siempre informada. |
| 3-5 | `CMUN` | Municipio | `N(3)` | Siempre informado. |
| 6-7 / 71-72 | `DIST` | Distrito censal | `N(2)` | Código dentro del municipio. |
| 8-10 / 73-75 | `SECC` | Sección censal | `N(3)` | Código dentro del distrito. |
| 11 / 76 | `LSECC` | Letra de sección | `A(1)` | Vacía en ambos snapshots. |
| 12-13 / 77-78 | `SUBSC` | Subsección | `A(2)` | Observados blanco y `01`-`06`; no asumir universo cerrado. |
| 14-20 / 79-85 | `CUN` | Unidad poblacional | `N(7)` | Referencia exacta a `UP`. |
| 21-25 / 161-165 | `CVIA` | Vía | `N(5)` | `00000`: sin vía. |
| 26-30 / 191-195 | `CPSVIA` | Pseudovía | `N(5)` | `00000`: sin pseudovía. |
| 31-42 / 246-257 | `MANZ` | Manzana catastral | `A(12)` | Vacía en ambos snapshots y en variaciones. |
| 43-47 / 258-262 | `CPOS` | Código postal | `N(5)` | Texto de cinco dígitos; nunca vacío ni `00000` observado. |
| 48 / 263 | `TINUM` | Tipo de numeración | `N(1)` | `0` sin numeración, `1` impar, `2` par. |
| 49-52 / 264-267 | `EIN` | Extremo inferior | `N(4)` | Parte numérica del portal inicial. |
| 53 / 268 | `CEIN` | Calificador inferior | `A(1)` | Blanco o sufijo alfanumérico. |
| 54-57 / 269-272 | `ESN` | Extremo superior | `N(4)` | Parte numérica del portal final. |
| 58 / 273 | `CESN` | Calificador superior | `A(1)` | Blanco o sufijo alfanumérico. |
| 59 | `TIPOINF` | Tipo de información | `A(1)` | Vacío observado. |
| 60-61 | `CDEV` | Causa de devolución | `A(2)` | Vacío observado. |
| 62-69 | `FVAR` | Fecha de referencia | `N(8)` | Constante para todo el snapshot. |
| 70 | `CVAR` | Causa de variación | `A(1)` | Vacío observado. |
| 86-110 | `NENTCOC` | Nombre corto de entidad colectiva | `A(25)` | Copia exacta del nombre correspondiente de `UP`. |
| 111-135 | `NENTSIC` | Nombre corto de entidad singular | `A(25)` | Copia exacta de `UP`. |
| 136-160 | `NNUCLEC` | Nombre corto de núcleo/diseminado | `A(25)` | Copia exacta de `UP`. |
| 166-190 | `NVIAC` | Nombre corto de vía | `A(25)` | Copia exacta de `VIAS`; vacío si no hay vía. |
| 196-245 | `DPSVIA` | Descripción de pseudovía | `A(50)` | Copia exacta de `PSEU`; vacío si no hay pseudovía. |

Todos los pares anterior/resultante coinciden en ambos snapshots. En enero de 2026
también coinciden al 100 % los cinco nombres denormalizados con sus tablas de
origen.

## Intervalos de portal

El extremo completo es `EIN+CEIN` o `ESN+CESN`, por ejemplo `0018A`. No debe
compararse sólo la parte numérica si existen calificadores.

- `TINUM=0` usa exactamente `EIN=0000`, `CEIN=S`, `ESN=0000`, `CESN=S` en las
  102.830 filas observadas de enero de 2026.
- `TINUM=1` exige extremos numéricos impares; `TINUM=2`, pares.
- `0000` no significa por sí solo “sin numeración”: también aparece como límite
  inferior de algunos tramos pares. Hay que interpretar el conjunto de cinco
  campos.
- Los calificadores observados incluyen letras, `Ñ` y dígitos. Aunque la norma
  histórica habla de blanco o letra, el validador debe aceptar el dominio físico
  alfanumérico o registrar los casos no normativos.
- La letra `S` no debe interpretarse aislada: aparece también como calificador en
  algunos tramos numerados.

## Clave y referencias

La clave natural comprobada es el bloque de identificación completo de 58
posiciones:

`CPRO, CMUN, DIST, SECC, LSECC, SUBSC, CUN, CVIA, CPSVIA, MANZ, CPOS, TINUM,
EIN, CEIN, ESN, CESN`.

No se encontraron duplicados. Las referencias hacia `UP`, `SECC`, `VIAS` y
`PSEU` resuelven al 100 % cuando el código no es un centinela.

Una fila puede tener sólo vía, sólo pseudovía o ninguna de las dos. No se observó
ninguna con ambas:

| Referencia en enero de 2026 | Filas |
| --- | ---: |
| Sólo `CVIA` | 1.453.038 |
| Sólo `CPSVIA` | 7.084 |
| Ninguna | 67.425 |
| Ambas | 0 |
