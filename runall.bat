@echo off
echo Activating virtual environment...
call .venv\Scripts\activate

echo Starting BACKEND on port 8080...
start cmd /k "uvicorn app.main:app --reload --port 8080"

echo Starting FRONTEND on port 8000...
start cmd /k "uvicorn ui.app:app --reload --port 8000"

echo Both servers started.
