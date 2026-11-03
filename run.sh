#!/bin/bash
set -e

echo "========================================================"
echo "Starting AccountIQ - Enterprise Intelligence Platform"
echo "========================================================"

# 1. Virtual environment setup
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r backend/requirements.txt
fi

# 2. Frontend packages
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install --prefix frontend
fi

# 3. Start services
echo "Starting Backend API on http://127.0.0.1:8000 ..."
./venv/bin/python backend/run.py &
BACKEND_PID=$!

echo "Starting Frontend UI on http://localhost:3000 ..."
npm run dev --prefix frontend &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT

echo "========================================================"
echo "AccountIQ is running!"
echo "Access Web UI:   http://localhost:3000"
echo "Access API Docs: http://127.0.0.1:8000/docs"
echo "Press Ctrl+C to terminate both servers."
echo "========================================================"

wait
