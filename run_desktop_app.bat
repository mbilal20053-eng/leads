@echo off
setlocal
cd /d "%~dp0"
title Lead Engine - Desktop App

if exist "dist\LeadEngine.exe" (
    echo Starting Lead Engine Desktop App...
    start "" "dist\LeadEngine.exe"
    exit /b 0
)

if exist ".venv\Scripts\python.exe" (
    echo Starting Lead Engine via Python virtual environment...
    start "" .venv\Scripts\python.exe gui\launch.py
    exit /b 0
)

python gui\launch.py
pause
