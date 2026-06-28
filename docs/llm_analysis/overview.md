# Callejero INE: resumen ejecutivo

## Alcance

Este análisis cubre:

- Los snapshots principales de `@upstream/caj_esp_072025/` y `@upstream/caj_esp_012026/`
- Los ficheros de variaciones de `@upstream/Var_Callejero_0725_0126/`
- La documentación oficial local: `@upstream/dis_registro.pdf`, `@upstream/Dis_nuevo.xlsx` y `@upstream/Variacionesencallejero.pdf`
- Las tablas de referencia `@upstream/cod_provincia.csv` y `@upstream/cod_mun.csv`

## Veredicto corto

Los snapshots principales del callejero tienen buena pinta para construir datasets derivados y validadores:

- Todos los registros observados tienen longitud fija exacta y estable.
- La codificación observada es `ISO-8859-1` con finales de línea `CRLF`.
- No se han encontrado claves duplicadas en `VIAS`, `PSEU`, `TRAM`, `UP` ni `SECC`.
- No se han encontrado referencias rotas a provincia o municipio respecto a `cod_provincia.csv` y `cod_mun.csv`.
- En `TRAM`, todas las referencias a `VIAS`, `PSEU` y `SECC` resuelven correctamente dentro del mismo snapshot.

Conclusión práctica: los snapshots parecen de calidad aceptable para generar datasets limpios, siempre que la capa de consumo trate bien la jerarquía de `UP`, los nombres con tildes y las relaciones M..N entre municipio y código postal.

## Caveats importantes

### 1. El fichero de variaciones no parece un diff trivial aplicable sin más

Estructuralmente los ficheros de variaciones son consistentes: anchura fija, fechas razonables y códigos de variación esperables.

Pero un replay ingenuo de `Var_Callejero_0725_0126/` sobre el snapshot de julio de 2025 no reconstruye exactamente el snapshot de enero de 2026. En pruebas rápidas quedan diferencias residuales relevantes, por ejemplo:

- `VIAS`: 2384 claves añadidas, 532 eliminadas y 11188 modificadas tras el replay ingenuo
- `PSEU`: 1639 añadidas, 151 eliminadas y 86 modificadas
- `UP`: 81 añadidas, 2 eliminadas y 104 modificadas

Esto no demuestra que el fichero esté mal, pero sí que no debe tratarse todavía como un log transaccional "plug and play". Puede requerir reglas adicionales de negocio o tener semántica más sutil de la que parece a primera vista.

### 2. `UP` no rellena todos los campos nominales en todos los niveles

El diseño sugiere muchos campos de nombre, pero el uso real depende del nivel jerárquico:

- En filas de municipio, el nombre aparece en `NMUN50`; `NMUN` y `NMUNC` están vacíos en la práctica.
- En entidad colectiva se rellenan `NENTCO`, `NENTCO50` y `NENTCOC`.
- En entidad singular se rellena siempre `NENTSI*`, y `NENTCO*` sólo cuando aplica.
- En núcleo/diseminado se rellena siempre `NNUCLE*`.

Conclusión práctica: no conviene modelar `UP` como una tabla plana donde todos los campos de nombre sean equivalentes.

### 3. El código postal es claramente una relación M..N

En el snapshot de enero de 2026:

- 2080 municipios tienen más de un código postal.
- 1963 códigos postales aparecen asociados a más de un municipio.

Ejemplos observados:

- `Madrid` tiene 58 códigos postales.
- `Murcia` tiene 54.
- El código postal `09640` aparece en 10 municipios.

Esto valida una de las hipótesis del proyecto: no debe usarse un modelo 1..1 entre municipio y código postal.

## Siguiente uso recomendado

Orden sugerido para reutilizar esta información:

1. Leer [snapshot_formats.md](/Users/danirod/code/censo-es-dataset/docs/llm_analysis/snapshot_formats.md)
2. Consultar [data_dictionary.md](/Users/danirod/code/censo-es-dataset/docs/llm_analysis/data_dictionary.md) para el significado, tipo y dominio de cada campo
3. Leer [quality_checks.md](/Users/danirod/code/censo-es-dataset/docs/llm_analysis/quality_checks.md)
4. Leer [reference_catalogs.md](/Users/danirod/code/censo-es-dataset/docs/llm_analysis/reference_catalogs.md) para catálogos CCAA/provincia/municipio
5. Leer [validator_assumptions.md](/Users/danirod/code/censo-es-dataset/docs/llm_analysis/validator_assumptions.md) si se van a construir validadores o servicios
6. Leer [variation_files.md](/Users/danirod/code/censo-es-dataset/docs/llm_analysis/variation_files.md) antes de diseñar sincronización incremental
7. Leer [completion_audit.md](/Users/danirod/code/censo-es-dataset/docs/llm_analysis/completion_audit.md) si se quiere revisar el cierre requisito por requisito
