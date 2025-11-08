# 📦 Poetry Setup & Installation Guide

## Overview

This project now uses **Poetry** for dependency management, providing a modern, reliable, and cross-platform solution for managing Python dependencies and virtual environments.

## ✨ Benefits of Poetry

- 🎯 **Single source of truth** - All dependencies in `pyproject.toml`
- 🔒 **Lock file** - Reproducible builds with `poetry.lock`
- 🌍 **Cross-platform** - Works seamlessly on Windows and Ubuntu/Linux
- 🚀 **Easy to use** - Simple commands for all operations
- 📦 **Virtual environment management** - Automatic isolation
- 🔧 **Dev dependencies** - Separate development tools

---

## 🚀 Quick Start

### Windows (PowerShell)

```powershell
# Run the PowerShell launcher
.\start.ps1
```

### Ubuntu/Linux (Bash)

```bash
# Make the script executable (first time only)
chmod +x start.sh

# Run the Bash launcher
./start.sh
```

### Cross-Platform (with Poetry installed)

```bash
# Install dependencies
poetry install

# Run the application
poetry run python run.py
```

---

## 📥 Installing Poetry

### Windows

**Option 1: PowerShell (Recommended)**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

**Option 2: Using pip**
```powershell
pip install poetry
```

After installation, close and reopen PowerShell.

### Ubuntu/Linux

**Option 1: Official Installer (Recommended)**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Option 2: Using pip**
```bash
pip install poetry
```

After installation, add Poetry to your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add this line to your `~/.bashrc` or `~/.zshrc` to make it permanent.

### Verify Installation

```bash
poetry --version
```

You should see something like: `Poetry (version 1.7.1)`

---

## 🛠️ Project Setup

### First Time Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/josedavidcamachovargas/SUPPORT_JD_PROGRAMS.git
   cd SUPPORT_JD_PROGRAMS/activity_selector
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```
   
   This creates a virtual environment and installs all dependencies.

3. **Activate the virtual environment** (optional):
   ```bash
   poetry shell
   ```

4. **Run the application**:
   ```bash
   poetry run python run.py
   ```

### Using Launcher Scripts

**Windows:**
```powershell
.\start.ps1
```

**Ubuntu/Linux:**
```bash
./start.sh
```

These scripts automatically check for Poetry, install dependencies if needed, and launch the app!

---

## 📋 Common Commands

### Running the Application

```bash
# Using Poetry
poetry run python run.py

# Or with launcher scripts
./start.sh        # Linux/Ubuntu
.\start.ps1       # Windows

# Or using Makefile
make run
```

### Managing Dependencies

```bash
# Install all dependencies
poetry install

# Install only production dependencies
poetry install --no-dev

# Add a new dependency
poetry add package-name

# Add a development dependency
poetry add --group dev package-name

# Update dependencies
poetry update

# Show installed packages
poetry show

# Export to requirements.txt (if needed)
poetry export -f requirements.txt --output requirements.txt
```

### Development Commands

```bash
# Run tests
poetry run pytest
# or
make test

# Format code with Black
poetry run black .
# or
make format

# Lint code
poetry run flake8 .
poetry run pylint models services utils ui
# or
make lint

# Type checking
poetry run mypy .
# or
make check

# Clean cache files
make clean
```

### Virtual Environment Management

```bash
# Activate virtual environment
poetry shell

# Deactivate (when inside poetry shell)
exit

# Show virtual environment path
poetry env info

# Remove virtual environment
poetry env remove python

# List all virtual environments
poetry env list
```

---

## 🌍 Cross-Platform Compatibility

### Path Handling

The project uses `pathlib.Path` throughout for cross-platform path compatibility:

```python
from pathlib import Path

# Works on both Windows and Linux
data_file = Path("data") / "activities_data.yml"
```

### Line Endings

- **Windows**: Uses CRLF (`\r\n`)
- **Linux**: Uses LF (`\n`)

Git automatically handles line endings. Configure your editor to use LF for consistency:

**VS Code** (`settings.json`):
```json
{
    "files.eol": "\n"
}
```

### File Permissions

**Linux/Ubuntu:**
```bash
# Make scripts executable
chmod +x start.sh
chmod +x run.py
```

**Windows:**
No special permissions needed.

---

## 🐛 Troubleshooting

### Poetry not found after installation

**Windows:**
1. Close and reopen PowerShell/Terminal
2. Check if Poetry is in PATH: `$env:PATH`
3. Add Poetry to PATH manually if needed

**Linux:**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Virtual environment issues

```bash
# Remove and recreate virtual environment
poetry env remove python
poetry install
```

### Dependency conflicts

```bash
# Update poetry.lock
poetry lock --no-update

# Force reinstall
poetry install --remove-untracked
```

### Import errors

```bash
# Make sure you're in the project directory
cd activity_selector

# Run with poetry
poetry run python run.py
```

### Tkinter not available

**Ubuntu/Linux:**
```bash
sudo apt-get install python3-tk
```

**Windows:**
Tkinter comes with Python by default.

---

## 📁 Project Structure

```
activity_selector/
├── pyproject.toml           # Poetry configuration & dependencies
├── poetry.lock              # Locked dependency versions
├── run.py                   # Cross-platform launcher
├── start.ps1                # Windows PowerShell launcher
├── start.sh                 # Ubuntu/Linux Bash launcher
├── Makefile                 # Common development tasks
├── .gitignore               # Git ignore patterns
├── activity_selector_refactored.py  # Main application (refactored)
├── activity_selector.py     # Original application (backup)
├── models/                  # Data models
├── services/                # External services (OpenAI)
├── utils/                   # Utility functions
├── ui/                      # UI dialogs
├── image_cache/             # Cached images
├── activities_data.yml      # Activity database
└── config.yml               # User configuration
```

---

## 🔄 Migration from pip/venv

If you were using `pip` and `venv` before:

1. **Export current dependencies** (optional):
   ```bash
   pip freeze > requirements-old.txt
   ```

2. **Remove old virtual environment**:
   ```bash
   # Windows
   Remove-Item -Recurse -Force venv

   # Linux
   rm -rf venv
   ```

3. **Install with Poetry**:
   ```bash
   poetry install
   ```

4. **Compare dependencies** (optional):
   ```bash
   poetry show
   ```

All your data files (`activities_data.yml`, `config.yml`, `image_cache/`) will remain intact!

---

## 🎯 Best Practices

1. **Always use Poetry commands** for dependency management
2. **Don't manually edit poetry.lock** - let Poetry manage it
3. **Commit both `pyproject.toml` and `poetry.lock`** to git
4. **Use `poetry shell`** for interactive development
5. **Use `poetry run`** for running scripts
6. **Keep dev dependencies separate** with `--group dev`

---

## 📚 Additional Resources

- **Poetry Documentation**: https://python-poetry.org/docs/
- **Poetry Commands**: https://python-poetry.org/docs/cli/
- **pyproject.toml Spec**: https://python-poetry.org/docs/pyproject/

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] `poetry --version` shows Poetry version
- [ ] `poetry install` completes without errors
- [ ] `poetry show` lists all dependencies
- [ ] `poetry run python run.py` launches the app
- [ ] Launcher scripts work (`.ps1` on Windows, `.sh` on Linux)
- [ ] All features work as expected

---

**Your Activity Selector is now powered by Poetry!** 🎉

For questions or issues, refer to the main README.md or create an issue on GitHub.
