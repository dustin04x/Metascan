@echo off
REM MetaScan Quick Start for Windows

echo.
echo ========================================
echo   MetaScan - Image Forensics Inspector
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org
    pause
    exit /b 1
)

REM Note: Node.js is optional (only needed if npm install fails)
REM We can serve files without it if needed

echo [1/4] Setting up backend...
cd /d "%~dp0backend"
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo Installing backend dependencies...
pip install -q -r requirements.txt
echo Backend ready!

echo.
echo [2/4] Setting up frontend (vanilla HTML/CSS/JS - no React!)...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install -q
)
echo Frontend ready!

echo.
echo [3/4] Starting backend...
cd /d "%~dp0backend"
call venv\Scripts\activate.bat
start cmd /k "python -m uvicorn app:app --host 127.0.0.1 --port 8000"
timeout /t 3

echo.
echo [4/4] Starting frontend...
cd /d "%~dp0frontend"
start cmd /k "npm run dev"

echo.
echo ========================================
echo   MetaScan is starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press any key to close this window...
pause
