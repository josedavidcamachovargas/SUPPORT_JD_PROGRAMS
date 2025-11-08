# Activity Selector - Cross-Platform Setup Script
# This PowerShell script works on Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Activity Selector - Setup Wizard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "🐍 Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.8 or higher from:" -ForegroundColor Yellow
    Write-Host "  https://www.python.org/downloads/" -ForegroundColor White
    Write-Host ""
    Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check if Poetry is installed
Write-Host "📦 Checking Poetry installation..." -ForegroundColor Yellow
$poetryInstalled = Get-Command poetry -ErrorAction SilentlyContinue

if ($poetryInstalled) {
    $poetryVersion = poetry --version
    Write-Host "✅ Poetry found: $poetryVersion" -ForegroundColor Green
} else {
    Write-Host "⚠️  Poetry is not installed!" -ForegroundColor Yellow
    Write-Host ""
    $installPoetry = Read-Host "Would you like to install Poetry now? (y/n)"
    
    if ($installPoetry -eq "y" -or $installPoetry -eq "Y") {
        Write-Host "📥 Installing Poetry..." -ForegroundColor Cyan
        try {
            (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
            Write-Host "✅ Poetry installed successfully!" -ForegroundColor Green
            Write-Host ""
            Write-Host "⚠️  Please close and reopen PowerShell, then run this script again." -ForegroundColor Yellow
            exit 0
        } catch {
            Write-Host "❌ Failed to install Poetry automatically." -ForegroundColor Red
            Write-Host "Please install manually: https://python-poetry.org/docs/#installation" -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host ""
        Write-Host "Poetry is required to continue. Install it manually:" -ForegroundColor Yellow
        Write-Host "  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -" -ForegroundColor White
        exit 1
    }
}

Write-Host ""

# Navigate to project directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Install dependencies
Write-Host "📦 Installing project dependencies..." -ForegroundColor Cyan
poetry install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check for data files
Write-Host "📄 Checking data files..." -ForegroundColor Yellow

if (-not (Test-Path "activities_data.yml")) {
    if (Test-Path "activities_data_example.yml") {
        Write-Host "⚠️  activities_data.yml not found. Creating from example..." -ForegroundColor Yellow
        Copy-Item "activities_data_example.yml" "activities_data.yml"
        Write-Host "✅ Created activities_data.yml" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No activity data found. You'll need to add activities manually." -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ activities_data.yml found" -ForegroundColor Green
}

if (-not (Test-Path "config.yml")) {
    Write-Host "ℹ️  config.yml will be created on first run" -ForegroundColor Cyan
} else {
    Write-Host "✅ config.yml found" -ForegroundColor Green
}

Write-Host ""

# Check image cache directory
if (-not (Test-Path "image_cache")) {
    Write-Host "📁 Creating image_cache directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "image_cache" -Force | Out-Null
    Write-Host "✅ image_cache directory created" -ForegroundColor Green
} else {
    Write-Host "✅ image_cache directory exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   ✅ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "  .\start.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Or manually:" -ForegroundColor Cyan
Write-Host "  poetry run python run.py" -ForegroundColor White
Write-Host ""

# Ask if user wants to run now
$runNow = Read-Host "Would you like to run the application now? (y/n)"
if ($runNow -eq "y" -or $runNow -eq "Y") {
    Write-Host ""
    Write-Host "🚀 Launching Activity Selector..." -ForegroundColor Green
    Write-Host ""
    poetry run python run.py
}
