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

Este script es el encargado de generar el fichero [CSV | JSON] para despues imporarlo en la base de datos y explotar los datos, para ejecutarlo:

```
python process_data.py
```
