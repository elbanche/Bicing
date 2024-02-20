import sys
sys.path.append("..") 

import pandas as pd
import argparse
import config

unziped_files_in_csv_path = './dataframes/df.csv'
resample_csv_path = './dataframes/dfResample.csv'

df = pd.read_csv(unziped_files_in_csv_path)

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
    g = df[df.station_id==i].resample(config.freq_time, on='last_updated_dt').agg(aggs)
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

df.to_csv(resample_csv_path, index=False)

