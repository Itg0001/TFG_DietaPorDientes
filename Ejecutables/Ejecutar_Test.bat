cd ..
REM IF NOT EXIST %HOMEPATH%\Miniconda3 Miniconda3-latest-Windows-x86_64.exe

IF NOT EXIST %HOMEPATH%\Miniconda3\envs\DietaEstrias conda env create -f %cd%\environment.yml


set path=%HOMEPATH%\Miniconda3\envs\DietaEstrias; %path%;

cd src
python mainTest.py

pause