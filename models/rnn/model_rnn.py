#!/usr/bin/env python
# coding: utf-8

# In[1]:


import subprocess


# In[ ]:


command = ["python", "model_rnn_create.py"]
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)


# In[3]:


command = ["python", "model_rnn_test.py"]
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

