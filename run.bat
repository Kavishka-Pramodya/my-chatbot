@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
title AI Chatbot Runner
color 0B

echo ========================================================
echo             🤖 Starting AI Chatbot Server
echo ========================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python is not installed or not added to your system PATH!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Python detected.
echo [2/3] Checking and installing dependencies...
pip install -r requirements.txt --quiet

echo [3/3] Launching Chatbot in your browser...
start http://127.0.0.1:8000

echo.
echo ========================================================
echo Server running at: http://127.0.0.1:8000
echo API Docs at:       http://127.0.0.1:8000/docs
echo Keep this window open while using the chatbot.
echo Press Ctrl + C to stop the server.
echo ========================================================
echo.

python backend\main.py

pause
