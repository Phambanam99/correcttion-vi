@echo off
chcp 65001 > nul
echo ========================================
echo   Vietnamese Text Corrector - GUI
echo ========================================
echo.

REM Set offline mode
set TRANSFORMERS_OFFLINE=1
set HF_DATASETS_OFFLINE=1

echo 🖥️ Starting Desktop App...
echo.

cd /d "%~dp0"
python main.py

pause
