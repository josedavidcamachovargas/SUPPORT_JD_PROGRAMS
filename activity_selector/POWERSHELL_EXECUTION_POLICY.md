# PowerShell Execution Policy Fix

## 🔒 Issue: Script Execution Disabled

You're seeing this error because Windows PowerShell has execution policies that prevent running scripts by default for security reasons.

```
.\setup.ps1 : No se puede cargar el archivo ... porque la ejecución de scripts está deshabilitada en este sistema.
```

---

## ✅ Solutions (Choose One)

### Solution 1: Bypass for Single Execution (Recommended)

Run the script with bypass flag:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

Or:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

This bypasses the policy only for this specific script execution (safest option).

---

### Solution 2: Change Policy for Current User (Recommended)

Allow scripts for your user account only:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then you can run normally:

```powershell
.\setup.ps1
.\start.ps1
```

**Note:** You'll need to confirm with `Y` when prompted.

---

### Solution 3: Change Policy for Current Session Only

Allow scripts for this PowerShell session only:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\setup.ps1
```

This policy resets when you close PowerShell.

---

### Solution 4: Run as Administrator (One-Time)

1. Open PowerShell as Administrator (Right-click → Run as Administrator)
2. Run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
   ```
3. Close admin PowerShell
4. Open normal PowerShell and run:
   ```powershell
   .\setup.ps1
   ```

---

### Solution 5: Use Python Directly (No PowerShell Needed)

Skip PowerShell entirely and use Python directly:

```powershell
# Install Poetry (if not installed)
python -m pip install poetry

# Install dependencies
poetry install

# Run the app
poetry run python run.py
```

Or even simpler:

```powershell
# Without Poetry (traditional method)
pip install pyyaml pillow requests openai
python activity_selector_refactored.py
```

---

## 🎯 Quick Start Command (No Policy Change Needed)

**Use this command to run the setup without changing any policies:**

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

**To run the app later:**

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

---

## 🔍 Understanding Execution Policies

| Policy | Description |
|--------|-------------|
| `Restricted` | Default. No scripts allowed. |
| `RemoteSigned` | Local scripts ok. Downloaded scripts need signature. |
| `Bypass` | Nothing blocked, no warnings. |
| `Unrestricted` | All scripts allowed, but warns for downloaded ones. |

**Scopes:**
- `Process` - Current session only (safest)
- `CurrentUser` - Your user account only
- `LocalMachine` - All users (requires admin)

---

## ✅ Recommended Approach

### Option A: Quick and Safe
```powershell
# Run with bypass (no policy change)
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

### Option B: Permanent Fix (One-Time)
```powershell
# Set policy for your user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then run normally
.\setup.ps1
```

### Option C: Pure Python (No PowerShell Issues)
```powershell
# Check if Poetry is installed
poetry --version

# If not, install it
pip install poetry

# Install dependencies
poetry install

# Run the app
poetry run python run.py
```

---

## 🐛 Still Having Issues?

### Check Current Policy
```powershell
Get-ExecutionPolicy -List
```

### Verify Script Path
```powershell
# Make sure you're in the right directory
cd C:\Users\David\Documents\GitHub\SUPPORT_JD_PROGRAMS\activity_selector

# List files
ls *.ps1
```

### Run with Full Path
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\David\Documents\GitHub\SUPPORT_JD_PROGRAMS\activity_selector\setup.ps1"
```

---

## 🎓 Why This Happens

Windows blocks downloaded or "untrusted" scripts by default to protect against malicious code. Since these scripts were created programmatically, Windows treats them as potentially unsafe.

**This is normal and expected behavior!**

---

## 🚀 Next Steps

1. **Choose a solution above** (I recommend Option A or B)
2. **Run the setup:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\setup.ps1
   ```
3. **Start using the app!**

---

**The scripts are safe - they only install dependencies and launch your Python application!** ✅
