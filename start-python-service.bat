@echo off
echo Starting Python PDF Intelligence Service...
cd /d "%~dp0service"
call venv\Scripts\activate.bat
python app.py
pause
