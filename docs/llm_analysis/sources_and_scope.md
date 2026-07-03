# Fuentes, versiones y alcance

## Datos analizados

| Familia | Fecha de referencia | Directorio |
| --- | --- | --- |
| Snapshot nacional julio 2025 | 30-06-2025 | `upstream/caj_esp_072025/` |
| Snapshot nacional enero 2026 | 31-12-2025 | `upstream/caj_esp_012026/` |
| Variaciones entre ambos | 01-07-2025 a 31-12-2025 | `upstream/Var_Callejero_0725_0126/` |

El análisis empírico se hizo sobre todas las filas, no sobre muestras. Las cifras
que describen dominios o integridad pertenecen a estos dos snapshots y no deben
convertirse en reglas eternas sin volver a validarlas en futuras publicaciones.

## Documentación local

| Fuente | Qué aporta | Limitaciones |
| --- | --- | --- |
| `upstream/Dis_nuevo.xlsx` | Layout de los cinco snapshots desde julio de 2025 | Omite la posición 11 (`LSECC`) del `SECC` real. |
| `upstream/dis_registro.pdf` | Diseño de 2009 para vías y pseudovías y contexto del cambio | Nombra algunos campos de otra forma y conserva un vector de errores pendiente que no existe en los datos. |
| `upstream/Variacionesencallejero.pdf` | Layout y semántica oficial de las variaciones | Algunas prescripciones no coinciden literalmente con el bundle observado. |
| CSV auxiliares | Catálogos territorial y de tipos de vía | Tienen encoding y calidad propios; véase [catálogos](./reference_catalogs.md). |

El vector de errores `A(20)` del PDF de 2009 no aparece en `Dis_nuevo.xlsx` ni en
los snapshots. Añadirlo produciría anchuras incorrectas de 152 para `VIAS` y 147
para `PSEU`; las anchuras reales son 132 y 127.

## Contexto oficial

La [página de Datos Abiertos del INE](https://www.ine.es/dyngs/DAB/index.htm?cid=1390)
confirma:

- publicación semestral, con referencia 30 de junio y 31 de diciembre;
- disponibilidad de ficheros nacionales y provinciales;
- aplicación del diseño acordado en 2009 desde julio de 2025;
- cambio metodológico del tramero desde 2021: los intervalos se forman agregando
  aproximaciones postales hasta portal, no rellenando por defecto `0001-9999`;
- publicación de un bundle de variaciones junto a cada snapshot.

Para conceptos de unidad poblacional se usa la
[metodología del Nomenclátor](https://www.ine.es/nomenclator/metodologia.htm).
Para la estructura histórica de intercambio y el método ABC se usa la
[Resolución de 1997](https://idapadron.ine.es/repositorio/legislacion/a1111.htm).

## Prioridad cuando las fuentes discrepan

1. Bytes reales de la publicación analizada.
2. `Dis_nuevo.xlsx`, por ser el diseño aplicable desde julio de 2025.
3. PDF específico de variaciones, para esos ficheros.
4. Diseño histórico, para semántica no repetida en fuentes recientes.

La documentación distingue **oficial/documentado**, **observado** e **inferencia**.
Una regularidad observada, como `LSECC` siempre vacío, no se declara dominio
cerrado.

## Nombres de fichero

Ejemplo snapshot: `TRAM.D251231.G260303`.

- `D251231` coincide con la fecha de referencia `2025-12-31` y con `FVAR`.
- `G260303` parece identificar una fecha posterior de generación, `2026-03-03`.

Ejemplo de variaciones: `TRAM.D250701.A251231`.

- Los sufijos delimitan el periodo observado, de 01-07-2025 a 31-12-2025.

La expansión de fechas está respaldada por su coincidencia con los datos. El
significado literal de las letras `D`, `G` y `A` no está definido en los documentos
locales y debe tratarse como inferencia, no como contrato.
