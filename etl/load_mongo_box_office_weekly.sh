#!/bin/bash

if [ -z $1 ]; then
    echo "USAGE: load_mongo_box_office_weekly.sh <FILEPATH>" &>/dev/stderr
    exit 1
fi

file="$1"

name="$(basename $1)"

datefile=${name%.*}

python process_data_box_office.py "$file"

mongoimport --db db_movies --collection sessions --file ../data/processed/json/sessions_"$datefile".json --jsonArray --upsert

mongoimport --db db_movies --collection movies --file ../data/processed/json/movies_"$datefile".json --jsonArray --upsert