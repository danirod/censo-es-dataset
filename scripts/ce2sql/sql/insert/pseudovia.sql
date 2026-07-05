INSERT INTO pseudovia (
    codigo_provincia,
    codigo_municipio,
    codigo_pseudovia,
    tipo_informacion,
    causa_devolucion,
    causa_variacion,
    descripcion
) VALUES (
    :codigo_provincia,
    :codigo_municipio,
    :codigo_pseudovia,
    :tipo_informacion,
    :causa_devolucion,
    :causa_variacion,
    :descripcion
);
