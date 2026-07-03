# Modelo conceptual del callejero

## Qué representa cada fichero

| Fichero | Entidad |
| --- | --- |
| `UP` | Jerarquía estadística de asentamientos dentro de un municipio. |
| `SECC` | División electoral del municipio en distrito y sección. |
| `VIAS` | Vías lógicas codificadas dentro de un municipio. |
| `PSEU` | Agrupaciones de dirección que sustituyen o complementan conceptualmente una vía. |
| `TRAM` | Unión entre territorio, unidad poblacional, vía/pseudovía, código postal y rango de portal. |

## Relaciones

```text
Provincia
└── Municipio
    ├── Unidad poblacional (UP)
    │   └── colectiva? -> singular -> núcleo o diseminado
    ├── Distrito -> Sección (SECC)
    ├── Vía (VIAS)
    ├── Pseudovía (PSEU)
    └── Tramo (TRAM)
        ├── una UP
        ├── una sección
        ├── como máximo una vía o pseudovía
        ├── un código postal
        └── un intervalo par, impar o sin numeración
```

La entidad colectiva es opcional. La entidad singular es el nivel territorial
estable bajo el municipio; cada núcleo o diseminado pertenece a una singular.

## Significado de los niveles de `UP`

- **Entidad colectiva:** agrupación histórica de entidades singulares presente
  sólo en algunas regiones, por ejemplo parroquias, concejos o diputaciones.
- **Entidad singular:** área habitable diferenciada dentro del municipio y
  reconocida por un nombre inequívoco.
- **Núcleo:** asentamiento concentrado que cumple los criterios estadísticos del
  INE.
- **Diseminado:** viviendas de una entidad singular que no pertenecen a un núcleo.

Son divisiones estadísticas; no deben confundirse automáticamente con entidades
locales administrativas.

## Papel central de `TRAM`

`TRAM` es la tabla puente del dataset. No contiene una dirección individual, sino
un intervalo de posibles portales que comparten contexto territorial. Es la fuente
para responder preguntas como:

- qué códigos postales aparecen en un municipio;
- en qué sección cae un intervalo de una vía;
- si un portal par o impar es compatible con un tramo;
- qué direcciones rurales existen sin una vía formal.

Los nombres incluidos en `TRAM` están denormalizados para facilitar consumo. En
enero de 2026 coinciden exactamente con `UP`, `VIAS` o `PSEU`; los códigos son las
referencias estables para joins.

## Cardinalidades que no deben simplificarse

- Municipio y código postal forman una relación muchos-a-muchos.
- Una vía puede tener muchos tramos, secciones y códigos postales.
- Una unidad poblacional contiene muchos tramos.
- No todo tramo tiene vía: 67.425 filas de enero de 2026 no tienen `CVIA` ni
  `CPSVIA`.
- En los datos analizados, vía y pseudovía son alternativas excluyentes, aunque la
  definición histórica permite que una pseudovía complemente conceptualmente una
  vía.

## Snapshot frente a eventos

Los directorios `caj_esp_*` son estados completos a una fecha. Los ficheros
`Var_Callejero_*` son notificaciones de operaciones. Comparten nombres de campos y
estructura de intercambio, pero no la misma semántica:

- un snapshot se reemplaza completo;
- una variación tiene estado anterior, operación y estado resultante;
- el bundle observado no reconstruye por sí solo el siguiente snapshot.
