@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1

if not exist .venv (
  echo Creating virtual environment...
  python -m venv .venv || goto :fail
)
call .venv\Scripts\activate.bat

rem Use the Keras requirements if a model file is present, otherwise the light install.
set REQ=requirements.txt
dir /b backend\models\*.keras >nul 2>&1 && set REQ=requirements-keras.txt

echo Installing dependencies from %REQ% (first run only takes a while)...
python -m pip install --quiet --upgrade pip
pip install --quiet -r %REQ% || goto :fail

echo.
echo Starting Customer Review Analyzer at http://127.0.0.1:8000
start "" http://127.0.0.1:8000
python app.py
goto :eof

:fail
echo.
echo Setup failed. Make sure Python 3.10+ is installed and on PATH.
pause
