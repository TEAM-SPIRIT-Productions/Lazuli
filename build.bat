rem This script builds lazulim and pushes the builds to PyPi
rem @author KOOKIIE
echo off
call pypi\scripts\activate.bat

echo Please select which repository to publish to:
echo A: Build and publish to TestPyPi (Test)
echo B: Only publish to PyPi (Production)
choice /c AB /t 10 /d A /m "What is your choice"
if errorlevel 2 call :production
if errorlevel 1 call :test

:: function to run from choice A
:test
echo You have selected A: Build and publish to TestPyPi (Test)
echo Now building the distribution archives...
python -m build
echo Now uploading the distribution archives...
python -m twine upload --repository testpypi dist/*
call venv\scripts\deactivate.bat
echo Sequence completed!
pause

EXIT /B 0

:: function to run from choice B
:production
echo You have selected B: Only publish to PyPi (Production)
echo Now uploading the distribution archives...
python -m twine upload dist/*
call venv\scripts\deactivate.bat
echo Sequence completed!
pause