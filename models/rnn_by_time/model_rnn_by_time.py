import subprocess
from datetime import datetime, timedelta
import os 
import json
from pathlib import Path

root = Path(__file__).parents[2]
config_path = os.path.join(root, 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

model_rnn_by_time_create = os.path.join(root, 'models', 'rnn_by_time', 'model_rnn_by_time_create.py')
model_rnn_by_time_test = os.path.join(root, 'models', 'rnn_by_time', 'model_rnn_by_time_test.py')

iter = datetime.strptime('00:00', '%H:%M')
while iter <= datetime.strptime('23:30', '%H:%M'):
    time_of_the_day = iter.strftime('%H:%M')
    print("TIME OF THE DAY: " + time_of_the_day)

    command = ["python3", model_rnn_by_time_create, "--time_of_the_day", time_of_the_day]
    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)
    
    iter += timedelta(minutes=config['minutes_inc'])

command = ["python3", model_rnn_by_time_test]
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

