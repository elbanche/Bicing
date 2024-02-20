#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import keras
import tensorflow as tf
from keras import layers
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
import pickle
import argparse
import os


# In[2]:


parser = argparse.ArgumentParser()
parser.add_argument('--time_of_the_day', type=str, help='Time of the day. Format: HH:MM')
args = parser.parse_args()
time_of_the_day = args.time_of_the_day


# In[3]:


name_model = 'RNN_by_time'

seq_length = 6 # model memory

train_csv_path = '../../data/dataframes/dfTrain.csv'
test_csv_path = '../../data/dataframes/dfTest.csv'
predictions_csv_path = './dfPredictions.csv'

pickles_path = './pickles' 


# In[ ]:


df = pd.read_csv(train_csv_path)
df['time'] = pd.to_datetime(df['last_updated_dt'])


# In[ ]:


if time_of_the_day:
    df = df[df['time'].dt.time == datetime.strptime(time_of_the_day, '%H:%M').time()]


# In[ ]:


def df_to_X_y(data):
    x = []
    y = []

    for i in range(len(data)-seq_length):
        _x = data[i:(i+seq_length)]
        _y = data[i+seq_length:i+seq_length+1]
        x.append(_x)
        y.append(_y)

    return np.array(x),np.array(y)


# In[ ]:


sc = StandardScaler()
training_data = sc.fit_transform(df['net_station_change'].values.reshape(-1, 1))

trainX, trainY = df_to_X_y(training_data)


# In[ ]:


#Model Creation
model = keras.Sequential()
model.add(layers.LSTM(32))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(1))
model.build(input_shape=trainX.shape)
model.summary()


# In[ ]:


#Complile
model.compile(
    loss=keras.losses.MeanSquaredError(),
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.001, momentum=0.9),
    metrics=["mse"],
)


# In[ ]:


#Fit
batch_size = 4
history = model.fit(
    trainX, trainY, batch_size=batch_size, epochs=10
)


# In[ ]:


# Save
time_of_the_day_str = ""
if time_of_the_day:
    time_of_the_day_str = time_of_the_day.replace(":", "_") + "_"

model_path = os.path.join(pickles_path, time_of_the_day_str + "model.pickle")
with open(model_path, 'wb') as file:
    pickle.dump(model, file)

scaler_path = os.path.join(pickles_path, time_of_the_day_str + "scaler.pickle")
with open(scaler_path, 'wb') as file:
    pickle.dump(sc, file)

