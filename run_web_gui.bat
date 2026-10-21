@echo off
setlocal
cd /d "%~dp0"
title Lead Engine - Web Interface

echo ========================================================
echo   Lead Engine Web Interface
echo ========================================================
echo.
echo Opening browser to http://127.0.0.1:5000 ...
start "" http://127.0.0.1:5000

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe gui\app.py
) else (
    python gui\app.py
)

pause
