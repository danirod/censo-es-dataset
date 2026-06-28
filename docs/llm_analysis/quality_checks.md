# Comprobaciones de calidad

## Fuentes

- `@upstream/caj_esp_072025/`
- `@upstream/caj_esp_012026/`
- `@upstream/cod_provincia.csv`
- `@upstream/cod_mun.csv`

## Integridad estructural

En ambos snapshots:

- Todas las filas tienen la anchura esperada.
- No se han observado claves duplicadas.
- No se han observado referencias a provincias o municipios fuera de catálogo.

Resumen:

| Fichero | Jul 2025 | Ene 2026 | Duplicadas | Referencias rotas |
| --- | ---: | ---: | ---: | ---: |
| `VIAS` | 903738 | 906194 | 0 | 0 |
| `PSEU` | 97899 | 101390 | 0 | 0 |
| `TRAM` | 1519034 | 1527547 | 0 | 0 |
| `UP` | 154056 | 154143 | 0 | 0 |
| `SECC` | 36626 | 36670 | 0 | 0 |

## Integridad cruzada

En ambos snapshots, `TRAM` referencia correctamente:

- `VIAS`
- `PSEU`
- `SECC`

Resultado observado:

- Referencias rotas a `VIAS`: 0
- Referencias rotas a `PSEU`: 0
- Referencias rotas a `SECC`: 0

## Distribuciones útiles para negocio

### Relación municipio <-> código postal

Snapshot enero 2026:

- Municipios con más de un código postal: 2080 de 8132
- Códigos postales asociados a más de un municipio: 1963 de 10795

Ejemplos:

- `Madrid`: 58 códigos postales
- `Murcia`: 54
- `Barcelona`: 42
- `09640`: compartido por 10 municipios
- `42180`: compartido por 10 municipios

### Tipo de numeración en `TRAM`

Snapshot enero 2026:

- `1` (impar): 724923
- `2` (par): 699794
- `0` (sin numeración): 102830

Esto es útil para construir validación de portales y rangos numéricos.

## Evolución entre snapshots

Comparando julio de 2025 contra enero de 2026:

| Fichero | Altas de clave | Bajas de clave | Cambios con misma clave |
| --- | ---: | ---: | ---: |
| `VIAS` | 5030 | 2574 | 16380 |
| `PSEU` | 3580 | 89 | 106 |
| `UP` | 102 | 15 | 85 |
| `SECC` | 52 | 8 | 0 |
| `TRAM` | 39911 | 31398 | 0 |

Lectura rápida:

- `VIAS` cambia bastante más por renombrados y ajustes que `PSEU` o `UP`.
- `TRAM` es la tabla más volátil, como cabría esperar al mezclar sección, unidad poblacional, vía, código postal y tramos numéricos.

## Conclusión de calidad

Para uso batch y para construcción de datasets derivados, la calidad observada es buena.

Para uso incremental, conviene tratar por separado:

- El snapshot completo, que sí parece muy confiable
- El fichero de variaciones, que necesita validación adicional antes de usarlo como fuente de sincronización exacta
