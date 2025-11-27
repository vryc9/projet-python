#!/bin/bash
# Helper script to run the Music Analysis Pipeline using the cross-platform runner

# Ensure we are in the project root
cd "$(dirname "$0")"

# Check if python3 is available
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python is not installed or not in PATH."
    exit 1
fi

# Run the Python runner script
$PYTHON_CMD run.py
