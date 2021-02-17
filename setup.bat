echo off
echo Setting up virtual environment, please wait!
echo Do not close this window until you are told to do so!

echo Generating venv folder...
rem Generate VENV in project dir
Python -m venv %~dp0venv

echo Installing dependencies...
rem Activate the VENV
call venv\scripts\activate.bat

rem Install requirements
pip install wheel
pip install -r requirements.txt
echo Sequence completed! You may now close this window:
pause