# Catálogos auxiliares de referencia

## Fuentes

- `@upstream/cod_ccaa.csv`
- `@upstream/cod_provincia.csv`
- `@upstream/cod_mun.csv`

## Tamaños observados

- `cod_ccaa.csv`: 19 filas
- `cod_provincia.csv`: 52 filas
- `cod_mun.csv`: 8132 filas

## Integridad entre catálogos

Comprobaciones realizadas:

- Todas las filas de `cod_mun.csv` referencian una provincia existente en `cod_provincia.csv`.
- Todas las filas de `cod_mun.csv` referencian una comunidad autónoma existente en `cod_ccaa.csv`.
- Ninguna provincia aparece asociada a más de una comunidad autónoma dentro de `cod_mun.csv`.

Resultado observado:

- Referencias rotas de municipio -> provincia: `0`
- Referencias rotas de municipio -> CCAA: `0`
- Provincias asociadas a más de una CCAA: `0`

## Cobertura

- Los 52 códigos de provincia aparecen usados por al menos un municipio.
- Los 19 códigos de comunidad autónoma aparecen usados por al menos un municipio.
- No hay provincias del snapshot ausentes del catálogo.
- No hay provincias del catálogo ausentes de los snapshots analizados.

## Conclusión práctica

Los tres CSV auxiliares son adecuados como tablas maestras para:

- catálogos jerárquicos CCAA -> provincia -> municipio
- validación temprana de claves territoriales
- enriquecimiento de datasets derivados del callejero

Recomendación:

- Tratar `cod_ccaa.csv` y `cod_provincia.csv` como catálogos de dimensión.
- Tratar `cod_mun.csv` como catálogo canónico de municipios, en combinación con la jerarquía poblacional de `UP`.
