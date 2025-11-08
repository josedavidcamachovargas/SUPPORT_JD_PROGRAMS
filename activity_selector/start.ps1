# Activity Selector - Windows PowerShell Launcher
# Run this script on Windows

Write-Host "🎲 Activity Selector - Starting..." -ForegroundColor Cyan

# Check if Poetry is installed
$poetryInstalled = Get-Command poetry -ErrorAction SilentlyContinue

if (-not $poetryInstalled) {
    Write-Host "❌ Poetry is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Poetry first:" -ForegroundColor Yellow
    Write-Host "  1. Open PowerShell as Administrator" -ForegroundColor White
    Write-Host "  2. Run: (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -" -ForegroundColor White
    Write-Host "  3. Close and reopen PowerShell" -ForegroundColor White
    Write-Host ""
    Write-Host "Or visit: https://python-poetry.org/docs/#installation" -ForegroundColor Cyan
    exit 1
}

# Navigate to project directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Installing dependencies (first time setup)..." -ForegroundColor Yellow
    poetry install
}

# Run the application
Write-Host "🚀 Launching Activity Selector..." -ForegroundColor Green
poetry run python run.py
