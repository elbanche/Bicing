#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append("../..")

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import keras
import tensorflow as tf
from keras import layers
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
import pickle
import config


# In[2]:


name_model = 'RNN'

seq_length = 6 # model memory

train_csv_path = '../../data/dataframes/dfTrain.csv'
test_csv_path = '../../data/dataframes/dfTest.csv'
predictions_csv_path = './dfPredictions.csv'

rnn_model_pickle_path = './model.pickle' 
rnn_scaler_pickle_path = './scaler.pickle' 


# In[3]:


df = pd.read_csv(train_csv_path)
df['time'] = pd.to_datetime(df['last_updated_dt'])


# In[4]:


def df_to_X_y(data):
    x = []
    y = []

    for i in range(len(data)-seq_length):
        _x = data[i:(i+seq_length)]
        _y = data[i+seq_length:i+seq_length+1]
        x.append(_x)
        y.append(_y)

    return np.array(x),np.array(y)


# In[5]:


sc = StandardScaler()
training_data = sc.fit_transform(df['num_bikes_available'].values.reshape(-1, 1))

trainX, trainY = df_to_X_y(training_data)


# In[6]:


#Model Creation
model = keras.Sequential()
model.add(layers.LSTM(32))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(1))
model.build(input_shape=trainX.shape)
model.summary()


# In[7]:


#Complile
model.compile(
    loss=keras.losses.MeanSquaredError(),
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.001, momentum=0.9),
    metrics=["mse"],
)


# In[8]:


#Fit
batch_size = 4
history = model.fit(
    trainX, trainY, batch_size=batch_size, epochs=10
)


# In[9]:


# Save
with open(rnn_model_pickle_path, 'wb') as file:
    pickle.dump(model, file)

with open(rnn_scaler_pickle_path, 'wb') as file:
    pickle.dump(sc, file)

