#!/bin/bash

echo "Ejecutando generate_station_csv.py"
echo "Hora de inicio: $(date)"
python ./data/generate_station_csv.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando resample_csv.py"
echo "Hora de inicio: $(date)"
python ./data/resample_csv.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando split_train_test.py"
echo "Hora de inicio: $(date)"
python ./data/split_train_test.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando model_dummy.py"
echo "Hora de inicio: $(date)"
python ./models/dummy/model_dummy.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando model_avg.py"
echo "Hora de inicio: $(date)"
python ./models/avg/model_avg.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando model_rnn.py"
echo "Hora de inicio: $(date)"
python ./models/rnn/model_rnn.py
echo "Hora de finalización: $(date)"
echo

echo "Ejecutando model_rnn_by_time.py"
echo "Hora de inicio: $(date)"
python ./models/rnn_by_time/model_rnn_by_time.py
echo "Hora de finalización: $(date)"
echo
