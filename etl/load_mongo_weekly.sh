#!/bin/bash

file="$1"

name="$(basename $1)"

datefile=${name%.*}

python process_data.py "$file"

mongoimport --db db_movies --collection sessions --file ../data/processed/json/sessions_"$datefile".json --jsonArray

mongoimport --db db_movies --collection movies --file ../data/processed/json/movies_"$datefile".json --jsonArray