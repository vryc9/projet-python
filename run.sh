#!/bin/bash
# Helper script to run the Music Analysis Pipeline using the local virtual environment

# Ensure we are in the project root
cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "my_env" ]; then
    echo "Virtual environment 'my_env' not found. Creating it..."
    python3 -m venv my_env
    ./my_env/bin/pip install -r music_analysis/requirements.txt
fi

# Run the pipeline
echo "Running Music Analysis Pipeline..."
./my_env/bin/python music_analysis/main.py
