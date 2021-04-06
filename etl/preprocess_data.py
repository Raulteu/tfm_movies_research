import os
import datetime
import calendar
import shutil

def generate_interim_files():

    raw_data_path = os.path.abspath(os.path.join(
        os.getcwd(), os.pardir, "data", "raw")
    )
    interim_data_path = os.path.abspath(
        os.path.join(os.getcwd(), os.pardir, "data", "interim")
    )
    c = calendar.Calendar(firstweekday=calendar.MONDAY)
    months_map = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12,
    }

    years = [
        item
        for item in os.listdir(raw_data_path)
        if os.path.isdir(os.path.join(raw_data_path, item))
    ]
    years = list(map(int, years))
    years.sort()

    print(years)

    for year in years:
        current_year_path = os.path.join(raw_data_path, year.__str__())
        months = [
            item
            for item in os.listdir(current_year_path)
            if os.path.isdir(os.path.join(current_year_path, item))
        ]
        
        for month in months:
            print(
                ("-" * 10)
                + "RENAME {}-{} FILES".format(months_map[month], year)
                + ("-" * 10)
            )

            
            if year <= 2015 or (year == 2016 and months_map[month] <= 5):

                current_month_path = os.path.join(current_year_path, month, "top fin de semana")
                files = [
                    item
                    for item in os.listdir(current_month_path)
                    if (item.upper().endswith(".XLSX") or item.upper().endswith(".XLS"))
                    and item.upper().startswith("TOP FIN DE SEMANA")
                ]
                files.sort()
                monthcal = c.monthdatescalendar(year, months_map[month])
                for week_file in files:
                    week_number = int(week_file.split(".")[0][-1])
                    week_date = [
                        day
                        for week in monthcal
                        for day in week
                        if day.weekday() == calendar.FRIDAY
                    ]

                    if len(week_date) > len(files):
                        week_date.remove(week_date[0])
                        
                    week_date = week_date[week_number - 1]
                    filename = week_date.__str__() + "." + week_file.split(".")[1]
                    shutil.copy(os.path.join(current_month_path, week_file), interim_data_path)
                    os.rename(os.path.join(interim_data_path, week_file), os.path.join(interim_data_path, filename))
                    print("{} - {} --> {}".format(week_file, week_date, filename))
            else:
                current_month_path = os.path.join(current_year_path, month)
                files = [
                    item
                    for item in os.listdir(current_month_path)
                    if (item.upper().endswith("TOP FIN DE SEMANA.XLSX") or item.upper().endswith("TOP FIN DE SEMANA.XLS"))
                ]
                files.sort()
                monthcal = c.monthdatescalendar(year, months_map[month])
                for week_file in files:
                    week_number = int(week_file.split(".")[0])
                    week_date = [
                        day
                        for week in monthcal
                        for day in week
                        if day.weekday() == calendar.FRIDAY
                    ]

                    if len(week_date) > len(files):
                        week_date.remove(week_date[0])

                    week_date = week_date[week_number-1]
                    filename = week_date.__str__() + "." + week_file.split(".")[2]
                    shutil.copy(os.path.join(current_month_path, week_file), interim_data_path)
                    os.rename(os.path.join(interim_data_path, week_file), os.path.join(interim_data_path, filename))
                    print("{} - {} --> {}".format(week_file, week_date, filename))

if __name__ == "__main__":
    generate_interim_files()