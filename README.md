# censo-es-dataset

Este repositorio contiene varios datasets de interés elaborados a partir del Callejero del Censo Electoral del INE. El Callejero del Censo Electoral del INE se puede descargar aquí: [https://www.ine.es/dyngs/DAB/es/index.htm?cid=1390](https://www.ine.es/dyngs/DAB/es/index.htm?cid=1390).

## Motivación

Hice esto originalmente porque quería cruzar la tabla de códigos postales con la de municipios, pero Correos pide 800 euros por esa información. Información que de todos modos está disponible de forma gratuita en el INE. Son como trileros, ellos ponen el anzuelo y a ver quién pica. No me sale de los huevos, que le pidan el dinero a Leire.

Luego lo estuve pensando, y tal vez sea interesante para fabricar más datasets de más cosas a partir de la información disponible en el INE. Listas de municipios, validadores de dirección... no hay límites.

## Instrucciones

Necesitas hacerte con una snapshot del INE del censo. Descárgalo desde el enlace anterior. Invoca el script de creación del SQLite. Recibe como parámetro la ruta al snapshot del INE (zip o extraído), y la ubicación del .sqlite a volcar. Tienes `uv` declarado en el `mise.toml`:

```bash
uv run scripts/build_sqlite.py caj_esp_012026.zip dataset.sqlite
```

Este script genera un dataset en formato SQLite que contiene los mismos datos que vienen del INE, pero cruzados en modo relacional, para una consulta más eficiente y poder sacar patrones mejor.

Luego está el script `scripts/generate_outputs.py`, que se ocupa de generar CSVs de referencia. Si los quieres rápidamente, los cargo en el directorio `output/`. Si tienes que regenerarlos (por ejemplo, porque haya una nueva snapshot), una vez tengas el SQLite generado puedes usar el siguiente comando para correr las queries:

```bash
uv run scripts/generate_outputs.py dataset.sqlite output/
```

## Licencias

Los datasets, **CC0-1.0**. Estoy jugando con datos públicos procedentes de fuentes públicas.

Los scripts para compilar los datasets son **MIT**. Tampoco es super innovador.

## Licencias de terceros

Los datasets publicados en este repositorio a partir de los scripts son elaboración propia a partir del archivo Callejero Censo electoral del INE ([www.ine.es](http://www.ine.es)). Fuente original reutilizada conforme al aviso legal del INE y su licencia CC BY 4.0: [https://www.ine.es/dyngs/AYU/index.htm?cid=125](https://www.ine.es/dyngs/AYU/index.htm?cid=125).