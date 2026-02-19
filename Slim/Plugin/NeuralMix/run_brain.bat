@echo off
cd python
if not exist "venv" (
    echo Creating Python Virtual Environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing AI Dependencies (This may take a while)...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo Starting NeuralMix Brain...
python server.py
