# Index
- [Files](#files)
- [Instructions](#instructions)

# Files

## generate_station_csv.py
A script to automates the process of generating CSV files for individual stations from a set of compressed data files.

**Command-Line Arguments:**
   - `--station_id`: The ID of the station for which CSV files will be generated.
   - `--start_year_month`: The start of the time range in the format YYYY_MM.
   - `--end_year_month`: The end of the time range in the format YYYY_MM.
   - `--zip_files_directory`: The path where the compressed data files are located.
   - `--output_file_path`: The path where the generated CSV files will be saved.

## resample_csv.py
A script to automate the resampling process and update the columns for later uses.

**Command-Line Arguments:**
   - `--freq_time`: Time frequency to be used for resampling the dataframe.
   - `--input_csv_file_path`: Path to the file to be readed.
   - `--output_csv_file_path`: Path to the file to be saved.

## ./data/
All files from 2023. For the latest data, users should check the official source at [OpenData Ajuntament Barcelona](https://opendata-ajuntament.barcelona.cat/data/ca/dataset/estat-estacions-bicing)

## RNN_model.ipynb
Creation, training, testing, and analysis of the RNN model to predict demand within a time window for a station in the network.

# Instructions
For example, if you want to study the RNN model for station 1, with all the records from 2023 using a 30-minute resample, you should execute the following code:

1. Generate a CSV file with station records from compressed files
```
python generate_station_csv.py --station_id 1 --start_year_month "2023_01" --end_year_month "2023_12" --zip_files_directory "./data/" --output_csv_file_path "./dataframes/df.csv"
```

2. Resample the created CSV file
```
python resample_csv.py --freq_time "30T" --input_csv_file_path "./dataframes/df.csv" --output_csv_file_path "./dataframes/dfResample.csv"
```

Now you're ready to work with the model in the Jupyter Notebook RNN_model.
