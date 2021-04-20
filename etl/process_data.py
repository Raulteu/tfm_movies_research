import os
import json
import sys
import pandas as pd
import numpy as np
from imdb import IMDb
import collections


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
        id_imdb = movies[movies['title'].str.lower() == row['title'].lower()]['id_imdb'].values[0]
        if id_imdb:
            row['id_imdb'] = id_imdb
        else:
            row['id_imdb'] = None
    except:
        row['id_imdb'] = None
    
    return row

def create_sessions(sessions, filename):

    datetime_month_week_file = filename.split('.')[len(filename.split('.'))-2][-9:]
    print(
        ("-" * 10)
        + "{}".format(datetime_month_week_file)
        + ("-" * 10)
    )
    
    # First Season
    if datetime_month_week_file <= '2013-01-1':
        header = [
            'rank', 'title', 'dist', 'sem', 'cinemas', 'screens',
            'gross_total', 'gross_delta', 'gross_cinema_mean', 'gross_screens_mean',
            'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
            'amount_eur', 'spectators']
        df = read_xlsx(filename, 'xls', skiprows=19, cols=header)
        df['original_title'] = np.nan
        df['sem'] = df['sem'].replace({'P': 1})
    
    # Second Season
    elif datetime_month_week_file > '2013-01-1' and datetime_month_week_file <= '2015-05-5' and datetime_month_week_file != '2013-12-5':
        header = [
            'rank', 'title', 'dist', 'sem', 'cinemas', 'screens',
            'gross_total', 'gross_delta', 'gross_cinema_mean', 'gross_screens_mean',
            'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
            'amount_eur', 'spectators']
        df = read_xlsx(filename, 'xls', skiprows=22, cols=header)
        df['original_title'] = np.nan
        df['sem'] = df['sem'].replace({'P': 1})

    # Third Season
    elif datetime_month_week_file > '2015-05-5' and datetime_month_week_file <= '2016-12-4':
        header = [
            'rank', 'title', 'original_title', 'dist', 'sem', 'cinemas', 'screens',
            'gross_total', 'gross_delta', 'gross_cinema_mean', 'gross_screens_mean',
            'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
            'amount_eur', 'spectators']
        df = read_xlsx(filename, 'xls', skiprows=16, cols=header)
        df['sem'] = df['sem'].replace({'P': 1})

    # Fourth Season
    elif datetime_month_week_file > '2016-12-4':
        header = [
            'rank', 'title', 'original_title', 'dist', 'sem', 'cinemas', 'screens',
            'gross_total', 'gross_delta', 'gross_cinema_mean', 'gross_screens_mean',
            'admissions_total', 'admissions_delta', 'admissions_cinema_mean', 'admissions_screen_mean',
            'amount_eur', 'spectators']
        df = read_xlsx(filename, 'xls', skiprows=2, cols=header)
        df['sem'] = df['sem'].replace({'P': 1})


    df['date_file'] = datetime_month_week_file
    sessions = pd.concat([sessions, df])

    sessions = sessions[sessions["rank"].notna()].copy()
    sessions['id_imdb'] = np.nan
    sessions = sessions.drop(['gross_delta','admissions_delta'],axis=1)
    sessions = sessions.sort_values(by = ['date_file','rank'])

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
            movie_name = row['title'] + " " + row['date_file'][0:4]
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
        row['_id'] = id
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
    movies = sessions[["title", "original_title", "date_file"]].copy().drop_duplicates()

    movies = movies.apply(lambda row: set_imdb_info(row), axis=1)
    
    if 'original_title' in movies.columns:
        movies = movies.drop(["original_title", "date_file"], axis=1)
    else:
        movies = movies.drop(["date_file"], axis=1)


    return movies


############################
#     EXPORT FUNCTIONS     #
############################

def export_files_to_csv(sessions, movies, datetime_month_week_file):
    """
    :param sessions:
    :param movies:
    :param year:
    :return:
    """
    
    sessions.to_csv(processed_data_path + "/csv/sessions_{}.csv".format(datetime_month_week_file), index=False)
    movies.to_csv(processed_data_path + "/csv/movies_{}.csv".format(datetime_month_week_file), index=False)

def export_files_to_json(sessions, movies, datetime_month_week_file):
    """
    :param sessions:
    :param movies:
    :param year:
    :return:
    """

    sessions_json = sessions.to_json(orient='records')
    with open(processed_data_path + '/json/sessions_{}.json'.format(datetime_month_week_file), 'w') as f:
        f.write(sessions_json)

    movies_json = movies.to_json(orient='records')
    with open(processed_data_path + '/json/movies_{}.json'.format(datetime_month_week_file), 'w') as f:
        f.write(movies_json)


############################
#       MAIN FUNCTION      #
############################

def generate_processed_files(filename):
    """
    :return:
    """
    datetime_month_week_file = filename.split('.')[len(filename.split('.'))-2][-9:]
    sessions = pd.DataFrame()
    sessions = create_sessions(sessions,filename)

    movies = create_movies(sessions)
    sessions = sessions.apply(lambda row: set_primary_key_sessions(row, movies), axis=1)

    export_files_to_csv(sessions, movies, datetime_month_week_file)
    export_files_to_json(sessions, movies, datetime_month_week_file)


if __name__ == "__main__":
    
    try:
        if (len(sys.argv) != 2):
            raise Exception('[ERROR] Incorrect Args : python process_data.py <absolute_filename_path>')
        generate_processed_files(sys.argv[1])
    except Exception as e:
        print(e)