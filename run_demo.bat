@echo off
setlocal
cd /d "%~dp0"
title Lead Engine - Demo Mode

echo ========================================================
echo   Running Lead Engine Demo (Offline Sample)
echo ========================================================
echo.

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe -c "from leadgen import get_vertical, run_pipeline; run_pipeline(get_vertical('web_design'), market='(demo)', demo=True, out_stem='demo_leads')"
) else (
    python -c "from leadgen import get_vertical, run_pipeline; run_pipeline(get_vertical('web_design'), market='(demo)', demo=True, out_stem='demo_leads')"
)

echo.
echo Demo finished! Generated:
echo   - demo_leads_crm.csv
echo   - demo_leads.xlsx
echo.
pause
