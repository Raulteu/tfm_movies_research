#!/bin/bash

dir="$1"

for file in $(ls "$dir"); do
    ./load_mongo_weekly.sh "$dir/$file"
done
