rem echo off
rem Generate API docs
echo Now re-generating API Docs...
call venv\scripts\activate.bat
call portray on_github_pages -mo lazuli
echo API Docs pushed to GitHub Pages!
call venv\scripts\deactivate.bat

rem Build & Distribute
echo Now building the distribution archives...
python setup.py sdist bdist_wheel
echo Now uploading the distribution archives...
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*

echo Sequence completed!
pause