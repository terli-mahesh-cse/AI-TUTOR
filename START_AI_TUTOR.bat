@echo off
title AI-Tutor - AI Powered Tutoring Platform
cd /d "%~dp0"

echo ========================================================
echo                 STARTING AI-TUTOR                       
echo ========================================================
echo.

:: Check if python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not found in your PATH.
    echo Please ensure Python is installed.
    pause
    exit /b
)

:: Ensure database is seeded
echo [1/3] Checking database...
python seed.py

:: Open the browser after a short 1.5 second delay
echo [2/3] Opening browser at http://localhost:8000 ...
start "" "http://localhost:8000"

:: Start Uvicorn Server
echo [3/3] Starting web server on http://localhost:8000 ...
echo.
echo ========================================================
echo   AI-Tutor is running!
echo   Website: http://localhost:8000
echo.
echo   Press CTRL+C or close this window to stop the server.
echo ========================================================
echo.

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
