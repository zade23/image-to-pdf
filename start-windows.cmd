@echo off
setlocal
title Image to PDF
cd /d "%~dp0"
if errorlevel 1 goto :failed

if not exist ".venv\Scripts\python.exe" goto :setup
".venv\Scripts\python.exe" -c "import streamlit, PIL" >nul 2>&1
if not errorlevel 1 goto :launch

:setup
where uv >nul 2>&1
if errorlevel 1 (
    echo uv is required to prepare the Python environment.
    echo Install uv from https://docs.astral.sh/uv/ and try again.
    goto :failed
)
uv sync --locked
if errorlevel 1 goto :failed

:launch
echo Starting Image to PDF. Your browser will open automatically.
echo Keep this window open while using the app. Close it to stop the app.
".venv\Scripts\python.exe" -m streamlit run app.py --server.address localhost --server.headless false --browser.gatherUsageStats false
if errorlevel 1 goto :failed
exit /b 0

:failed
echo.
echo Could not start the app. Check the error above.
pause
exit /b 1
