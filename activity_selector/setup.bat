@echo off
REM Activity Selector - Windows Batch Setup Script
REM This .bat file works without execution policy issues!

echo ========================================
echo    Activity Selector - Setup Wizard
echo ========================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check 'Add Python to PATH' during installation!
    pause
    exit /b 1
)

python --version
echo [OK] Python found!
echo.

REM Check if Poetry is installed
echo Checking Poetry installation...
python -m poetry --version >nul 2>&1
if %errorlevel% neq 0 (
    poetry --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [WARNING] Poetry is not installed!
        echo.
        set /p install_poetry="Would you like to install Poetry now? (y/n): "
        
        if /i "%install_poetry%"=="y" (
            echo Installing Poetry...
            python -m pip install poetry
            if %errorlevel% neq 0 (
                echo [ERROR] Failed to install Poetry!
                echo Please install manually: https://python-poetry.org/docs/#installation
                pause
                exit /b 1
            )
            echo [OK] Poetry installed successfully!
        ) else (
            echo.
            echo Poetry is required to continue.
            echo Install it with: python -m pip install poetry
            pause
            exit /b 1
        )
    )
)

REM Show Poetry version
python -m poetry --version >nul 2>&1
if %errorlevel% equ 0 (
    python -m poetry --version
) else (
    poetry --version
)
echo [OK] Poetry found!
echo.

REM Navigate to project directory
cd /d "%~dp0"

REM Install dependencies
echo Installing project dependencies...
python -m poetry install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully!
echo.

REM Check for data files
echo Checking data files...

if not exist "activities_data.yml" (
    if exist "activities_data_example.yml" (
        echo [WARNING] activities_data.yml not found. Creating from example...
        copy "activities_data_example.yml" "activities_data.yml" >nul
        echo [OK] Created activities_data.yml
    ) else (
        echo [WARNING] No activity data found. You'll need to add activities manually.
    )
) else (
    echo [OK] activities_data.yml found
)

if not exist "config.yml" (
    echo [INFO] config.yml will be created on first run
) else (
    echo [OK] config.yml found
)

echo.

REM Check image cache directory
if not exist "image_cache" (
    echo Creating image_cache directory...
    mkdir "image_cache"
    echo [OK] image_cache directory created
) else (
    echo [OK] image_cache directory exists
)

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   start.bat
echo.
echo Or manually:
echo   poetry run python run.py
echo.

set /p run_now="Would you like to run the application now? (y/n): "
if /i "%run_now%"=="y" (
    echo.
    echo Launching Activity Selector...
    echo.
    python -m poetry run python run.py
)

pause
