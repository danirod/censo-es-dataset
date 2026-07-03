# Auditoría de cierre

## Objetivo

Mejorar la documentación de `docs/llm_analysis` mediante contraste completo con
los snapshots, los ficheros de variaciones, los CSV, el XLSX y los PDF, manteniendo
varios documentos breves y útiles para humanos y modelos de razonamiento inferior.

El cierre exige dos auditorías consecutivas que no encuentren mejoras pendientes.

## Requisitos y evidencia

| Requisito | Evidencia |
| --- | --- |
| Analizar toda la documentación previa | Inventario y lectura de todos los Markdown; índice final en `overview.md`. |
| Contrastar los dos snapshots completos | 2.711.353 y 2.725.944 filas recorridas, respectivamente, con anchuras, tipos, claves, dominios y relaciones comprobados. |
| Contrastar el bundle completo | 54.654 filas recorridas; layouts, operaciones, duplicados, payloads y replay analizados. |
| Contrastar XLSX y PDF | Cinco hojas del Excel extraídas; ambos PDF leídos y sus tablas críticas renderizadas visualmente. |
| Contrastar CSV auxiliares | Encodings, esquemas, cardinalidades, integridad y calidad de `TiposVia.csv` comprobados. |
| Aclarar formato y semántica | Diccionarios separados para `VIAS/PSEU`, `TRAM`, `UP/SECC` y variaciones. |
| Facilitar uso humano y por LLM | Modelo conceptual, guía de lectura, reglas de validación y modelo relacional explícitos. |
| Mantener archivos cortos | Ningún documento funcional supera 130 líneas; cada uno tiene una responsabilidad. |
| Distinguir certeza | `sources_and_scope.md` fija prioridad y separa dato oficial, observación e inferencia. |

## Correcciones materiales realizadas

- `FVAR` de snapshot documentado como fecha de referencia común.
- `CUN` explicado como `CCSSDNN`, con método ABC y `NN=99` para diseminado.
- `0000S-0000S` y los calificadores de portal explicados sin simplificaciones
  incorrectas.
- Discrepancias de `SECC`, vector de errores, `POS` y ceros/blancos explicitadas.
- Nombres denormalizados de `TRAM` verificados contra sus tablas de origen.
- `TiposVia.csv` reclasificado como relación de sinonimia imperfecta.
- `NSEC` descartado como clave u orden total.
- Duplicados exactos y modificaciones sin cambio de `TRAM` cuantificados.
- Replay de variaciones reproducido y sus conflictos cuantificados.
- Recomendaciones de SQLite corregidas para códigos, claves vacías y FKs.

## Historial de iteraciones

### Iteración de mejora

La primera revisión encontró documentación duplicada, un cierre obsoleto, ausencia
de layouts de variaciones y varios dominios o caveats no documentados. Se
reorganizó y amplió el conjunto; por tanto, esta iteración no cuenta como auditoría
sin cambios.

### Auditorías finales

La primera tentativa encontró finales de fichero no canónicos mediante
`git diff --check`; se corrigieron y se reinició el contador.

1. **Primera pasada limpia:** fuentes, cifras, layouts, enlaces, tablas, longitudes
   y `git diff --check` revalidados sin mejoras pendientes.
2. **Segunda pasada limpia:** revisión adversarial desde `overview.md`, cobertura de
   preguntas de parseo/semántica/joins/SQLite/validación/replay, búsqueda de
   contradicciones y comprobación final del diff; ninguna mejora pendiente.

Se cumple el criterio de dos auditorías consecutivas sin cambios materiales.
