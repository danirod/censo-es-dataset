CREATE INDEX idx_tramo_codigo_postal ON tramo (codigo_postal);
CREATE INDEX idx_tramo_municipio ON tramo (codigo_provincia, codigo_municipio);
CREATE INDEX idx_tramo_via ON tramo (codigo_provincia, codigo_municipio, codigo_via);
CREATE INDEX idx_tramo_pseudovia ON tramo (codigo_provincia, codigo_municipio, codigo_pseudovia);
CREATE INDEX idx_tramo_unidad_poblacional
    ON tramo (codigo_provincia, codigo_municipio, codigo_unidad_poblacional);
CREATE INDEX idx_via_nombre ON via (codigo_provincia, codigo_municipio, nombre);
CREATE INDEX idx_pseudovia_descripcion ON pseudovia (codigo_provincia, codigo_municipio, descripcion);
