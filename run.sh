#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
REQ=requirements.txt
ls backend/models/*.keras >/dev/null 2>&1 && REQ=requirements-keras.txt
pip install --quiet --upgrade pip
pip install --quiet -r "$REQ"
echo "Starting Customer Review Analyzer at http://127.0.0.1:8000"
python app.py
