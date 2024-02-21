#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import datetime, timedelta
import os 
import json


# In[2]:

current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, '../../config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

train_csv_path = os.path.join(current_path, '../../data/dataframes/dfTrain.csv')
test_csv_path = os.path.join(current_path, '../../data/dataframes/dfTest.csv')
predictions_csv_path = os.path.join(current_path, './dfPredictions.csv')


# In[3]:


dfTrain = pd.read_csv(train_csv_path)
dfTrain = dfTrain.tail(1)

dfTest = pd.read_csv(test_csv_path)

df = pd.concat([dfTrain, dfTest], ignore_index=True)
df['time'] = pd.to_datetime(df['last_updated_dt'])


# In[4]:


dfPredictions = pd.DataFrame()

for index, row in df.iloc[1:].iterrows():
    for i in range(1, config['prediction_window'] + 1):
        dfAux = pd.DataFrame({
            'LastTimeWithData': [df['time'].shift(i).iloc[index]],
            'ti': [i],
            'Time': [row['time']],
            'Predict': [df['num_bikes_available'].shift(i).iloc[index]],
            'Real': [row['num_bikes_available']]
        }, index=[index])

        dfPredictions = pd.concat([dfPredictions, dfAux], ignore_index=True)

dfPredictions['LastTimeWithData'] = pd.to_datetime(dfPredictions['LastTimeWithData'], errors='coerce')
dfPredictions = dfPredictions.dropna(subset=['LastTimeWithData'])
dfPredictions = dfPredictions.dropna(subset=['Predict'])


# In[6]:


dfPredictions.to_csv(predictions_csv_path, index=False)

