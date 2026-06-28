# Suposiciones verificadas para futuros validadores

## Objetivo

Esta nota resume tesis prácticas que sí han sido contrastadas sobre los snapshots completos y que son especialmente útiles para diseñar:

- validadores de dirección
- catálogos municipio <-> código postal
- servicios de autocompletado o normalización

## 1. `cod_mun.csv` sí puede actuar como catálogo canónico de municipios

Comprobaciones observadas sobre enero de 2026:

- Las 8132 claves `(CPRO, CMUN)` de `cod_mun.csv` aparecen exactamente una vez como fila municipal en `UP` (`CUN = 0000000`).
- No hay municipios de `UP` fuera de `cod_mun.csv`.
- Las 8132 claves `(CPRO, CMUN)` también aparecen en `SECC`.

Recomendación:

- Usar `cod_mun.csv` como catálogo canónico de municipios.
- Usar `UP` para jerarquía poblacional, no como fuente principal de nombre visible del municipio.

Motivo:

- El nombre municipal de `UP` no coincide literalmente con `cod_mun.csv`.
- Coincidencia exacta `cod_mun.NOMBRE` vs `UP.NMUN50`: `0 / 8132`
- Coincidencia tras aplicar `upper()`: `7533 / 8132`

Las diferencias restantes son sobre todo de estilo editorial:

- mayúsculas
- artículos desplazados a paréntesis, como `Ballestero, El` -> `BALLESTERO (EL)`
- variantes bilingües o puntuación ligeramente distinta

Conclusión práctica:

- Para mostrar nombres al usuario final, `cod_mun.csv` parece más adecuado.
- Para joins internos, basta la clave `(CPRO, CMUN)`.

## 2. `TRAM` tiene invariantes fuertes útiles para validación

Snapshot enero de 2026:

- Filas con sólo `CVIA` informado: 1453038
- Filas con sólo `CPSVIA` informada: 7084
- Filas con `CVIA = 0` y `CPSVIA = 0`: 67425
- Filas con ambos informados a la vez: `0`

Interpretación:

- La relación entre vía y pseudovía en `TRAM` parece prácticamente exclusiva.
- Nunca se observó un tramo con vía y pseudovía simultáneas.
- Sí existen muchos tramos sin ninguna de las dos, sobre todo en contextos rurales o diseminados.

Recomendación:

- No asumir que toda dirección válida tenga `CVIA`.
- Soportar validación por unidad poblacional + código postal + rango numérico incluso cuando no haya vía explícita.

### Perfil de los tramos sin vía ni pseudovía

En enero de 2026 hay `67425` filas de `TRAM` con `CVIA = 0` y `CPSVIA = 0`.

Propiedades observadas:

- Todas pertenecen a `CUN` de tipo núcleo/diseminado; no se observaron municipios ni entidades colectivas en este grupo.
- `55882` de esas filas, aproximadamente el `82.9 %`, están en Galicia (`15`, `27`, `32`, `36`).
- Asturias (`33`) aporta otras `10267`.

Patrón nominal más frecuente:

- entidad colectiva informada
- entidad singular informada
- núcleo `*DISEMINADO*` o nombre de núcleo explícito

Interpretación:

- No parecen filas corruptas ni residuos.
- Representan direccionamiento rural o diseminado donde la unidad poblacional pesa más que la vía.

Consecuencia para producto:

- Un validador no urbano debe poder aceptar direcciones ancladas en entidad singular/núcleo y código postal, sin exigir una calle formal.

## 3. Los rangos numéricos de `TRAM` son coherentes a gran escala

Snapshot enero de 2026:

- `TINUM = 1` (impar): 724923
- `TINUM = 2` (par): 699794
- `TINUM = 0` (sin numeración): 102830

Comprobaciones realizadas:

- No se han visto casos con `EIN > ESN` cuando ambos límites están informados.
- No se han visto incoherencias de paridad:
  - `TINUM = 1` con extremos pares
  - `TINUM = 2` con extremos impares
- No se han visto códigos postales vacíos o a cero en `TRAM`.
- No se han visto filas de `TRAM` con `CUN = 0000000`.

Conclusión práctica:

- `TRAM` sí parece apto para una validación por rango de portal razonablemente estricta.

## 4. `TVIA` cubre casi por completo `TiposVia.csv`, pero no al 100 % limpio

Snapshot enero de 2026:

- Códigos `TVIA` distintos en `VIAS`: 272
- Códigos presentes en `TiposVia.csv` como tipo o sinónimo: 270
- Códigos no cubiertos: 2

Singletons observados:

- `GRNJA`
- `DISEM`

Recomendación:

- `TiposVia.csv` es muy útil como tabla de normalización, pero no conviene tratarla como universo cerrado sin fallback.
- Mantener un mecanismo de "unknown passthrough" para tipos raros o históricos.

## 5. `NVIAC` no debe confundirse con el nombre oficial completo

En `VIAS`:

- `NVIA == NVIAC` en 849794 de 906194 filas
- `NVIA` empieza por `NVIAC` en 876039 filas
- 29662 nombres completos superan 25 caracteres

Ejemplos observados:

- `JOSE DE MADINABEITIA KALEA` -> `JOSE MADINABEITIA KALEA`
- `MONSEÑOR FRANCISCO SAENZ DE URTURI (DE)` -> `MON FCO SAENZ URTURI (DE)`
- `CAMINO SIRISOLO/SIRISOLOBIDEA` -> `CNO SIRISOLO/SIRISOLOBIDE`

Interpretación:

- `NVIAC` funciona como nombre corto, abreviado o truncado.
- No es un identificador canónico equivalente a `NVIA`.

Recomendación:

- Para display o matching exigente, priorizar `NVIA`.
- Para búsqueda tolerante, autocompletado o índices compactos, `NVIAC` sí puede ser útil.

## 6. En `PSEU` no aparece una doble semántica de nombre

En el snapshot de enero de 2026:

- La descripción de identificación y la descripción final coinciden en el 100 % de las filas observadas.

Conclusión práctica:

- `PSEU` parece más simple que `VIAS` a efectos de normalización.
- No hay evidencia de un campo "nombre corto" alternativo con semántica propia.
