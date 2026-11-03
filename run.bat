@echo off
echo ========================================================
echo Starting AccountIQ - Enterprise Intelligence Platform
echo ========================================================

REM 1. Check Python and venv
if not exist "venv\Scripts\python.exe" (
    echo Creating Python virtual environment...
    python -m venv venv
    call venv\Scripts\pip.exe install -r backend\requirements.txt
)

REM 2. Check Node and frontend packages
if not exist "frontend\node_modules" (
    echo Installing frontend packages...
    call npm install --prefix frontend
)

REM 3. Run Backend and Frontend
echo Starting Backend API on http://127.0.0.1:8000 ...
start "AccountIQ Backend" cmd /k "venv\Scripts\python.exe backend\run.py"

echo Starting Frontend on http://localhost:3000 ...
start "AccountIQ Frontend" cmd /k "npm run dev --prefix frontend"

echo ========================================================
echo AccountIQ is running!
echo Access Web UI:   http://localhost:3000
echo Access API Docs: http://127.0.0.1:8000/docs
echo ========================================================
