# Callejero del Censo Electoral: guía de lectura

## Veredicto

Los snapshots nacionales de julio de 2025 y enero de 2026 son estructural y
referencialmente sólidos para construir datasets derivados:

- cero registros de anchura incorrecta;
- cero claves duplicadas;
- cero campos numéricos físicamente inválidos;
- cero referencias rotas entre `TRAM`, `UP`, `SECC`, `VIAS` y `PSEU`;
- cero padres ausentes en la jerarquía poblacional.

El bundle de variaciones no merece el mismo nivel de confianza como mecanismo de
sincronización: no reconstruye el snapshot siguiente, repite líneas de `TRAM` y
contiene modificaciones sin cambio visible.

## Mapa documental

| Pregunta | Documento |
| --- | --- |
| ¿Qué fuentes y versiones se analizaron? | [Fuentes y alcance](./sources_and_scope.md) |
| ¿Cómo se relacionan los cinco ficheros? | [Modelo conceptual](./conceptual_model.md) |
| ¿Cómo se leen físicamente? | [Formato de snapshots](./snapshot_formats.md) |
| ¿Qué significan tipos y campos comunes? | [Convenciones del diccionario](./data_dictionary.md) |
| ¿Qué significa cada campo de `VIAS`/`PSEU`? | [Vías y pseudovías](./fields_vias_pseu.md) |
| ¿Qué significa cada campo de `TRAM`? | [Tramos](./fields_tram.md) |
| ¿Cómo funcionan `UP`, `CUN` y `SECC`? | [Unidades y secciones](./fields_up_secc.md) |
| ¿Qué calidad tienen los snapshots? | [Comprobaciones](./quality_checks.md) |
| ¿Cómo son los CSV auxiliares? | [Catálogos](./reference_catalogs.md) |
| ¿Cómo se carga en una base de datos? | [Modelo relacional](./relational_model.md) |
| ¿Qué reglas usar en un validador? | [Suposiciones de validación](./validator_assumptions.md) |
| ¿Cuál es el layout de variaciones? | [Layout de variaciones](./variation_layouts.md) |
| ¿Se pueden reproducir snapshots con ellas? | [Análisis de variaciones](./variation_files.md) |

## Cinco ideas que evitan errores

1. Los códigos son texto con ceros iniciales, aunque el INE los marque `N`.
2. `FVAR` es fecha común de referencia en un snapshot, no última modificación de
   cada fila.
3. `TRAM` es la tabla puente y una vía no es obligatoria en entornos rurales.
4. Municipio y código postal forman una relación muchos-a-muchos.
5. Para estado productivo debe cargarse el snapshot completo; las variaciones son
   una señal parcial.

## Caveats de fuente

- `SECC` mide 11 caracteres reales aunque el Excel sólo enumere 10.
- El vector de errores de 20 posiciones del PDF de 2009 no forma parte de los
  ficheros publicados.
- El PDF de variaciones contiene una errata de seis ceros para un `CUN` de siete.
- `NSEC` no proporciona el orden total que su descripción podría sugerir.
- Las regularidades observadas en dos publicaciones deben revalidarse al cargar
  una tercera.
