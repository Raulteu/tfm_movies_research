# tfm_movies_research

## Prerequisitos
Por motivos de confidencialidad, los datos no se encuentran en este repositorio. Una vez que haya obtenido los datos debe colocarlos en la carpteta ```data/raw``` situada en la raiz del proyecto. A continuación se muestra el árbol de directorio para una correcta colocación de los datos:

```
.
├── data
│   ├── interim
│   ├── processed
│   └── raw
├── etl
│   ├── preprocess_data.py
│   └── process_data.py
└── README.md

```

Para realizar de forma correcta el parseo de los ficheros xlsx y xls es necesaio tener instalada una versión específica de xlrd, para ello

```
python -m pip install xlrd==1.2.0
```

## Preprocesado

Este script carga en la carpeta ```data/interim``` los ficheros cambiando el mismo de los nombres para tenerlos organizados por fecha. Para ejecutarlo:

```
python preprocess_data.py
```

## Procesado

Para procesar los datos se ha creado un script en python encargado de generar el fichero csv | json correspondiente al fichero excel pasado por argumento. Para realizarlo debemos ejecutar:

```
python process_data.py <absolute-path-filename>
```

Dado que llegarán ficheros de forma semanal se han creados dos scripts de bash para automatizar esta tarea.

- Por un lado tenemos el script semanal (**load_mongo_weekly**) quebásicamente ejecuta el fichero de python anterior, panado el fichero como aegumento. Para ello:

```
/load_mongo_weekly.sh <absolute-path-filename>
```

Tras ello ejecutará las instrucciones para importar los datos en la BBDD

- Por otro lado, tenemos el script para cargar el histórico, que itera sobre todos los ficheros situados en la carpeta interim y ejecuta para cada uno de ellos el script semanal, importando también los datos en la BBDD.


```
/load_mongo_weekly.sh <directory>
```

## Importar datos a la Base de Datos

En este caso se ha seleccionado una Base de Datos no relacional (Mongo) dada la estructura de los campos procedentes de la entidad pelicula. Para importar los datos en esta BBDD deberemos:

```
use db_movies

mongoimport --db db_movies --collection sessions --file data/processed/sessions.json --jsonArray

mongoimport --db db_movies --collection movies --file data/processed/movies.json --jsonArray
```

## TODO

- Mirar fichero maldito (2013-12-27)
- afinar mas la busqueda de peliculas en imdb