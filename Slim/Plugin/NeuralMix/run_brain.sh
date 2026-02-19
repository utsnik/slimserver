#!/bin/bash

# Navigate to script directory
cd "$(dirname "$0")/python"

# Create Venv if missing
if [ ! -d "venv" ]; then
    echo "Creating Python Virtual Environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing AI Dependencies for ARM/Linux..."
    # specialized install for Pi often helps, but standard pip is usually fine for these libs
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "Starting NeuralMix Brain..."
python3 server.py
