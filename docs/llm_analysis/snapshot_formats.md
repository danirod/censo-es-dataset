# Formato físico de los snapshots

## Propiedades comunes

| Propiedad | Valor observado |
| --- | --- |
| Codificación | `ISO-8859-1` |
| Final de línea | `CRLF` |
| Cabecera | Ninguna |
| Separador | Ninguno; posiciones fijas |
| Relleno alfanumérico | Espacios a la derecha |
| Registros de longitud incorrecta | 0 en ambos snapshots |

No abrir estos ficheros como UTF-8. Al leer en modo texto, el terminador no forma
parte de la anchura indicada.

## Ficheros

| Fichero | Anchura | Filas julio 2025 | Filas enero 2026 | Diccionario |
| --- | ---: | ---: | ---: | --- |
| `VIAS` | 132 | 903.738 | 906.194 | [Vías y pseudovías](./fields_vias_pseu.md) |
| `PSEU` | 127 | 97.899 | 101.390 | [Vías y pseudovías](./fields_vias_pseu.md) |
| `TRAM` | 273 | 1.519.034 | 1.527.547 | [Tramos](./fields_tram.md) |
| `UP` | 604 | 154.056 | 154.143 | [Unidades y secciones](./fields_up_secc.md) |
| `SECC` | 11 | 36.626 | 36.670 | [Unidades y secciones](./fields_up_secc.md) |

## Cómo cortar campos

Las posiciones de la documentación son inclusivas y empiezan en 1. En lenguajes
con slices de inicio inclusivo y fin exclusivo:

```text
posición INE 1-2  -> slice [0:2]
posición INE 6-10 -> slice [5:10]
```

Primero se elimina sólo `\r\n`; después se comprueba la longitud y por último se
extraen campos. Aplicar `strip()` a toda la línea destruiría los espacios del
último campo y ocultaría registros truncados.

## Controles que debe hacer un parser

1. Rechazar o apartar líneas cuya anchura no sea la esperada.
2. Validar que cada campo `N` contiene exactamente tantos dígitos como posiciones.
3. Decodificar antes de recortar los campos `A`.
4. Preservar los códigos como texto.
5. Validar `FVAR` como `AAAAMMDD`.
6. Conservar la línea y el número de línea para trazabilidad.

En los dos snapshots analizados no hay infracciones de anchura ni campos `N` con
espacios o caracteres no numéricos.

## Semántica de snapshot

Todos los registros de una publicación comparten `FVAR`, que coincide con su fecha
de referencia. `TIPOINF`, `CDEV` y `CVAR` están vacíos. Los bloques anterior y
resultante coinciden exactamente: no deben interpretarse como dos versiones
temporales dentro del snapshot.

Las discrepancias entre fuentes y la interpretación prudente de los nombres de
fichero están en [fuentes y alcance](./sources_and_scope.md).
