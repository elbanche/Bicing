import subprocess
import os 
from pathlib import Path

root = Path(__file__).parents[2]
config_path = os.path.join(root, 'config.json')

model_rnn_create = os.path.join(root, 'models', 'rnn', 'model_rnn_create.py')
model_rnn_test = os.path.join(root, 'models', 'rnn', 'model_rnn_test.py')

command = ["python", model_rnn_create]
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

command = ["python", model_rnn_test]
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

