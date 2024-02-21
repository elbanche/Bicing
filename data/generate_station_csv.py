import py7zr
import pandas as pd
import argparse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os 
import json

current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, '../config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

zip_files_path = os.path.join(current_path, './raw/')
unziped_files_in_csv_path = os.path.join(current_path, './dataframes/df.csv')

first_datetime_to_test = datetime.strptime(config['first_datetime_to_test'], '%Y-%m-%d %H:%M')
start_date = first_datetime_to_test - timedelta(days=config['days_for_training'], hours=0, minutes=0)
start_date = start_date.replace(day=1)
end_date = first_datetime_to_test + timedelta(days=config['days_for_testing'], hours=0, minutes=0)

# Generate and filter filenames for each month in the range
files_in_directory = os.listdir(zip_files_path)
current_date = start_date
files = []

while current_date <= end_date:
    prefix_to_search = current_date.strftime("%Y_%m")
    
    # Filter files that start with the searched text
    files_with_prefix = [file for file in files_in_directory if file.startswith(prefix_to_search)]

    # Add the paths to the list of found files
    files.extend([os.path.join(zip_files_path, file) for file in files_with_prefix])

    # Move to the next month
    current_date += relativedelta(months=1)

print("Files found:")
for file_path in files:
    print(file_path)

df = pd.DataFrame()

for file_7z_path in files:

    # Extract the content of the 7z file and load it into df_aux
    with py7zr.SevenZipFile(file_7z_path, 'r') as file:
        file.extractall(zip_files_path)

    file_csv_path = file_7z_path.replace('.7z', '.csv')

    df_aux = pd.read_csv(file_csv_path)

    # Filtrar las estaciones iguales a station_id y concatenar con el resultado final
    df = pd.concat([df, df_aux[df_aux['station_id'] == config['station_id']]])

    # Remove the extracted CSV file after loading it into the DataFrame
    os.remove(file_csv_path)

df.to_csv(unziped_files_in_csv_path, index=False)
