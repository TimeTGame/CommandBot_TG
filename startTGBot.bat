@echo off

set VENV_PATH=./.venv
set PYTHON_PATH=%VENV_PATH%/Scripts/python.exe
set REQUIREMENTS=./requirements.txt
cd /d "%~dp0"

if not exist "%VENV_PATH%" (
    echo If you read it, we create virtual environment for our bot
    echo Creating virtual environment...    
    python -m venv .venv
    echo Virtual environment created!
    
    call "%VENV_PATH%/Scripts/activate.bat"
    if exist "%REQUIREMENTS%" (
        echo Installing requirements...
        pip install -r "%REQUIREMENTS%"
    )
)

start /min %VENV_PATH%/Scripts/pythonw.exe ./run.py
