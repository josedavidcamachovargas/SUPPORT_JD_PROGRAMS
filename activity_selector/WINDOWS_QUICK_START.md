# 🚀 Quick Start - Windows Users

## ⚡ TL;DR - Fastest Way to Run

```cmd
.\setup.bat
```

**Important:** In PowerShell, you MUST use `.\` before the filename!

---

## 🔧 Complete Setup Instructions

### Step 1: Open Command Prompt or PowerShell

Navigate to the project folder:
```cmd
cd C:\Users\David\Documents\GitHub\SUPPORT_JD_PROGRAMS\activity_selector
```

### Step 2: Run Setup (Choose One Method)

#### Method A: Batch File (Easiest - Recommended) ✅

**In PowerShell:**
```powershell
.\setup.bat
```

**In Command Prompt (cmd):**
```cmd
setup.bat
```

**⚠️ Important:** PowerShell requires `.\` before the filename for security reasons!

**No permissions needed, no policy issues!**

#### Method B: PowerShell with Bypass
```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```
**Works without changing any policies**

#### Method C: Set PowerShell Policy (One-Time)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```
**After this, you can use `.\setup.ps1` normally**

#### Method D: Direct Python/Poetry
```cmd
python -m pip install poetry
poetry install
```
**Skips all scripts, uses Poetry directly**

### Step 3: Run the Application (Choose One Method)

#### Method A: Batch File (Easiest) ✅
```cmd
start.bat
```

#### Method B: PowerShell
```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```
Or if you set the policy in Step 2:
```powershell
.\start.ps1
```

#### Method C: Direct Poetry
```cmd
poetry run python run.py
```

---

## 🎯 Recommended for You

Based on your error, use the **batch files** (`.bat`):

```cmd
# First time
setup.bat

# Every time after
start.bat
```

These work 100% of the time with no policy issues!

---

## 🐛 Troubleshooting

### Error: "Poetry is not installed"

Install Poetry:
```cmd
python -m pip install poetry
```

Then run `setup.bat` again.

### Error: "Python is not installed"

1. Download Python from: https://www.python.org/downloads/
2. Install it
3. **Important:** Check "Add Python to PATH" during installation
4. Restart your terminal
5. Try again

### Scripts Not Found

Make sure you're in the right directory:
```cmd
cd C:\Users\David\Documents\GitHub\SUPPORT_JD_PROGRAMS\activity_selector
dir *.bat
```

You should see:
- `setup.bat`
- `start.bat`

---

## 📋 What Each File Does

| File | Purpose |
|------|---------|
| `setup.bat` | Interactive setup wizard (Windows, no policy issues) |
| `start.bat` | Launch the app (Windows, no policy issues) |
| `setup.ps1` | Interactive setup wizard (PowerShell, needs policy) |
| `start.ps1` | Launch the app (PowerShell, needs policy) |
| `setup.sh` | Interactive setup wizard (Linux) |
| `start.sh` | Launch the app (Linux) |

---

## ✅ Quick Test

After setup, verify everything works:

```cmd
REM Check Poetry
poetry --version

REM Check dependencies
poetry show

REM Run the app
start.bat
```

---

## 🎉 You're Done!

From now on, just double-click `start.bat` or run:
```cmd
start.bat
```

**No PowerShell policy issues, ever!** 🎊

---

## 📚 More Information

- **PowerShell Policy Issues**: See [POWERSHELL_EXECUTION_POLICY.md](POWERSHELL_EXECUTION_POLICY.md)
- **Poetry Guide**: See [POETRY_SETUP.md](POETRY_SETUP.md)
- **Full Documentation**: See [README.md](README.md)

---

**Need help? All the .bat files are included and ready to use!** ✨
