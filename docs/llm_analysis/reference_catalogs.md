# Catálogos auxiliares

## Formato físico

Los cuatro CSV usan `;` y tienen cabecera. Son UTF-8, a diferencia de los ficheros
de anchura fija.

| Fichero | Filas | Final de línea | Particularidad |
| --- | ---: | --- | --- |
| `cod_ccaa.csv` | 19 | `LF` | Sin BOM |
| `cod_provincia.csv` | 52 | `LF` | Sin BOM |
| `cod_mun.csv` | 8.132 | `CRLF` | Sin BOM; última fila sin salto final |
| `TiposVia.csv` | 684 | `CRLF` | BOM UTF-8 |

Todas las filas tienen el número de columnas de su cabecera.

## Esquemas territoriales

`cod_ccaa.csv` y `cod_provincia.csv`:

| Columna | Significado | Tipo |
| --- | --- | --- |
| `CODIGO` | Código de dos dígitos | Texto |
| `LITERAL` | Nombre oficial | Texto UTF-8 |

`cod_mun.csv`:

| Columna | Significado | Tipo |
| --- | --- | --- |
| `CODAUTO` | Código de comunidad autónoma | Texto de 2 dígitos |
| `CPRO` | Código de provincia | Texto de 2 dígitos |
| `CMUN` | Código municipal dentro de provincia | Texto de 3 dígitos |
| `DC` | Dígito de control municipal | Texto de 1 dígito |
| `NOMBRE` | Denominación oficial | Texto |

La clave de municipio usada por el callejero es `(CPRO, CMUN)`. `DC` no aparece
en los snapshots y no debe añadirse a sus joins. El INE indica que se asigna
mediante una regla de cálculo para detectar errores, pero las fuentes locales no
publican el algoritmo; conviene conservarlo y contrastarlo, no recalcularlo.

## Integridad territorial

- No hay claves municipales duplicadas.
- Todas las filas municipales referencian una provincia y CCAA existentes.
- Ninguna provincia está asociada a más de una CCAA.
- Los 52 códigos provinciales y los 19 autonómicos tienen uso.
- Los 8.132 municipios coinciden exactamente con las filas municipales de `UP` y
  aparecen en `SECC`.

`cod_mun.csv` es la mejor dimensión de nombres municipales. `UP.NMUN50` sirve para
la jerarquía, pero usa mayúsculas y convenciones editoriales distintas.

## `TiposVia.csv`

| Columna | Significado práctico |
| --- | --- |
| `TIPO_VIA` | Código de tipo descrito por la fila |
| `SINONIMO` | Código considerado equivalente |
| `DESCRIPCION` | Literal asociado a `TIPO_VIA` |
| `COMENTARIO` | Nota excepcional |

El fichero representa una **relación de sinonimia**, no una función simple
`sinónimo -> código canónico`. Por ejemplo, los códigos de calle en distintas
lenguas aparecen relacionados entre sí en muchas combinaciones. Elegir siempre la
primera columna como normalizada puede producir resultados arbitrarios.

Calidad observada:

- 684 filas y 309 códigos en la unión de ambas columnas.
- 678 pares `(TIPO_VIA, SINONIMO)` distintos.
- Dos filas exactas están repetidas (`PSAXE/PSAXE/PASAXE` y
  `RUELA/RUELA/RUELA`).
- Hay cinco pares repetidos con descripciones iguales o contradictorias.
- Faltan 11 relaciones inversas y dos autorrelaciones; no asumir simetría perfecta.
- `.` tiene el comentario “Tipo de vía a extinguir”.
- De los 272 `TVIA` usados en enero de 2026, sólo `GRNJA` y `DISEM` no aparecen
  en ninguna de las dos columnas.

Uso recomendado: tratarlo como grafo de equivalencias con fallback al código
original. Si una aplicación necesita un único nombre canónico, debe definir y
versionar su propia política.
