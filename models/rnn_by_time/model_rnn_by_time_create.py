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
import json
from pathlib import Path

root = Path(__file__).parents[2]
config_path = os.path.join(root, 'config.json')

parser = argparse.ArgumentParser()
parser.add_argument('--time_of_the_day', type=str, help='Time of the day. Format: HH:MM')
args = parser.parse_args()
time_of_the_day = args.time_of_the_day

seq_length = 6 # model memory

with open(config_path, 'r') as f:
    config = json.load(f)

train_csv_path = os.path.join(root, 'data', 'dataframes', 'dfTrain.csv')
test_csv_path = os.path.join(root, 'data', 'dataframes', 'dfTest.csv')
predictions_csv_path = os.path.join(root, 'models', 'rnn_by_time', 'dfPredictions.csv')
pickles_path = os.path.join(root, 'models', 'rnn_by_time', 'pickles')

df = pd.read_csv(train_csv_path)
df['time'] = pd.to_datetime(df['last_updated_dt'])

if time_of_the_day:
    df = df[df['time'].dt.time == datetime.strptime(time_of_the_day, '%H:%M').time()]

def df_to_X_y(data):
    x = []
    y = []

    for i in range(len(data)-seq_length):
        _x = data[i:(i+seq_length)]
        _y = data[i+seq_length:i+seq_length+1]
        x.append(_x)
        y.append(_y)

    return np.array(x),np.array(y)

sc = StandardScaler()
training_data = sc.fit_transform(df['net_station_change'].values.reshape(-1, 1))

trainX, trainY = df_to_X_y(training_data)

#Model Creation
model = keras.Sequential()
model.add(layers.LSTM(32))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(1))
model.build(input_shape=trainX.shape)
model.summary()

#Complile
model.compile(
    loss=keras.losses.MeanSquaredError(),
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.001, momentum=0.9),
    metrics=["mse"],
)

#Fit
batch_size = 4
history = model.fit(
    trainX, trainY, batch_size=batch_size, epochs=10
)

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

