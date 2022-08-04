rem This script generates API docs and pushes them to GitHub, as well as builds
rem and pushes builds to PyPi
rem @author KOOKIIE
echo off
call venv\scripts\activate.bat
rem Generate API docs
echo Now re-generating API Docs...
call portray on_github_pages -mo lazuli
echo API Docs pushed to GitHub Pages!

rem Build & Distribute
echo Now building the distribution archives...
python setup.py sdist bdist_wheel
echo Now uploading the distribution archives...
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*

call venv\scripts\deactivate.bat
echo Sequence completed!
pause