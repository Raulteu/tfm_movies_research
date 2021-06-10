#!/bin/bash

####################
### Define paths ###
####################

box_office_path="data/data_box_office/processed/json/"
geographical_path="data/data_geographical/processed/json/"

#####################
### Run container ###
#####################

docker-compose up -d

#####################################
#####    Load Box office Data   #####
#####################################
for file in $(ls "$box_office_path"); do
    if [[ $file == *"movies"* ]]; then
        mongoimport --db db_movies --collection movies --file data/data_box_office/processed/json/"$file" --jsonArray --upsert
    fi

    if [[ $file == *"sessions"* ]]; then
        mongoimport --db db_movies --collection sessions --file data/data_geographical/processed/json/"$file" --jsonArray --upsert
    fi
done

#######################################
#####    Load Geographical Data   #####
#######################################

for file in $(ls "$geographical_path"); do
    mongoimport --db db_movies --collection provinces --file data/data_geographical/processed/json/"$file" --jsonArray --upsert
done