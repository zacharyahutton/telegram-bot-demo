@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment missing. Run: python -m venv .venv
  echo Then: .venv\Scripts\pip install -r requirements.txt
  pause
  exit /b 1
)
if not exist ".env" (
  echo Copy .env.example to .env and add your TELEGRAM_BOT_TOKEN.
  pause
  exit /b 1
)
echo Starting Tendem Demo Bot... Leave this window open.
".venv\Scripts\python.exe" run_polling.py
echo.
echo Bot stopped. Press any key to close.
pause >nul
