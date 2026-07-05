INSERT INTO via (
    codigo_provincia,
    codigo_municipio,
    codigo_via,
    tipo_informacion,
    causa_devolucion,
    causa_variacion,
    tipo_via,
    nombre,
    nombre_corto
) VALUES (
    :codigo_provincia,
    :codigo_municipio,
    :codigo_via,
    :tipo_informacion,
    :causa_devolucion,
    :causa_variacion,
    :tipo_via,
    :nombre,
    :nombre_corto
);
