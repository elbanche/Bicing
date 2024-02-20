#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append("../..")

import subprocess
from datetime import datetime, timedelta
import config


# In[2]:


iter = datetime.strptime('00:00', '%H:%M')
while iter <= datetime.strptime('23:30', '%H:%M'):
    time_of_the_day = iter.strftime('%H:%M')
    print("TIME OF THE DAY: " + time_of_the_day)

    command = ["python", "model_rnn_by_time_create.py", "--time_of_the_day", time_of_the_day]
    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)
    
    iter += timedelta(minutes=config.minutes_inc)


# In[ ]:


command = ["python", "model_rnn_by_time_test.py"]
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

