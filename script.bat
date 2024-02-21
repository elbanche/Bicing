@echo off

echo Ejecutando generate_station_csv.py
echo Hora de inicio: %TIME%
python .\data\generate_station_csv.py
echo Hora de finalización: %TIME%
echo.

echo Ejecutando resample_csv.py
echo Hora de inicio: %TIME%
python .\data\resample_csv.py
echo Hora de finalización: %TIME%
echo.

echo Ejecutando split_train_test.py
echo Hora de inicio: %TIME%
python .\data\split_train_test.py
echo Hora de finalización: %TIME%
echo.

echo Ejecutando model_dummy.py
echo Hora de inicio: %TIME%
python .\models\dummy\model_dummy.py
echo Hora de finalización: %TIME%
echo.

echo Ejecutando model_avg.py
echo Hora de inicio: %TIME%
python .\models\avg\model_avg.py
echo Hora de finalización: %TIME%
echo.

echo Ejecutando model_rnn.py
echo Hora de inicio: %TIME%
python .\models\rnn\model_rnn.py
echo Hora de finalización: %TIME%
echo.

echo Ejecutando model_rnn_by_time.py
echo Hora de inicio: %TIME%
python .\models\rnn_by_time\model_rnn_by_time.py
echo Hora de finalización: %TIME%
echo.
