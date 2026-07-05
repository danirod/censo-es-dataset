SELECT COUNT(*)
FROM tramo AS tramo
WHERE tramo.codigo_pseudovia <> '00000'
  AND NOT EXISTS (
    SELECT 1
    FROM pseudovia AS pseudovia
    WHERE pseudovia.codigo_provincia = tramo.codigo_provincia
      AND pseudovia.codigo_municipio = tramo.codigo_municipio
      AND pseudovia.codigo_pseudovia = tramo.codigo_pseudovia
  );
