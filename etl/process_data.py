import os
import json
import pandas as pd
import numpy as np
from imdb import IMDb


def read_xlsx(filename, extension, skiprows, cols):
    df = pd.read_excel(filename, header=None, skiprows=skiprows, names=cols)
    return df


def create_sessions(sessions):
    interim_data_path = os.path.abspath(
        os.path.join(os.getcwd(), os.pardir, "data", "interim")
    )

    files = os.listdir(interim_data_path)
    files.sort()

    for file in files[:20]:
        print(
            ("-" * 10)
            + "{}".format(file)
            + ("-" * 10)
        )
        datetime_file = file.split('.')[0]

        # First Season
        if datetime_file < '2013-01-11':
            header = [
                'rank', 'title', 'dist', 'sem', 'cinemas', 'screens',
                'gross_total', 'gross_increment', 'gross_cinema_mean', 'gross_screens_mean',
                'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
                'amount_eur', 'spectators']
            df = read_xlsx(os.path.join(interim_data_path, file), 'xls', skiprows=10, cols=header)
            df['original_title'] = np.nan
            df = df.iloc[9:].copy()
        # Second Season
        elif datetime_file >= '2013-01-11' and datetime_file < '2014-05-16':
            header = [
                'rank', 'title', 'dist', 'sem', 'cinemas', 'screens',
                'gross_total', 'gross_increment', 'gross_cinema_mean', 'gross_screens_mean',
                'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
                'amount_eur', 'spectators']
            df = read_xlsx(os.path.join(interim_data_path, file), 'xls', skiprows=14, cols=header)
            df['original_title'] = np.nan
            df = df.iloc[8:].copy()
        # Third Season
        elif datetime_file >= '2014-05-16' and datetime_file < '2015-05-29':
            header = [
                'rank', 'title', 'original_title', 'dist', 'sem', 'cinemas', 'screens',
                'gross_total', 'gross_increment', 'gross_cinema_mean', 'gross_screens_mean',
                'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
                'amount_eur', 'spectators']

            df = read_xlsx(os.path.join(interim_data_path, file), 'xls', skiprows=22, cols=header)

        # Fourth Season
        else:
            header = [
                'rank', 'title', 'original_title', 'dist', 'sem', 'cinemas', 'screens',
                'gross_total', 'gross_increment', 'gross_cinema_mean', 'gross_screens_mean',
                'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
                'amount_eur', 'spectators']
            df = read_xlsx(os.path.join(interim_data_path, file), 'xls', skiprows=16, cols=header)

        sessions = pd.concat([sessions, df])

    sessions = sessions[sessions["rank"].notna()].copy()


    return sessions


def set_imdb_info(row, movie_name):
    # create an instance of the IMDb class
    ia = IMDb()

    id = ia.search_movie(movie_name)[0].movieID
    movie = ia.get_movie(id).data

    row['year'] = movie['year']
    row['id_imdb'] = id
    row['url'] = "https://www.imdb.com/title/tt" + id
    row['rating'] = movie['rating']
    row['votes'] = movie['votes']
    row['release_date'] = movie['original air date']
    row['genre'] = movie['genres']
    row['main_director'] = [elem['name'] for elem in movie['director']]
    row['directors'] = [elem['name'] for elem in movie['directors']]
    row['main_writer'] = [elem['name'] for elem in movie['writer']]
    row['writers'] = [elem['name'] for elem in movie['writers']]
    row['producers'] = [elem['name'] for elem in movie['producers']]
    row['actors'] = [elem['name'] for elem in movie['cast']]
    row['plot'] = movie['plot']
    row['language'] = movie['languages']
    row['country'] = movie['countries']
    row['production'] = movie['production companies']
    print(movie_name)


def create_movies(df):
    columns = ["title", "original_title", "year", "id_imdb", "url_imdb", "rating_imdb", "release_date",
               "genre", "rated", "director", "writer", "actors", "plot", "language", "country", "awards", "production"]

    movies = pd.DataFrame()
    movies["title"] = df.title.unique()
    print(movies.head(20))
    # CREAR TITLE Y ORIGINAL TITLE COMO UNIQUE DEL DATAFRAME SESSIONS
    # ...

    # ...

    # POR CADA TITLE:
    for index, row in movies.iterrows():
        print(row)
        set_imdb_info(row, row['title'])
    print(movies.head(20))


    # a = np.unique(df[["title", "original_title"]].values)
    # print(a)
    # movies["title"] = df.title.unique()
    # movies["original_title"] = df.original_title.unique()

    # print(df.title.unique())
    # print("_____________________________")
    # print(df.original_title.unique())


def main():
    columns = [
        'rank', 'title', 'original_title', 'dist', 'sem', 'cinemas', 'screens',
        'gross_total', 'gross_increment', 'gross_cinema_mean', 'gross_screens_mean',
        'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
        'amount_eur', 'spectators']
    sessions = pd.DataFrame(columns=columns)

    df = create_sessions(sessions)
    create_movies(df)


if __name__ == "__main__":
    main()

# TODO
# Añadir titulo original a aquellas peliculas que no lo tengan (fase 1 y fase 2)
# Concatenar el dataframe de cada iteracion en uno final que será ya la tabla de sessiones (eliminar de esta tabla las columnas de increment)
# Coger las peliculas del dataframe session con el atributo unique() y crear un dataframe nuevo que sera la tabla de peliculas, enriquecer este dataframe con imdb ...
# Con esto tendriamos las dos tablas listas
