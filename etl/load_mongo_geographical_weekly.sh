#!/bin/bash

if [ -z $1 ]; then
    echo "USAGE: load_mongo_geographical_weekly.sh <FILEPATH>" &>/dev/stderr
    exit 1
fi

file="$1"

name="$(basename $1)"

datefile=${name%.*}

year=${datefile: -4}
last_year=$(( $year - 1 ))

python process_geographical_data.py "$file"

mongoimport --db db_movies --collection provinces --file ../data_geographical/processed/json/province_"$year"_"$last_year".json --jsonArray --upsert
