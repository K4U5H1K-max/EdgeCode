@echo off

REM AutoCoder Startup Script for Windows

echo Starting AutoCoder...
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.11+
    exit /b 1
)

REM Check Node version
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed. Please install Node.js 20+
    exit /b 1
)

REM Navigate to script directory
cd /d "%~dp0"

echo AutoCoder Root: %cd%
echo.

REM Start backend
echo Starting Backend (FastAPI)...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements if needed
if not exist ".env" (
    echo Setting up .env file...
    copy .env.example .env
    echo Please edit backend\.env and add your GROQ_API_KEY
)

echo Starting FastAPI server...
start cmd /k "call venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --port 8000"

echo.
echo Starting Frontend (Vite)...
cd ..\frontend

REM Install dependencies if needed
if not exist "node_modules" (
    echo Installing npm dependencies...
    call npm install
)

echo Starting Vite dev server...
start cmd /k "npm run dev"

echo.
echo ====================================
echo AutoCoder is running!
echo ====================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Check the command windows for logs
echo.
pause
