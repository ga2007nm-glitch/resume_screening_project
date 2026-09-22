@echo off
cd /d "%~dp0"
echo Starting FastAPI server in a new terminal...
start "" ".\.venv\Scripts\python.exe" -m uvicorn main:app --reload --reload-dir . --host 127.0.0.1 --port 8000

echo Opening Microsoft Edge at http://127.0.0.1:8000
start "" "msedge" "http://127.0.0.1:8000"
exit /b 0
