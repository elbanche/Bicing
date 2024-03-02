#!/bin/bash

echo "Ejecutando generate_station_csv.py"
echo "Hora de inicio: $(date)"
python3 ./data/generate_station_csv.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando resample_csv.py"
echo "Hora de inicio: $(date)"
python3 ./data/resample_csv.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando split_train_test.py"
echo "Hora de inicio: $(date)"
python3 ./data/split_train_test.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando model_dummy.py"
echo "Hora de inicio: $(date)"
python3 ./models/dummy/model_dummy.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando model_avg.py"
echo "Hora de inicio: $(date)"
python3 ./models/avg/model_avg.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando model_rnn.py"
echo "Hora de inicio: $(date)"
python3 ./models/rnn/model_rnn.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando model_rnn_by_time.py"
echo "Hora de inicio: $(date)"
python3 ./models/rnn_by_time/model_rnn_by_time.py
echo "Hora de finalización: $(date)"
echo
