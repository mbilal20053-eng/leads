@echo off
setlocal
cd /d "%~dp0"

if "%~1"=="" (
    echo ========================================================
    echo   Lead Engine CLI
    echo ========================================================
    echo.
    echo Usage:
    echo   run_cli.bat --list
    echo   run_cli.bat --vertical web_design --country Canada --city Toronto --limit 10 --out toronto_leads
    echo   run_cli.bat --vertical web_design --country "United States" --state Texas --city Austin --limit 10
    echo   run_cli.bat --vertical web_design --market "London, UK" --sources overture --limit 10
    echo   run_cli.bat --help
    echo.
    if exist ".venv\Scripts\python.exe" (
        .venv\Scripts\python.exe -m leadgen --list
    ) else (
        python -m leadgen --list
    )
    exit /b 0
)

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe -m leadgen %*
) else (
    python -m leadgen %*
)
