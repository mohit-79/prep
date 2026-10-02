#!/usr/bin/env bash
# SQL Final Prep Tracker Launcher for Linux / macOS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo " Starting SQL Final Prep Tracker (Linux)  "
echo "=========================================="

if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python 3 is required but was not found in PATH." >&2
    echo "Please install python3 (e.g. sudo apt install python3) and try again." >&2
    exit 1
fi

"$PYTHON_CMD" server.py
