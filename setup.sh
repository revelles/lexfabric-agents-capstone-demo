#!/usr/bin/env bash
set -e

echo "[1] Creating virtual environment..."
python3 -m venv .venv

echo "[2] Activating environment..."
source .venv/bin/activate

echo "[3] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[4] Setting PYTHONPATH..."
export PYTHONPATH="$PWD/src"

echo "[5] Done!"
echo "Run: source .venv/bin/activate"
