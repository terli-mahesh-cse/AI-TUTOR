@echo off
title AI-Tutor - Live Public Tunnel
cd /d "%~dp0"

echo ========================================================
echo             AI-TUTOR: GOING LIVE ONLINE                 
echo ========================================================
echo.

:: Ensure app dependencies and seed
echo [1/3] Verifying database...
python seed.py

:: Start local server in background if not already running
echo [2/3] Checking local web server on port 8000...
powershell -Command "if (!(Test-NetConnection -ComputerName 127.0.0.1 -Port 8000 -InformationLevel Quiet)) { Start-Process python -ArgumentList '-m uvicorn app.main:app --host 127.0.0.1 --port 8000' -WindowStyle Minimized }"

:: Generate instant public HTTPS URL
echo [3/3] Generating public live HTTPS URL...
echo.
echo Your public IP password for localtunnel (if prompted by tunnel page):
curl -s https://loca.lt/mytunnelpassword
echo.
echo ========================================================
echo  Your live website link will appear below:
echo ========================================================
echo.

npx localtunnel --port 8000
pause
