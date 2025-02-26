import pandas as pd
from datetime import datetime, timedelta
import os 
import json
from pathlib import Path

n_media_samples = 6

root = Path(__file__).parents[2]
config_path = os.path.join(root, 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

train_csv_path = os.path.join(root, 'data', 'dataframes', 'dfTrain.csv')
test_csv_path = os.path.join(root, 'data', 'dataframes', 'dfTest.csv')
predictions_csv_path = os.path.join(root, 'models', 'avg', 'dfPredictions.csv')

dfTrain = pd.read_csv(train_csv_path)
dfTrain = dfTrain.tail(n_media_samples)

dfTest = pd.read_csv(test_csv_path)

df = pd.concat([dfTrain, dfTest], ignore_index=True)
df['time'] = pd.to_datetime(df['last_updated_dt'])

dfPredictions = pd.DataFrame()

for index, row in df.iloc[n_media_samples:].iterrows():
    sum = 0
    for j in range(1, n_media_samples + 1):
        sum += df['num_bikes_available'].iloc[index-j]

    for i in range(0, config['prediction_window']):    
        pred = sum / n_media_samples
  
        if ((index + i) < df.shape[0]):
            dfAux = pd.DataFrame({
                'LastTimeWithData': [df['time'].iloc[index-1]],
                'ti': [i + 1],
                'Time': [df['time'].iloc[index + i]],
                'Predict': [pred],
                'Real': [df['num_bikes_available'].iloc[index + i]]
            })

            dfPredictions = pd.concat([dfPredictions, dfAux], ignore_index=True)

            sum += pred

        sum -= df['num_bikes_available'].iloc[index + i - config['prediction_window'] - 1]


dfPredictions.to_csv(predictions_csv_path, index=False)

