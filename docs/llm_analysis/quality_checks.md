# Comprobaciones de calidad de los snapshots

Todas las cifras proceden de recorridos completos de julio de 2025 y enero de
2026.

## Estructura y claves

| Fichero | Anchura incorrecta | Campos `N` inválidos | Claves duplicadas |
| --- | ---: | ---: | ---: |
| `VIAS` | 0 | 0 | 0 |
| `PSEU` | 0 | 0 | 0 |
| `TRAM` | 0 | 0 | 0 |
| `UP` | 0 | 0 | 0 |
| `SECC` | 0 | 0 | 0 |

Todas las fechas `FVAR` son válidas y coinciden con la fecha de referencia del
snapshot. Todas las líneas terminan en `CRLF`.

## Integridad referencial

En ambos snapshots:

- cero referencias territoriales fuera de `cod_provincia.csv` o `cod_mun.csv`;
- cero referencias de `TRAM` a una `UP` inexistente;
- cero referencias de `TRAM` a `SECC`, `VIAS` o `PSEU` inexistentes, ignorando
  `00000` donde significa “no aplica”;
- cero padres ausentes en la jerarquía `UP`;
- cero diferencias entre los nombres denormalizados de `TRAM` y sus filas de
  origen.

Esto permite normalizar `TRAM` sin perder nombres y reconstruirlos mediante joins.

## Tramos y portales

En enero de 2026:

| `TINUM` | Significado | Filas |
| --- | --- | ---: |
| `0` | Sin numeración | 102.830 |
| `1` | Impar | 724.923 |
| `2` | Par | 699.794 |

No se observaron:

- `EIN > ESN`;
- extremos pares en tramos impares;
- extremos impares en tramos pares;
- códigos postales vacíos o `00000`;
- `CUN=0000000` en `TRAM`.

Todos los tramos sin numeración usan exactamente `0000S-0000S`. El campo `MANZ`
está vacío en 100 % de las filas y `LSECC` también. `SUBSC` usa blanco o
`01`-`06`.

## Municipio y código postal

La relación es muchos-a-muchos:

- 2.080 de 8.132 municipios tienen más de un código postal.
- 1.963 de 10.795 códigos postales aparecen en más de un municipio.
- Madrid tiene 58 códigos; Murcia, 54; Barcelona, 42.
- `09640` y `42180` aparecen cada uno en 10 municipios.

No modelar `postal_code` como atributo único de municipio.

## Cambios entre snapshots

| Fichero | Altas de clave | Bajas de clave | Misma clave con contenido distinto |
| --- | ---: | ---: | ---: |
| `VIAS` | 5.030 | 2.574 | 16.380 |
| `PSEU` | 3.580 | 89 | 106 |
| `UP` | 102 | 15 | 85 |
| `SECC` | 52 | 8 | 0 |
| `TRAM` | 39.911 | 31.398 | 0 |

En `TRAM`, la clave natural incluye todo el bloque anterior, incluido el intervalo;
por ello un cambio territorial o de rango se expresa como baja y alta, no como
“misma clave modificada”.

## Veredicto

Los snapshots tienen buena integridad estructural y relacional para cargas batch.
Este veredicto no se extiende al bundle de variaciones, cuyas anomalías se
documentan por separado.
