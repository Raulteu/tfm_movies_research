#!/bin/bash

if [ -z $1 ]; then
    echo "USAGE: load_mongo_box_office_historical.sh <DIR_PATH>" &>/dev/stderr
    exit 1
fi

dir="$1"

for file in $(ls "$dir"); do
    ./load_mongo_box_office_weekly.sh "$dir/$file"
done
