@echo off
chcp 65001 > nul
echo ========================================
echo   Vietnamese Text Corrector - API
echo ========================================
echo.

REM Set offline mode - không tải từ internet
set TRANSFORMERS_OFFLINE=1
set HF_DATASETS_OFFLINE=1

REM Set HuggingFace cache path (nếu models ở thư mục khác)
REM set HF_HOME=%~dp0..\models

echo 🚀 Starting API Server...
echo 📍 API will be available at: http://localhost:5000
echo 🌐 Web interface: http://localhost:8080
echo.
echo Press Ctrl+C to stop
echo.

cd /d "%~dp0"
python api/app.py

pause
