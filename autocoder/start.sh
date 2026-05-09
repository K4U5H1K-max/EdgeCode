#!/bin/bash

# AutoCoder Startup Script

set -e

echo "Starting AutoCoder..."
echo ""

# Check Python version
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.11+"
    exit 1
fi

# Check Node version
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js 20+"
    exit 1
fi

# Navigate to script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "AutoCoder Root: $SCRIPT_DIR"
echo ""

# Start backend
echo "Starting Backend (FastAPI)..."
cd "$SCRIPT_DIR/backend"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements if needed
if [ ! -f ".env" ]; then
    echo "Setting up .env file..."
    cp .env.example .env
    echo "Please edit backend/.env and add your GROQ_API_KEY"
fi

echo "Starting FastAPI server..."
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"

echo ""
echo "Starting Frontend (Vite)..."
cd "$SCRIPT_DIR/frontend"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

echo "Starting Vite dev server..."
npm run dev &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "=" >&2
echo "AutoCoder is running!" >&2
echo "=" >&2
echo ""
echo "Frontend: http://localhost:5173" >&2
echo "Backend:  http://localhost:8000" >&2
echo "API Docs: http://localhost:8000/docs" >&2
echo ""
echo "Press Ctrl+C to stop" >&2
echo ""

# Wait for user interrupt
wait
