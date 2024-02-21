import pandas as pd
import argparse
from datetime import datetime, timedelta
import os 
import json

current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, '../config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

resample_csv_path = os.path.join(current_path, './dataframes/dfResample.csv')
train_csv_path = os.path.join(current_path, './dataframes/dfTrain.csv')
test_csv_path = os.path.join(current_path, './dataframes/dfTest.csv')

first_datetime_to_test = datetime.strptime(config['first_datetime_to_test'], '%Y-%m-%d %H:%M')
days_for_training = 300
days_for_testing = 6

days_for_training = timedelta(days=config['days_for_training'], hours=0, minutes=0)
days_for_testing = timedelta(days=config['days_for_testing'], hours=0, minutes=0)

df = pd.read_csv(resample_csv_path)
df['time'] = pd.to_datetime(df['last_updated_dt'])

trainStart = first_datetime_to_test - days_for_training
testEnd = first_datetime_to_test + days_for_testing

dfTrain = df[(trainStart  < df['time'])  & (df['time'] < first_datetime_to_test)]
dfTest = df[(first_datetime_to_test <= df['time']) & (df['time'] <= testEnd)]
df = pd.concat([dfTrain, dfTest], ignore_index=True)


dfTrain.to_csv(train_csv_path, index=False)
dfTest.to_csv(test_csv_path, index=False)

