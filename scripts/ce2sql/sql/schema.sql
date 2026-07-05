CREATE TABLE comunidad_autonoma (
    codigo_autonomia TEXT NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE provincia (
    codigo_provincia TEXT NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE municipio (
    codigo_provincia TEXT NOT NULL,
    codigo_municipio TEXT NOT NULL,
    codigo_autonomia TEXT NOT NULL,
    digito_control TEXT NOT NULL,
    nombre TEXT NOT NULL,
    PRIMARY KEY (codigo_provincia, codigo_municipio),
    FOREIGN KEY (codigo_autonomia) REFERENCES comunidad_autonoma (codigo_autonomia),
    FOREIGN KEY (codigo_provincia) REFERENCES provincia (codigo_provincia)
);

CREATE TABLE tipo_via_sinonimo (
    tipo_via TEXT NOT NULL,
    sinonimo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    comentario TEXT NOT NULL
);

CREATE TABLE unidad_poblacional (
    codigo_provincia TEXT NOT NULL,
    codigo_municipio TEXT NOT NULL,
    codigo_unidad_poblacional TEXT NOT NULL,
    tipo_informacion TEXT NOT NULL,
    causa_devolucion TEXT NOT NULL,
    causa_variacion TEXT NOT NULL,
    nombre_municipio_largo TEXT NOT NULL,
    nombre_municipio TEXT NOT NULL,
    nombre_municipio_corto TEXT NOT NULL,
    nombre_entidad_colectiva_largo TEXT NOT NULL,
    nombre_entidad_colectiva TEXT NOT NULL,
    nombre_entidad_colectiva_corto TEXT NOT NULL,
    nombre_entidad_singular_largo TEXT NOT NULL,
    nombre_entidad_singular TEXT NOT NULL,
    nombre_entidad_singular_corto TEXT NOT NULL,
    nombre_nucleo_largo TEXT NOT NULL,
    nombre_nucleo TEXT NOT NULL,
    nombre_nucleo_corto TEXT NOT NULL,
    PRIMARY KEY (codigo_provincia, codigo_municipio, codigo_unidad_poblacional),
    FOREIGN KEY (codigo_provincia, codigo_municipio) REFERENCES municipio (codigo_provincia, codigo_municipio)
);

CREATE TABLE seccion_censal (
    codigo_provincia TEXT NOT NULL,
    codigo_municipio TEXT NOT NULL,
    distrito TEXT NOT NULL,
    seccion TEXT NOT NULL,
    letra_seccion TEXT NOT NULL,
    PRIMARY KEY (codigo_provincia, codigo_municipio, distrito, seccion, letra_seccion),
    FOREIGN KEY (codigo_provincia, codigo_municipio) REFERENCES municipio (codigo_provincia, codigo_municipio)
);

CREATE TABLE via (
    codigo_provincia TEXT NOT NULL,
    codigo_municipio TEXT NOT NULL,
    codigo_via TEXT NOT NULL,
    tipo_informacion TEXT NOT NULL,
    causa_devolucion TEXT NOT NULL,
    causa_variacion TEXT NOT NULL,
    tipo_via TEXT NOT NULL,
    nombre TEXT NOT NULL,
    nombre_corto TEXT NOT NULL,
    PRIMARY KEY (codigo_provincia, codigo_municipio, codigo_via),
    FOREIGN KEY (codigo_provincia, codigo_municipio) REFERENCES municipio (codigo_provincia, codigo_municipio)
);

CREATE TABLE pseudovia (
    codigo_provincia TEXT NOT NULL,
    codigo_municipio TEXT NOT NULL,
    codigo_pseudovia TEXT NOT NULL,
    tipo_informacion TEXT NOT NULL,
    causa_devolucion TEXT NOT NULL,
    causa_variacion TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    PRIMARY KEY (codigo_provincia, codigo_municipio, codigo_pseudovia),
    FOREIGN KEY (codigo_provincia, codigo_municipio) REFERENCES municipio (codigo_provincia, codigo_municipio)
);

CREATE TABLE tramo (
    codigo_provincia TEXT NOT NULL,
    codigo_municipio TEXT NOT NULL,
    distrito TEXT NOT NULL,
    seccion TEXT NOT NULL,
    letra_seccion TEXT NOT NULL,
    subseccion TEXT NOT NULL,
    codigo_unidad_poblacional TEXT NOT NULL,
    nombre_entidad_colectiva_corto TEXT NOT NULL,
    nombre_entidad_singular_corto TEXT NOT NULL,
    nombre_nucleo_corto TEXT NOT NULL,
    codigo_via TEXT NOT NULL,
    nombre_via_corto TEXT NOT NULL,
    codigo_pseudovia TEXT NOT NULL,
    descripcion_pseudovia TEXT NOT NULL,
    manzana TEXT NOT NULL,
    codigo_postal TEXT NOT NULL,
    tipo_numeracion TEXT NOT NULL,
    extremo_inferior TEXT NOT NULL,
    calificador_extremo_inferior TEXT NOT NULL,
    extremo_superior TEXT NOT NULL,
    calificador_extremo_superior TEXT NOT NULL,
    tipo_informacion TEXT NOT NULL,
    causa_devolucion TEXT NOT NULL,
    causa_variacion TEXT NOT NULL,
    PRIMARY KEY (
        codigo_provincia,
        codigo_municipio,
        distrito,
        seccion,
        letra_seccion,
        subseccion,
        codigo_unidad_poblacional,
        codigo_via,
        codigo_pseudovia,
        manzana,
        codigo_postal,
        tipo_numeracion,
        extremo_inferior,
        calificador_extremo_inferior,
        extremo_superior,
        calificador_extremo_superior
    ),
    FOREIGN KEY (codigo_provincia, codigo_municipio)
        REFERENCES municipio (codigo_provincia, codigo_municipio),
    FOREIGN KEY (codigo_provincia, codigo_municipio, codigo_unidad_poblacional)
        REFERENCES unidad_poblacional (codigo_provincia, codigo_municipio, codigo_unidad_poblacional),
    FOREIGN KEY (codigo_provincia, codigo_municipio, distrito, seccion, letra_seccion)
        REFERENCES seccion_censal (codigo_provincia, codigo_municipio, distrito, seccion, letra_seccion)
);
