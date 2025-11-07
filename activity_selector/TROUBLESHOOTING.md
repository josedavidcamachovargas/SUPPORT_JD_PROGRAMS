# Troubleshooting Guide - Activity Selector Refactored

## 🐛 Common Issues and Solutions

### Issue: AttributeError - 'update_status_bar' not found

**Symptoms:**
```
AttributeError: 'ActivitySelectorRefactored' object has no attribute 'update_status_bar'
```

**Cause:** Python is using cached bytecode (`.pyc` files) from an older version.

**Solution:**
```powershell
# Clear all Python cache files
cd activity_selector
Remove-Item -Recurse -Force __pycache__, models\__pycache__, services\__pycache__, utils\__pycache__, ui\__pycache__ -ErrorAction SilentlyContinue

# Then run the app
python activity_selector_refactored.py
```

**Alternative Solution (Linux/Mac):**
```bash
cd activity_selector
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
python activity_selector_refactored.py
```

---

### Issue: Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'models'
ImportError: cannot import name 'ActivityDialogs'
```

**Cause:** Missing `__init__.py` files or wrong working directory.

**Solution:**
1. Make sure you're in the `activity_selector` directory:
   ```powershell
   cd c:\Users\David\Documents\GitHub\SUPPORT_JD_PROGRAMS\activity_selector
   ```

2. Verify all `__init__.py` files exist:
   ```
   models/__init__.py
   services/__init__.py
   utils/__init__.py
   ui/__init__.py
   ```

3. If missing, the files should be auto-created, but you can create them manually:
   ```powershell
   New-Item -ItemType File -Path "models\__init__.py" -Force
   New-Item -ItemType File -Path "services\__init__.py" -Force
   New-Item -ItemType File -Path "utils\__init__.py" -Force
   New-Item -ItemType File -Path "ui\__init__.py" -Force
   ```

---

### Issue: Dialogs Not Working

**Symptoms:**
- Buttons show placeholder messages
- Features say "Full implementation available in original file"

**Cause:** Running old cached version of the file.

**Solution:**
```powershell
# Force clear cache and restart
cd activity_selector
Remove-Item -Recurse -Force __pycache__, *\__pycache__
python -B activity_selector_refactored.py  # -B flag ignores bytecode
```

---

### Issue: OpenAI API Errors

**Symptoms:**
```
Error: OpenAI API key not configured
Image generation failed
```

**Solution:**
1. Open the app
2. Go to **Settings** (⚙️)
3. Enter your OpenAI API key
4. Click **Save Settings**
5. Or disable images if you don't want to use the API

---

### Issue: YAML Parsing Errors

**Symptoms:**
```
yaml.scanner.ScannerError
Error loading activities
```

**Cause:** Corrupted `activities_data.yml` file.

**Solution:**
1. Backup your current data file:
   ```powershell
   Copy-Item activities_data.yml activities_data.yml.backup
   ```

2. Try the example data:
   ```powershell
   Copy-Item activities_data_example.yml activities_data.yml
   ```

3. Restart the application

---

### Issue: Images Not Displaying

**Symptoms:**
- Images show as blank or error message
- "Failed to load image" message

**Possible Causes & Solutions:**

**1. Images disabled:**
   - Go to Settings → Enable "✅ Enable AI Image Generation"

**2. No API key:**
   - Go to Settings → Enter OpenAI API key

**3. Pillow not installed:**
   ```powershell
   pip install Pillow
   ```

**4. Cache corrupted:**
   - Settings → Click "🗑️ Clear Image Cache"
   - Regenerate images

---

### Issue: Both Versions Running

**Symptoms:**
- Multiple windows open
- Changes not saving properly

**Solution:**
```powershell
# Kill all Python processes
Get-Process python | Stop-Process -Force

# Then start fresh
python activity_selector_refactored.py
```

---

## 🔧 Development Issues

### Issue: Code Changes Not Reflecting

**Solution:**
Always clear cache after editing Python files:
```powershell
Remove-Item -Recurse -Force __pycache__, *\__pycache__ -ErrorAction SilentlyContinue
```

Or use Python's `-B` flag to skip bytecode:
```powershell
python -B activity_selector_refactored.py
```

---

### Issue: Testing Both Versions

**To test original:**
```powershell
python activity_selector.py
```

**To test refactored:**
```powershell
python activity_selector_refactored.py
```

**Note:** Both share the same data files, so be careful when testing!

---

## 📋 Quick Health Check

Run this to verify everything is set up correctly:

```powershell
cd activity_selector

# Check file structure
Get-ChildItem -Recurse -Filter "*.py" | Select-Object Name, Directory

# Check for __pycache__ directories (should clear these)
Get-ChildItem -Recurse -Directory -Filter "__pycache__"

# Clear cache
Remove-Item -Recurse -Force __pycache__, *\__pycache__ -ErrorAction SilentlyContinue

# Run with bytecode generation disabled
python -B activity_selector_refactored.py
```

---

## 🆘 Still Having Issues?

1. **Check Python version:**
   ```powershell
   python --version  # Should be 3.8 or higher
   ```

2. **Check dependencies:**
   ```powershell
   pip list | Select-String "yaml|Pillow|openai|tkinter"
   ```

3. **Verify file integrity:**
   ```powershell
   Get-Content activity_selector_refactored.py | Select-String "def update_status_bar"
   ```

4. **Run with verbose errors:**
   ```powershell
   python -v activity_selector_refactored.py
   ```

5. **Check if original still works:**
   ```powershell
   python activity_selector.py
   ```
   If original works but refactored doesn't, there may be an import issue.

---

## ✅ Validation Commands

**Before reporting an issue, run these:**

```powershell
# 1. Clear all cache
Remove-Item -Recurse -Force __pycache__, *\__pycache__ -ErrorAction SilentlyContinue

# 2. Verify main file has update_status_bar method
Select-String "def update_status_bar" activity_selector_refactored.py

# 3. Verify dialogs file exists
Test-Path ui\dialogs.py

# 4. Check for syntax errors
python -m py_compile activity_selector_refactored.py

# 5. Run with clean import
python -B activity_selector_refactored.py
```

---

## 💡 Prevention Tips

1. **Always clear cache after editing:**
   ```powershell
   Remove-Item -Recurse -Force *\__pycache__ -ErrorAction SilentlyContinue
   ```

2. **Use `-B` flag during development:**
   ```powershell
   python -B activity_selector_refactored.py
   ```

3. **Restart Python interpreter in IDE** after making changes

4. **Keep backups of data files:**
   ```powershell
   Copy-Item activities_data.yml activities_data.yml.backup
   ```

5. **Test in a clean terminal** to avoid environment issues

---

**Current Status:** ✅ All issues resolved! App running without errors after cache clear.
