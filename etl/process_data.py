import os
import json
import pandas as pd
import numpy as np
from imdb import IMDb

interim_data_path = os.path.abspath(
    os.path.join(os.getcwd(), os.pardir, "data", "interim")
)
processed_data_path = os.path.abspath(
    os.path.join(os.getcwd(), os.pardir, "data", "processed")
)

############################
#    SESSIONS FUNCTIONS    #
############################

def read_xlsx(filename, extension, skiprows, cols):
    df = pd.read_excel(filename, header=None, skiprows=skiprows, names=cols)
    return df

def set_primary_key_sessions(row,movies):
    """
    :param movies:
    :param row:
    :return:
    """
    try:
        id_imdb = movies[movies['title'] == row['title']]['id_imdb'].values[0]
        if id_imdb:
            row['id_imdb'] = id_imdb
        else:
            row['id_imdb'] = None
    except:
        row['id_imdb'] = None
    
    return row

def create_sessions(sessions):

    files = os.listdir(interim_data_path)
    files.sort()

    for file in files[-10:]:
        print(
            ("-" * 10)
            + "{}".format(file)
            + ("-" * 10)
        )
        datetime_file = file.split('.')[0]

        # First Season
        if datetime_file < '2013-01-11' and datetime_file != '2013-12-27':
            header = [
                'rank', 'title', 'dist', 'sem', 'cinemas', 'screens',
                'gross_total', 'gross_delta', 'gross_cinema_mean', 'gross_screens_mean',
                'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
                'amount_eur', 'spectators']
            df = read_xlsx(os.path.join(interim_data_path, file), 'xls', skiprows=10, cols=header)
            df['original_title'] = np.nan
            df = df.iloc[9:].copy()

        # Second Season
        elif datetime_file >= '2013-01-11' and datetime_file < '2014-05-16':
            header = [
                'rank', 'title', 'dist', 'sem', 'cinemas', 'screens',
                'gross_total', 'gross_delta', 'gross_cinema_mean', 'gross_screens_mean',
                'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
                'amount_eur', 'spectators']
            df = read_xlsx(os.path.join(interim_data_path, file), 'xls', skiprows=14, cols=header)
            df['original_title'] = np.nan
            df = df.iloc[8:].copy()

        # Third Season
        elif datetime_file >= '2014-05-16' and datetime_file < '2015-05-29':
            header = [
                'rank', 'title', 'original_title', 'dist', 'sem', 'cinemas', 'screens',
                'gross_total', 'gross_delta', 'gross_cinema_mean', 'gross_screens_mean',
                'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
                'amount_eur', 'spectators']
            df = read_xlsx(os.path.join(interim_data_path, file), 'xls', skiprows=16, cols=header)

        # Fourth Season
        else:
            header = [
                'rank', 'title', 'original_title', 'dist', 'sem', 'cinemas', 'screens',
                'gross_total', 'gross_delta', 'gross_cinema_mean', 'gross_screens_mean',
                'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
                'amount_eur', 'spectators']
            df = read_xlsx(os.path.join(interim_data_path, file), 'xls', skiprows=16, cols=header)

        df['date'] = datetime_file
        sessions = pd.concat([sessions, df])

    sessions = sessions[sessions["rank"].notna()].copy()
    sessions['id_imdb'] = np.nan
    sessions = sessions.drop(['gross_delta','admissions_delta'],axis=1)
    sessions = sessions.sort_values(by = ['date','rank'])

    return sessions

############################
#     MOVIES FUNCTIONS     #
############################

def set_imdb_info(row):
    """
    :param row:
    :return:
    """
    try:
            
        if pd.isnull(row['original_title']):
            movie_name = row['title'] + " " + row['min_date'][0:4]
        else:
            movie_name = row['original_title']

        print("*" * 50)
        print("Getting info about {}...".format(movie_name))

        ia = IMDb()
        ids = ia.search_movie(movie_name)

        if(len(ids) > 0):
            id = ids[0].movieID
        else:
            ids = ia.search_movie(row['title'])
            id = ids[0].movieID

        movie = ia.get_movie(id).data

        standard_features = ['year', 'rating', 'votes', 'original air date', 'genres', 'plot', 'languages',
                             'countries', 'original title', 'certificates']

        features_with_name = ['director', 'writer', 'writers', 'producers', 'production companies',
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


############################
#     EXPORT FUNCTIONS     #
############################

def export_files_to_csv(sessions,movies):
    """
    :param sessions:
    :param movies:
    :return:
    """
    
    sessions.to_csv(processed_data_path + "/sessions.csv", index=False)
    movies.to_csv(processed_data_path + "/movies.csv", index=False)

def export_files_to_json(sessions,movies):
    """
    :param sessions:
    :param movies:
    :return:
    """

    sessions_json = sessions.to_json(orient='records')
    with open(processed_data_path + '/sessions.json', 'w') as f:
        f.write(sessions_json)

    movies_json = movies.to_json(orient='records')
    with open(processed_data_path + '/movies.json', 'w') as f:
        f.write(movies_json)


############################
#       MAIN FUNCTION      #
############################

def generate_processed_files():
    """
    :return:
    """
    sessions = pd.DataFrame()

    sessions = create_sessions(sessions)
    movies = create_movies(sessions)
    sessions = sessions.apply(lambda row: set_primary_key_sessions(row, movies), axis=1)

    export_files_to_csv(sessions, movies)
    export_files_to_json(sessions, movies)

if __name__ == "__main__":
    generate_processed_files()