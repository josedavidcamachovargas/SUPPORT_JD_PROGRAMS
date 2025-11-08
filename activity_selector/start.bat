@echo off
REM Activity Selector - Windows Batch Launcher
REM This .bat file works without execution policy issues!

echo Starting Activity Selector...
echo.

REM Check if Poetry is installed
python -m poetry --version >nul 2>&1
if %errorlevel% neq 0 (
    poetry --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Poetry is not installed!
        echo.
        echo Please run setup.bat first, or install Poetry:
        echo   python -m pip install poetry
        echo.
        echo Then run this script again.
        pause
        exit /b 1
    )
)

REM Navigate to project directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv" (
    echo [WARNING] Dependencies not installed!
    echo.
    echo Please run setup.bat first, or run:
    echo   python -m poetry install
    echo.
    pause
    exit /b 1
)

REM Run the application
python -m poetry run python run.py

REM If there was an error, pause so user can see it
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application exited with an error.
    pause
)
