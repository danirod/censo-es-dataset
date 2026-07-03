# Modelo relacional recomendado

Esta propuesta separa una capa **raw**, fiel a los bytes, y una capa **canónica**
para consultas. Evita perder información al mismo tiempo que elimina duplicación.

## Capa raw

Guardar por publicación:

- nombre de fichero;
- fecha de referencia;
- número de línea;
- línea original decodificada como ISO-8859-1;
- campos extraídos sin normalización destructiva.

Esto permite reparsear, comparar publicaciones y explicar cualquier transformación.

## Tablas canónicas

| Tabla | Clave primaria |
| --- | --- |
| `province` | `cpro` |
| `municipality` | `(cpro, cmun)` |
| `population_unit` | `(cpro, cmun, cun)` |
| `census_section` | `(cpro, cmun, dist, secc, lsecc)` |
| `road` | `(cpro, cmun, cvia)` |
| `pseudo_road` | `(cpro, cmun, cpsvia)` |
| `segment` | Los 16 campos del bloque identificador de `TRAM` |

La clave de `segment` es:

`cpro, cmun, dist, secc, lsecc, subsc, cun, cvia, cpsvia, manz, cpos, tinum,
ein, cein, esn, cesn`.

En SQLite, todos los componentes de una clave deben declararse `NOT NULL`; los
blancos físicos pueden representarse como `''`. Usar `NULL` dentro de una clave
compuesta permite comportamientos de unicidad no deseados.

## Tipos

- Códigos territoriales, postales y de vía: `TEXT` con longitud fija.
- Nombres: `TEXT`, sin cambiar mayúsculas, tildes ni puntuación en la columna
  fuente.
- `FVAR`: `TEXT(8)` raw y, opcionalmente, una columna `DATE` derivada.
- `EIN` y `ESN`: conservar `TEXT(4)` y añadir enteros derivados para rangos.
- Calificadores: `TEXT(1)`.

No usar `INTEGER` para códigos con ceros iniciales.

## Claves foráneas

- `population_unit.(cpro,cmun)` -> `municipality`.
- `road` y `pseudo_road` -> `municipality`.
- `census_section` -> `municipality`.
- `segment.(cpro,cmun,cun)` -> `population_unit`.
- `segment.(cpro,cmun,dist,secc,lsecc)` -> `census_section`.

Para vía y pseudovía, resulta más limpio convertir el centinela `00000` a una
referencia canónica nullable y conservar el código raw aparte. Así pueden
declararse FKs normales y una restricción:

```sql
CHECK (road_id IS NULL OR pseudo_road_id IS NULL)
```

No se debe exigir que una de las dos exista: hay tramos rurales sin ambas.

## Datos que pueden normalizarse

Los campos `NENTCOC`, `NENTSIC`, `NNUCLEC`, `NVIAC` y `DPSVIA` de `TRAM` son
copias exactas de sus tablas de origen en enero de 2026. Pueden omitirse de la
tabla canónica y recuperarse mediante joins, manteniéndolos en raw para detectar
divergencias futuras.

Los campos anterior/resultante duplicados en snapshots también pueden reducirse a
una sola copia canónica.

## Código postal

No crear `municipality.postal_code`. La relación se deriva de los tramos y es
muchos-a-muchos. Si se materializa para rendimiento, usar:

```text
municipality_postal_code(cpro, cmun, cpos)
```

con clave primaria en las tres columnas y procedencia trazable hasta `segment`.

## Actualización

La estrategia segura es cargar cada snapshot en staging, validar y sustituir la
versión canónica dentro de una transacción. No aplicar todavía
`Var_Callejero_*` como log transaccional: tiene cobertura parcial y anomalías
documentadas en [variaciones](./variation_files.md).
