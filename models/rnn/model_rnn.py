#!/usr/bin/env python
# coding: utf-8

# In[1]:


import subprocess
import os 


# In[2]:

current_path = os.path.dirname(os.path.abspath(__file__))
model_rnn_create = os.path.join(current_path, './model_rnn_create.py')


command = ["python", model_rnn_create]
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)


# In[4]:

current_path = os.path.dirname(os.path.abspath(__file__))
model_rnn_test = os.path.join(current_path, './model_rnn_test.py')

command = ["python", model_rnn_test]
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

