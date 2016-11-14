IF NOT EXIST %HOMEPATH%\Miniconda3 Miniconda3-latest-Windows-x86_64.exe
IF NOT EXIST %HOMEPATH%\DietaEstrias conda env create -f environment.yml
set path=%HOMEPATH%\DietaEstrias;%path%;

cd src
python mainTest.py

pause