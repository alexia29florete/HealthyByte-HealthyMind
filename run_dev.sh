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

# pornește frontend
cd frontend
python3 app.py
