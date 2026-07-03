# Variaciones julio 2025 -> enero 2026

El layout campo a campo está en [variation_layouts.md](./variation_layouts.md).
Este documento evalúa comportamiento y fiabilidad.

## Operaciones

| Código | Significado | `UP` | `VIAS`/`PSEU` | `TRAM` |
| --- | --- | :---: | :---: | :---: |
| `A` | Alta | Sí | Sí | Sí |
| `B` | Baja | Sí | Sí | Sí |
| `M` | Modificación | Sí | Sí | Sí |
| `R` | Recodificación | No | Sí | No |
| `F` | Fusión | No | No | Permitida |
| `S` | Segregación | No | No | Permitida |

No aparecen `F` ni `S` en el bundle analizado. Todas las operaciones observadas
pertenecen al dominio permitido de su fichero.

## Estructura observada

| Fichero | Anchura | Filas | A | B | M | R |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `VIAS` | 112 | 10.487 | 2.747 | 2.171 | 5.519 | 50 |
| `PSEU` | 81 | 2.160 | 1.996 | 14 | 49 | 101 |
| `TRAM` | 127 | 41.958 | 8.168 | 12.030 | 21.760 | 0 |
| `UP` | 608 | 49 | 20 | 13 | 16 | 0 |

Todas las filas tienen anchura exacta, `CRLF`, campos de fecha válidos y
`TIPOINF/CDEV` vacíos.

El periodo interno va de `20250701` a `20251230`; en `UP` termina el
`20251217`. Que el nombre llegue a `A251231` no implica que deba existir una
operación el último día.

## Payload por operación

El bundle cumple sistemáticamente:

- `A`: identificación ausente mediante ceros/espacios y resultado informado;
- `B`: identificación informada y resultado a ceros/espacios;
- `M`: ambos bloques informados;
- `R`: código anterior y nuevo informados y distintos.

`UP` sólo tiene un `CUN`, que siempre se informa; en bajas deja vacío el bloque de
nombres. En `VIAS`, `POS` vale `0` siempre aunque el PDF diga que irá vacío.

## `NSEC` no es una clave ni un orden total

El PDF lo describe como secuencia para ordenar cambios de una misma fecha. En este
bundle:

- `VIAS`: 10.438 de 10.487 filas usan `0001`;
- `PSEU`: 2.142 de 2.160 usan `0001`;
- `TRAM`: 41.926 de 41.958 usan `0001`;
- `UP`: las 49 usan `0001`;
- se repiten masivamente pares `(FVAR, NSEC)`;
- el orden físico no es cronológico.

Conclusión: conservar `NSEC`, pero no imponer `UNIQUE(FVAR,NSEC)` ni usarlo como
orden global. Si se necesita reproducción determinista, ordenar por `FVAR`,
`NSEC`, fichero, clave y número de línea, dejando claro que los empates no tienen
precedencia oficial demostrada.

## Anomalías de `TRAM`

`TRAM` contiene 3.246 repeticiones exactas por encima de la primera copia:

| Operación | Copias adicionales idénticas |
| --- | ---: |
| `A` | 87 |
| `B` | 1.495 |
| `M` | 1.664 |

Hay 1.646 líneas distintas repetidas; una aparece 34 veces. Los otros tres
ficheros no tienen duplicados exactos.

Además, 738 filas `M` (717 distintas tras deduplicar) tienen bloques anterior y
resultante idénticos. No describen un cambio visible en los campos publicados.

Para replay:

1. preservar el fichero raw;
2. deduplicar líneas exactas en la capa de aplicación;
3. registrar `M` sin cambio como evento no operativo, no como error fatal;
4. no usar el conteo bruto de eventos como conteo de cambios únicos.

## Cobertura respecto al siguiente snapshot

Un replay simple sobre julio de 2025 no reconstruye enero de 2026. Tras aplicar
las operaciones en orden `FVAR`, `NSEC` y posición original, al estado resultante
le faltan o le sobran estas claves respecto al objetivo:

| Fichero | Faltan en replay | Sobran en replay | Misma clave, contenido distinto |
| --- | ---: | ---: | ---: |
| `VIAS` | 2.384 | 532 | 11.188 |
| `PSEU` | 1.639 | 151 | 86 |
| `UP` | 81 | 2 | 104 |
| `TRAM` | 33.855 | 50.850 | 0 |

En `TRAM`, 10.553 bajas y 20.676 modificaciones apuntan a una clave anterior que
no existe en el snapshot de julio; 156 altas ya existían. En los otros ficheros
estos conflictos son mucho menores. Esto descarta que el problema sea sólo el
orden de eventos o los duplicados exactos.

Comparación de señal útil:

- `UP`: 20 altas, 13 bajas y 14 modificaciones del bundle sí corresponden a
  cambios reales, pero el delta total es mayor.
- `VIAS`: 2.589 altas `A` y 2.155 bajas `B` se alinean con el delta, frente a
  5.030 altas y 2.574 bajas reales.
- `PSEU`: 1.864 altas `A` y sólo 4 bajas `B` se alinean, frente a 3.580 altas y
  89 bajas reales.
- `TRAM`: incluso usando la clave lógica, sólo 2.010 altas y 1.416 bajas encajan
  con 36.317 altas y 27.874 bajas reales; unas 560 `M` se parecen a baja+alta.

## Conclusión

El bundle tiene estructura interpretable y señal real, pero no es un log
transaccional exhaustivo. Sirve para auditoría y pistas de cambio. La fuente segura
para estado productivo sigue siendo el snapshot completo.
