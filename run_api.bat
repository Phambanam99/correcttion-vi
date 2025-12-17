@echo off
chcp 65001 > nul
echo ========================================
echo   Vietnamese Text Corrector - API
echo ========================================
echo.

REM Fix HuggingFace cache symlinks issue on Windows
set HF_HOME=C:\Users\System Interlace\.cache\huggingface
set TRANSFORMERS_CACHE=%HF_HOME%\hub
set HF_HUB_DISABLE_SYMLINKS_WARNING=1

REM Uncomment below to use offline mode (sau khi đã tải models)
REM set TRANSFORMERS_OFFLINE=1
REM set HF_DATASETS_OFFLINE=1

echo 🚀 Starting API Server...
echo 📍 API will be available at: http://localhost:5000
echo 🌐 Web interface: http://localhost:8080
echo.
echo Press Ctrl+C to stop
echo.

cd /d "%~dp0"
python api/app.py

pause
