echo off

rem ----------------------------------------------------------
rem Allow user to choose which virtual environment to set up
setlocal

echo This script will set up your virtual environment.
echo Do not close this window until you are told to do so!
echo Please select which virtual environment to set up:
echo A: Environment for using Lazuli
echo B: Environment for testing/distributing Lazuli
choice /c AB /t 10 /d A /m "What is your choice"
if errorlevel 2 call :distrubute
if errorlevel 1 call :use

pause
endlocal
rem ----------------------------------------------------------

:: function to run from choice A
:use
echo You have selected A: Environment for *USING* Lazuli

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

EXIT /B 0

rem ----------------------------------------------------------

:: function to run from choice B
:distrubute
echo You have selected B: Environment for testing/distributing Lazuli

echo Generating pypi folder...
rem Generate VENV in project dir
Python -m venv %~dp0pypi

echo Installing dependencies...
rem Activate the VENV
call pypi\scripts\activate.bat

rem Install requirements
pip install wheel
pip install -r contributor_requirements.txt
echo Sequence completed! You may now close this window:
pause

EXIT