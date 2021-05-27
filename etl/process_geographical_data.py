import pandas as pd
import numpy as np
import os
import sys 

processed_data_path = os.path.abspath(
    os.path.join(os.getcwd(), os.pardir, "data", "data_geographical", "processed")
)

def generate_geographical_data(filename):
    """
    
    """
    df= pd.read_excel(filename, header=1, skiprows=3)
    year = int(filename.split('.')[0][-4:])
    last_year = year-1

    df = df[:-1].copy()
    df = df.replace('€','',regex=True)
    if year <= 2015:
        col_provinces = 'PROVINCIAS'
        gross_colname_current_year = 'RECAUDACION {}'.format(year)
        gross_colname_last_year = 'RECAUDACION {}'.format(last_year)
        admissions_colname_current_year = 'ESPECTADORES {}'.format(year)
        admissions_colname_last_year = 'ESPECTADORES {}'.format(last_year)

    else:
        col_provinces = 'PROVINCIA'
        gross_colname_current_year = 'REC. {}'.format(year)
        gross_colname_last_year = 'REC. {}'.format(last_year)
        admissions_colname_current_year = 'ESP. {}'.format(year)
        admissions_colname_last_year = 'ESP. {}'.format(last_year)
    
    df = df[
        [
            col_provinces, 
            gross_colname_last_year, 
            gross_colname_current_year, 
            admissions_colname_last_year,
            admissions_colname_current_year
        ]
    ].copy()

    df_current_year = df[[col_provinces, gross_colname_current_year,admissions_colname_current_year]].copy()
    df_current_year['year'] = year
    df_current_year.columns = ['province','gross_total','admissions_total','year']



    df_last_year = df[[col_provinces, gross_colname_last_year,admissions_colname_last_year]].copy()
    df_last_year['year'] = last_year
    df_last_year.columns = ['province','gross_total','admissions_total','year']

    df = pd.concat([df_last_year,df_current_year],axis=0)
    df['province'] = df['province'].str.upper()
    df['_id'] = df['year'].astype(str) + '-' + df['province']
    df['gross_total'] = [str(x).replace('.', '').replace(' ','') for x in df['gross_total']]
    df['admissions_total'] = [str(x).replace('.', '').replace(' ','') for x in df['admissions_total']]
    df['gross_total'] = df['gross_total'].astype(float)
    df['admissions_total'] = df['admissions_total'].astype(float)
    
    export_files_to_csv(df,year,last_year)
    export_files_to_json(df, year, last_year)

############################
#     EXPORT FUNCTIONS     #
############################


def export_files_to_csv(df, year, last_year):
    """
    :param df:
    :param year:
    :param last_year:
    :return:
    """

    df_json = df.to_json(orient="records")
    with open(
        processed_data_path + "/json/province_{}_{}.json".format(year,last_year),
        "w", encoding='iso-8859-1'
    ) as f:
        f.write(df_json)


def export_files_to_json(df, year, last_year):
    """
    :param df:
    :param year:
    :param last_year:
    :return:
    """
    df.to_csv(
        processed_data_path + "/csv/province_{}_{}.csv".format(year,last_year),
        index=False,
    )
    

if __name__ == "__main__":

    try:
        if len(sys.argv) != 2:
            raise Exception(
                "[ERROR] Incorrect Args : python process_geographical_data <absolute_filename_path>"
            )
        generate_geographical_data(sys.argv[1])
    except Exception as e:
        print(e)
