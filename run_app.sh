#!/bin/bash
cd "$(dirname "$0")"
echo "Starting FastAPI server..."
./.venv/bin/python -m uvicorn main:app --reload --reload-dir . --host 127.0.0.1 --port 8000 &
sleep 2
echo "Opening browser at http://127.0.0.1:8000"
if command -v xdg-open > /dev/null; then
    xdg-open http://127.0.0.1:8000
elif command -v open > /dev/null; then
    open http://127.0.0.1:8000
fi
