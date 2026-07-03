# Reglas para validadores y productos

Estas reglas separan contratos seguros de regularidades observadas. Las segundas
deben medirse de nuevo al incorporar otra publicación.

## Reglas seguras

### Identificadores

- Tratar todos los códigos como texto y conservar ceros iniciales.
- Municipio se identifica por `(CPRO, CMUN)`.
- Vía y pseudovía añaden `CVIA` o `CPSVIA`.
- Unidad poblacional añade `CUN`, incluido su dígito de control.
- No unir por nombres.

### Portales

- Seleccionar primero municipio, unidad, vía/pseudovía y código postal.
- Aplicar `TINUM`: `1` admite números impares; `2`, pares; `0`, sin número.
- Comparar extremos completos `NNNNA`, no sólo el entero, cuando haya
  calificadores.
- Interpretar `0000S-0000S` como sin numeración sólo junto con `TINUM=0`.
- No rechazar calificadores numéricos o `Ñ`: existen en los datos.

### Vía opcional

No exigir calle formal. En enero de 2026 hay 67.425 tramos con
`CVIA=CPSVIA=00000`; todos pertenecen a núcleos/diseminados. El 82,9 % está en
Galicia y otros 10.267 en Asturias. Son direccionamiento rural válido, no residuos.

### Código postal

- Un municipio puede tener muchos códigos postales.
- Un código postal puede cruzar municipios.
- Validar la asociación a través de `TRAM`, no mediante prefijos ni una columna
  única en municipio.

## Nombres

### Municipio

`cod_mun.NOMBRE` es preferible para presentación:

- sus 8.132 claves coinciden con `UP` y `SECC`;
- `UP.NMUN50` está en mayúsculas y usa otras convenciones;
- sólo 7.533 nombres coinciden después de aplicar `upper()`.

Las diferencias restantes incluyen artículos desplazados, variantes bilingües y
puntuación. No son fallos de integridad.

### Vía

En enero de 2026:

- `NVIA == NVIAC` en 849.794 de 906.194 filas;
- `NVIA` empieza por `NVIAC` en 876.039;
- 29.662 nombres completos superan 25 caracteres.

`NVIAC` puede abreviar, omitir partículas o truncar. Usar `NVIA` para presentar y
`NVIAC` como señal adicional de búsqueda, nunca como sustituto canónico.

### Pseudovía

`NPSVIA` y `DPSVIA` coinciden en 100 % de ambos snapshots. Puede conservarse una
copia en la capa canónica.

### Tipos de vía

`TiposVia.csv` sirve para ampliar equivalencias, no para imponer sin más una forma
canónica. El catálogo tiene pares duplicados, relaciones no simétricas y dos
códigos usados no cubiertos. Un normalizador debe:

1. conservar el `TVIA` original;
2. expandir equivalencias conocidas;
3. aceptar códigos desconocidos;
4. versionar cualquier elección de etiqueta canónica.

## Reglas observadas que pueden cambiar

En los snapshots analizados:

- `LSECC` está siempre vacío;
- `MANZ` está siempre vacío;
- `SUBSC` es blanco o `01`-`06`;
- nunca aparecen `CVIA` y `CPSVIA` a la vez;
- los nombres denormalizados de `TRAM` coinciden con sus catálogos;
- `TIPOINF`, `CDEV` y `CVAR` están vacíos.

Estas condiciones son excelentes alertas de regresión, pero salvo donde el diseño
lo indique no deben codificarse como dominios cerrados permanentes.

## Ingesta y actualización

- Validar en staging antes de publicar una nueva versión.
- Contar anchuras, duplicados, dominios y referencias en cada publicación.
- Sustituir snapshots de forma atómica.
- No usar `FVAR` del snapshot como fecha de modificación individual.
- No aplicar el bundle de variaciones sin deduplicación y reconciliación contra el
  snapshot siguiente.

El esquema concreto recomendado está en [modelo relacional](./relational_model.md).
