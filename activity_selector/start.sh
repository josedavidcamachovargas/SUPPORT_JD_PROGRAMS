#!/usr/bin/env bash
# Activity Selector - Ubuntu/Linux Bash Launcher
# Run this script on Ubuntu/Linux

set -e

echo "🎲 Activity Selector - Starting..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed!"
    echo ""
    echo "Please install Poetry first:"
    echo "  curl -sSL https://install.python-poetry.org | python3 -"
    echo ""
    echo "Then add Poetry to your PATH:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Or visit: https://python-poetry.org/docs/#installation"
    exit 1
fi

# Navigate to project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Installing dependencies (first time setup)..."
    poetry install
fi

# Run the application
echo "🚀 Launching Activity Selector..."
poetry run python run.py
