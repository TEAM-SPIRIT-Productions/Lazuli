:: This script allows the user to launch the tests without needing use command line
@ECHO off
echo "This script will start Project Lazuli's test sequence."
echo "Note: The PyTest module is required for this sequence."
echo "Note: Test files must be put in the repository root, for this sequence."
echo "Starting up virtual environment..."
call pypi\scripts\activate.bat
echo "Attempting to test the capabilities of Lazuli..."
py.test
echo "Test concluded."
pause