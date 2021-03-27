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

    for file in files[:1]:
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
            df = read_xlsx(os.path.join(interim_data_path, file), 'xls', skiprows=19, cols=header)
            df['original_title'] = np.nan
            df = df.iloc[9:].copy()
        # Second Season
        elif datetime_file >= '2013-01-11' and datetime_file < '2014-05-16':
            header = [
                'rank', 'title', 'dist', 'sem', 'cinemas', 'screens',
                'gross_total', 'gross_increment', 'gross_cinema_mean', 'gross_screens_mean',
                'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
                'amount_eur', 'spectators']
            df = read_xlsx(os.path.join(interim_data_path, file), 'xls', skiprows=22, cols=header)
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

        df['date'] = datetime_file
        sessions = pd.concat([sessions, df])

    # header = [
    #     'rank', 'title', 'dist', 'sem', 'cinemas', 'screens',
    #     'gross_total', 'gross_increment', 'gross_cinema_mean', 'gross_screens_mean',
    #     'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
    #     'amount_eur', 'spectators']
    # sessions = read_xlsx(os.path.join(interim_data_path, '2013-12-27.xls'), 'xls', skiprows=22, cols=header)

    sessions = sessions[sessions["rank"].notna()].copy()

    return sessions


def set_imdb_info(row):
    """
    :param row:
    :return:
    """
    if pd.isnull(row['original_title']):
        movie_name = row['title'] + " " + row['min_date'][0:4]
    else:
        movie_name = row['original_title']

    # movie_name = row['title']
    print("*" * 50)
    print("Getting info about {}...".format(movie_name))

    try:
        ia = IMDb()
        id = ia.search_movie(movie_name)[0].movieID
        movie = ia.get_movie(id).data

        standard_features = ['year', 'rating', 'votes', 'original air date', 'genres', 'plot', 'languages',
                             'countries', 'original title', 'certificates']

        features_with_name = ['director', 'writer', 'writers', 'producers', 'production companies'
                              'cast']
        row['original_title'] = movie['title']
        row['id_imdb'] = id
        row['url'] = "https://www.imdb.com/title/tt" + id

        for feature in standard_features:
            if feature in movie.keys():
                row[feature] = movie[feature]
            else:
                row[feature] = None

        for feature in features_with_name:
            if feature in movie.keys():
                row[feature] = [elem['name'] for elem in movie[feature] if 'name' in elem.keys()]
            else:
                row[feature] = []
    except:
        pass

    return row


def create_movies(sessions):
    """
    :param sessions:
    :return:
    """
    movies = pd.DataFrame()
    movies = sessions[["title", "original_title", "date"]].copy().drop_duplicates()
    movies = movies.groupby(by=["title", "original_title"], dropna=False).agg(min_date=('date', 'min')).reset_index()

    # POR CADA PELICULA:
    movies = movies.apply(lambda row: set_imdb_info(row), axis=1)
    movies = movies.drop(["original title", "min_date"], axis=1)

    return movies

def main():
    """
    :return:
    """
    sessions = pd.DataFrame()

    sessions = create_sessions(sessions)
    movies = create_movies(sessions)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    print(movies.head(20))

    # sessions.to_csv("sessions.csv", index=False)
    # movies.to_csv("movies.csv", index=False)


if __name__ == "__main__":
    main()

# TODO
# Hay algunas películas que no se encuentran en IMDb y aparecen en movies con NaN excepto title
# Volver a buscar esas películas sin el anio en el titulo

# Mirar fichero maldito
# Con esto tendriamos las dos tablas listas
