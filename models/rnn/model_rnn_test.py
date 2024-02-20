#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append("../..")

import pandas as pd
import pickle
import numpy as np
import config
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# In[2]:


name_model = 'RNN'

seq_length = 6 # model memory

train_csv_path = '../../data/dataframes/dfTrain.csv'
test_csv_path = '../../data/dataframes/dfTest.csv'
predictions_csv_path = './dfPredictions.csv'

rnn_model_pickle_path = './model.pickle' 
rnn_scaler_pickle_path = './scaler.pickle' 


# In[3]:


model = pd.read_pickle(rnn_model_pickle_path)
sc = pd.read_pickle(rnn_scaler_pickle_path)


# In[4]:


dfTrain = pd.read_csv(train_csv_path)
dfTrain = dfTrain.tail(seq_length)

dfTest = pd.read_csv(test_csv_path)

df = pd.concat([dfTrain, dfTest], ignore_index=True)
df['time'] = pd.to_datetime(df['last_updated_dt'])


# In[5]:


def df_to_X_y(data):
    x = []
    y = []

    for i in range(len(data)-seq_length):
        _x = data[i:(i+seq_length)]
        _y = data[i+seq_length:i+seq_length+1]
        x.append(_x)
        y.append(_y)

    return np.array(x),np.array(y)


# In[6]:


training_data = df['time'].values.reshape(-1, 1)
testXtime, testYTime = df_to_X_y(training_data)


# In[7]:


training_data = df['num_bikes_available'].values.reshape(-1, 1)
testX_num_bikes_available, testY_num_bikes_available = df_to_X_y(training_data)


# In[8]:


sc = StandardScaler()
training_data = sc.fit_transform(df['num_bikes_available'].values.reshape(-1, 1))
testX, testY = df_to_X_y(training_data)


# In[9]:


dfPredictions = pd.DataFrame()

testX_i = testX
testXtime_i = testXtime[:, -1, 0]
testX_num_bikes_available_i = testX_num_bikes_available[:, -1, 0]

testY_i = testY[:, 0, 0]
testYTime_i = testYTime[:, 0, 0]
testY_num_bikes_available_i = testY_num_bikes_available[:, 0, 0]

for i in range(1, config.prediction_window + 1):
    aux = model.predict(testX_i)
    predict = sc.inverse_transform(aux)
    predict = predict[:, 0]

    dfAux = pd.DataFrame({
        'Model' : name_model,
        'LastTimeWithData': testXtime_i,
        'ti': i,
        'Time': testYTime_i,
        'Predict': predict,
        'Real': testY_num_bikes_available_i
    })
    dfPredictions = pd.concat([dfPredictions, dfAux], ignore_index=True)

    testX_i = np.hstack((testX_i, aux[:, np.newaxis]))  #le agrego una dimension a aux para poder hacer hstack
    testX_i = testX_i[:, -seq_length:, :]   #quito la primera columna
    testX_i = testX_i[:-1]
    
    testXtime_i = testXtime_i[:-1]
    testX_num_bikes_available_i = testX_num_bikes_available_i[:-1]

    testY_i = testY_i[1:]
    testYTime_i = testYTime_i[1:]
    testY_num_bikes_available_i = testY_num_bikes_available_i[1:]


# In[10]:


dfPredictions.to_csv(predictions_csv_path, index=False)

