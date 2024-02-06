## generate_station_csv.py
A script to automates the process of generating CSV files for individual stations from a set of compressed data files.

**Command-Line Arguments:**
   - `--station_id`: The ID of the station for which CSV files will be generated.
   - `--start_year_month`: The start of the time range in the format YYYY_MM.
   - `--end_year_month`: The end of the time range in the format YYYY_MM.
   - `--zip_files_directory`: The path where the compressed data files are located.
   - `--output_file_path`: The path where the generated CSV files will be saved.

## generate_station_csv
A script to automate the resampling process and update the columns for later uses.

**Command-Line Arguments:**
   - `--freq_time`: Time frequency to be used for resampling the dataframe.
   - `--input_csv_file_path`: Path to the file to be readed.
   - `--output_csv_file_path`: Path to the file to be saved.

## ./data/
All files from 2023. For the latest data, users should check the official source at [OpenData Ajuntament Barcelona](https://opendata-ajuntament.barcelona.cat/data/ca/dataset/estat-estacions-bicing)
