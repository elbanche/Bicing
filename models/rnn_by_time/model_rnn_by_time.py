#!/usr/bin/env python
# coding: utf-8

# In[1]:
import subprocess
from datetime import datetime, timedelta
import os 
import json

current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, '../../config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

model_rnn_by_time_create = os.path.join(current_path, './model_rnn_by_time_create.py')
model_rnn_by_time_test = os.path.join(current_path, './model_rnn_by_time_test.py')


# In[2]:


iter = datetime.strptime('00:00', '%H:%M')
while iter <= datetime.strptime('23:30', '%H:%M'):
    time_of_the_day = iter.strftime('%H:%M')
    print("TIME OF THE DAY: " + time_of_the_day)

    command = ["python", model_rnn_by_time_create, "--time_of_the_day", time_of_the_day]
    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)
    
    iter += timedelta(minutes=config['minutes_inc'])


# In[3]:


command = ["python", model_rnn_by_time_test]
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

