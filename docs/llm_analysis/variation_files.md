# Ficheros de variaciones 072025 -> 012026

## Fuentes

- Documento: `@upstream/Variacionesencallejero.pdf`
- Datos: `@upstream/Var_Callejero_0725_0126/`

## Qué documenta el PDF

El PDF define un mecanismo de notificación entre dos fechas basado en:

- `FVAR`: fecha de variación
- `NSEC`: secuencia dentro de la fecha
- `CVAR`: código de operación

Códigos documentados:

- `A`: alta
- `B`: baja
- `M`: modificación
- `R`: recodificación
- `F`: fusión, sólo tramero
- `S`: segregación, sólo tramero

## Anchuras observadas

| Fichero | Anchura observada |
| --- | ---: |
| `VIAS` | 112 |
| `PSEU` | 81 |
| `TRAM` | 127 |
| `UP` | 608 |

Todas las filas observadas cumplen exactamente la anchura esperada.

## Rango temporal observado

En el bundle `0725 -> 0126`:

- Inicio observado: `20250701`
- Fin observado: `20251230`
- En `UP`, el último `FVAR` observado es `20251217`

Esto encaja con la idea de notificar cambios posteriores al snapshot de junio de 2025 y previos al de diciembre de 2025.

## Distribución de operaciones

| Fichero | A | B | M | R | F | S |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `VIAS` | 2747 | 2171 | 5519 | 50 | 0 | 0 |
| `PSEU` | 1996 | 14 | 49 | 101 | 0 | 0 |
| `TRAM` | 8168 | 12030 | 21760 | 0 | 0 | 0 |
| `UP` | 20 | 13 | 16 | 0 | 0 | 0 |

## Comportamiento observado

- `TIPOINF` y `CDEV` van siempre vacíos en los registros observados.
- En `VIAS`, el campo `POS` no aparece vacío en la práctica; viene informado sistemáticamente, normalmente con `0`, aunque el PDF lo describe como prescindible.
- El bundle parece internamente bien formado.
- No se han visto longitudes anómalas.

## Caveat principal

Un replay ingenuo del bundle sobre el snapshot `caj_esp_072025` no reconstruye exactamente `caj_esp_012026`.

Diferencias residuales tras un replay simple:

- `VIAS`: 2384 claves añadidas, 532 eliminadas, 11188 modificadas
- `PSEU`: 1639 añadidas, 151 eliminadas, 86 modificadas
- `UP`: 81 añadidas, 2 eliminadas, 104 modificadas

Interpretación prudente:

- El bundle no debe usarse aún como diff exacto sin investigación adicional.
- Puede faltar lógica de aplicación.
- Puede haber reglas especiales para `M` y `R`.
- Puede haber diferencias de semántica entre "snapshot de estado" y "notificación de cambios".

## Qué sí parece explicar y qué no

La situación no es uniforme por familia de fichero.

### `UP`

Es el caso que mejor encaja:

- Delta real entre snapshots: `102` altas, `15` bajas, `85` cambios con misma clave
- Bundle de variaciones:
  - `A`: `20` claves que realmente aparecen como altas
  - `B`: `13` claves que realmente aparecen como bajas
  - `M`: `14` claves que realmente cambian

Conclusión:

- El bundle de `UP` apunta a cambios reales y tiene señal útil.
- Aun así, su cobertura es incompleta respecto al delta total.

### `VIAS` y `PSEU`

Tienen señal intermedia:

- En `VIAS`, muchas `M` y `A` sí aterrizan sobre claves que cambian o aparecen en el snapshot final.
- En `PSEU`, las `R` parecen especialmente informativas, porque varias recodificaciones sí coinciden con altas y bajas reales.

Pero la cobertura sigue siendo claramente parcial:

- `VIAS`: delta real de `5030` altas y `2574` bajas, frente a `2589` altas de `A` bien alineadas y `2155` bajas de `B` bien alineadas
- `PSEU`: delta real de `3580` altas y `89` bajas, frente a `1864` altas de `A` bien alineadas y sólo `4` bajas de `B` bien alineadas

Conclusión:

- El bundle de `VIAS` y `PSEU` parece útil como pista de cambios, pero no como reconstrucción exhaustiva del estado.

### `TRAM`

Es el caso más débil.

Incluso reduciendo la comparación a la clave lógica del tramo:

- Delta real entre snapshots: `36317` altas y `27874` bajas
- Bundle de variaciones:
  - `A` que encajan con altas reales: `2010`
  - `B` que encajan con bajas reales: `1416`
  - `M` que parecen actuar como baja+alta real: del orden de `~560`

Conclusión:

- En `TRAM`, la cobertura del bundle es demasiado baja como para usarlo como diff fiable del snapshot.
- Para consumo productivo, el snapshot completo sigue siendo la base segura.

## Recomendación

Usar estos ficheros así:

- Sí: auditoría, análisis forense, pistas para sincronización incremental
- No todavía: reconstrucción exacta de snapshots sin pruebas adicionales y reglas de negocio explícitas
