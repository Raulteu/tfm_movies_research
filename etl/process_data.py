import os
import json
import pandas as pd
import numpy as np


def read_xlsx(filename, extension, skiprows, cols):
    df = pd.read_excel(filename, header=None, skiprows=skiprows, names=cols)
    return df


def create_sessions(sessions):
    interim_data_path = os.path.abspath(
        os.path.join(os.getcwd(), os.pardir, "data", "interim")
    )

    files = os.listdir(interim_data_path)
    files.sort()

    for file in files[200:210]:
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


def create_movies(df):
    columns = ["id", "title", "original_title", "year", "id_imdb", "url_imdb", "rating_imdb", "release_date",
               "genre", "rated", "director", "writer", "actors", "plot", "language", "country", "awards", "production"]

    movies = pd.DataFrame()
    movies["title", "original_title"] = df[["title", "original_title"]]
    # a = np.unique(df[["title", "original_title"]].values)
    # print(a)
    # movies["title"] = df.title.unique()
    # movies["original_title"] = df.original_title.unique()

    print(movies.head(10))

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
