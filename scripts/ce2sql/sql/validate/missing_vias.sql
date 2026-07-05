SELECT COUNT(*)
FROM tramo AS tramo
WHERE tramo.codigo_via <> '00000'
  AND NOT EXISTS (
    SELECT 1
    FROM via AS via
    WHERE via.codigo_provincia = tramo.codigo_provincia
      AND via.codigo_municipio = tramo.codigo_municipio
      AND via.codigo_via = tramo.codigo_via
  );
