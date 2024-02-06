import py7zr
import pandas as pd
import argparse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os

start_year_month = '2023_01'
end_year_month = '2023_12'
station_id = 1
zip_files_directory = './data/'
output_csv_file_path = './df.csv'

# Command line arguments setup
parser = argparse.ArgumentParser(description='Description of your script')
parser.add_argument('--station_id', type=int, default=station_id, help='ID of the station')
parser.add_argument('--start_year_month', type=str, default=start_year_month, help='Start of the period (format: YYYY_MM)')
parser.add_argument('--end_year_month', type=str, default=end_year_month, help='End of the period (format: YYYY_MM)')
parser.add_argument('--zip_files_directory', type=str, default=zip_files_directory, help='Path to the directory containing .7z files')
parser.add_argument('--output_csv_file_path', type=str, default=output_csv_file_path, help='Path to the file to be saved')

# Parse the arguments
args, unknown = parser.parse_known_args()

# Use the argument values
station_id = args.station_id
start_year_month = args.start_year_month
end_year_month = args.end_year_month
zip_files_directory = args.zip_files_directory
output_csv_file_path = args.output_csv_file_path

# Convert start and end year-month to datetime objects
start_date = datetime.strptime(start_year_month, '%Y_%m')
end_date = datetime.strptime(end_year_month, '%Y_%m')

# Generate and filter filenames for each month in the range
files_in_directory = os.listdir(zip_files_directory)
current_date = start_date
files = []

while current_date <= end_date:
    prefix_to_search = current_date.strftime("%Y_%m")
    
    # Filter files that start with the searched text
    files_with_prefix = [file for file in files_in_directory if file.startswith(prefix_to_search)]

    # Add the paths to the list of found files
    files.extend([os.path.join(zip_files_directory, file) for file in files_with_prefix])

    # Move to the next month
    current_date += relativedelta(months=1)

print("Files found:")
for file_path in files:
    print(file_path)

df = pd.DataFrame()

for file_7z_path in files:

    # Extract the content of the 7z file and load it into df_aux
    with py7zr.SevenZipFile(file_7z_path, 'r') as file:
        file.extractall(zip_files_directory)

    file_csv_path = file_7z_path.replace('.7z', '.csv')

    df_aux = pd.read_csv(file_csv_path)

    # Filtrar las estaciones iguales a station_id y concatenar con el resultado final
    df = pd.concat([df, df_aux[df_aux['station_id'] == station_id]])

    # Remove the extracted CSV file after loading it into the DataFrame
    os.remove(file_csv_path)

df.to_csv(output_csv_file_path, index=False)
