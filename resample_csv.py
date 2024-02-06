import pandas as pd
import argparse

freq_time = '30T' # para el resample
input_csv_file_path = './dataframes/df.csv'
output_csv_file_path = './dataframes/dfResample.csv'


# Command line arguments setup
parser = argparse.ArgumentParser(description='Description of your script')
parser.add_argument('--freq_time', type=str, default=freq_time, help='Time frequency to be used for resampling the dataframe')
parser.add_argument('--input_csv_file_path', type=str, default=input_csv_file_path, help='Path to the file to be readed')
parser.add_argument('--output_csv_file_path', type=str, default=output_csv_file_path, help='Path to the file to be saved')

# Parse the arguments
args = parser.parse_args()

# Use the argument values
freq_time = args.freq_time
input_csv_file_path = args.input_csv_file_path
output_csv_file_path = args.output_csv_file_path

df = pd.read_csv(input_csv_file_path)

df['last_reported_dt'] = pd.to_datetime(df['last_reported'], unit='s')
df['last_updated_dt'] = pd.to_datetime(df['last_updated'], unit='s')

aggs = {
    'num_bikes_available': 'first',
    'num_bikes_available_types.mechanical' :'first',
    'num_bikes_available_types.ebike': 'first',
    'num_docks_available': 'first',
    'status': 'first'
}

groups = []
for i in df.station_id.unique():
    g = df[df.station_id==i].resample(freq_time, on='last_updated_dt').agg(aggs)
    g['station_id'] = i
    g = g.reset_index()
    g = g.set_index(['station_id', 'last_updated_dt'])
    groups.append(g)
    
df = pd.concat(groups)
df.columns = ['num_bikes_available', 'num_bikes_available_types.mechanical', 'num_bikes_available_types.ebike', 'num_docks_available', 'status']

df['num_bikes_available'] = df['num_bikes_available'].ffill()
df['num_bikes_available_types.mechanical'] = df['num_bikes_available_types.mechanical'].ffill()
df['num_bikes_available_types.ebike'] = df['num_bikes_available_types.ebike'].ffill()

# Variables accesorias
df['empty'] = df['num_bikes_available'] == 0
df['full'] = df['num_docks_available'] == 0
df['not_in_service'] = df.status != 'IN_SERVICE'

# Calculamos el cambio neto
df['net_station_change'] = (df.groupby(['station_id']).num_bikes_available.shift(0) -
                            df.groupby(['station_id']).num_bikes_available.shift(1))
df['station_undock'] = df.net_station_change.apply(lambda x: x if x < 0 else 0)
df['station_dock'] = df.net_station_change.apply(lambda x: x if x > 0 else 0)

df['net_station_change'].fillna(0, inplace=True)
df['station_undock'].fillna(0, inplace=True)
df['station_dock'].fillna(0, inplace=True)

df['hour'] = df.index.get_level_values(1).hour
df['day'] = df.index.get_level_values(1).day
df['month'] = df.index.get_level_values(1).month
df['year'] = df.index.get_level_values(1).year
df['weekday'] = df.index.get_level_values(1).weekday

df = df.reset_index()

df.to_csv(output_csv_file_path, index=False)

