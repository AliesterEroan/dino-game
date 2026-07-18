@echo off
echo ========================================
echo Dino Jump Game Launcher
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    echo Please install Python from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [INFO] Python found
echo [INFO] Installing dependencies...
pip install -r backend\requirements.txt

echo [INFO] Starting Dino Jump Game...
echo.
cd backend
python game.py
