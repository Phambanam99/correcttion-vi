@echo off
chcp 65001 > nul
echo ========================================
echo   Vietnamese Text Corrector - Web
echo ========================================
echo.

REM Start web server
echo 🌐 Starting Web Server...
echo 📍 Open browser: http://localhost:8080
echo.
echo Press Ctrl+C to stop
echo.

cd /d "%~dp0web"
python -m http.server 8080

pause
