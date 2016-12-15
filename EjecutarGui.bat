
IF NOT EXIST %HOMEPATH%\Miniconda3\envs\DietaEstrias conda env create -f %cd%\environment.yml


set path=%HOMEPATH%\Miniconda3\envs\DietaEstrias; %path%;
cd src
python main.py

pause