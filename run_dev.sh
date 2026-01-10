#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# venv
source .venv/bin/activate

# pornește backend
( cd backend && python3 main.py ) &
BACK_PID=$!

# oprește backend când ieși din frontend
trap "kill $BACK_PID 2>/dev/null || true" EXIT

# AȘTEAPTĂ ca backend-ul să fie gata (verifică dacă portul 8000 răspunde)
echo "Waiting for backend to start..."
for i in {1..30}; do
  if curl -s http://127.0.0.1:8000 > /dev/null 2>&1; then
    echo "Backend is ready!"
    break
  fi
  echo "Waiting... ($i/30)"
  sleep 1
done

# pornește frontend
cd frontend
python3 app.py
