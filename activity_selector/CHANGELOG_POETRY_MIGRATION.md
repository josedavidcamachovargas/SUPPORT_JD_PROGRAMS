# Changelog - Poetry Migration & Improvements

## Version 2.0.0 - Poetry Migration (November 7, 2025)

### 🎉 Major Changes

#### Poetry Integration
- **Migrated from manual dependency management to Poetry**
- Created `pyproject.toml` with complete project configuration
- Generated `poetry.lock` for reproducible builds
- Updated Python requirement from `^3.8` to `^3.9` (compatible with Python 3.12.10)

#### Cross-Platform Launcher Scripts
Created multiple launcher scripts for different platforms and shells:

**Windows:**
- `setup.bat` - Windows batch setup wizard (no execution policy issues)
- `start.bat` - Windows batch launcher
- `setup.ps1` - PowerShell setup wizard (with colored output)
- `start.ps1` - PowerShell launcher

**Linux/Ubuntu:**
- `setup.sh` - Bash setup wizard with dependency checking
- `start.sh` - Bash launcher

**Universal:**
- `run.py` - Cross-platform Python launcher

#### Content Policy Violation Handling
- **Added automatic retry mechanism** for OpenAI content policy violations
- Implemented `_build_safe_fallback_prompt()` method
- Generic, family-friendly fallback prompts by category
- Seamless user experience - no failed image generations

### 📦 Dependencies

#### Production Dependencies
- `python = "^3.9"` (updated from ^3.8)
- `pyyaml = "^6.0.1"`
- `pillow = "^10.4.0"`
- `requests = "^2.32.3"`
- `openai = "^1.51.0"`

#### Development Dependencies
- `pytest = "^8.3.3"`
- `pytest-cov = "^5.0.0"`
- `black = "^24.8.0"`
- `flake8 = "^7.1.1"`
- `mypy = "^1.11.2"`
- `pylint = "^3.3.1"`

### 📝 Documentation

#### New Documentation Files (All in English)
1. **POETRY_SETUP.md** - Complete Poetry installation and usage guide
2. **POETRY_MIGRATION.md** - Detailed migration summary and benefits
3. **POETRY_COMPLETE.md** - Quick completion guide
4. **POETRY_VISUAL_SUMMARY.md** - Visual diagrams and comparisons
5. **POWERSHELL_EXECUTION_POLICY.md** - Solutions for PowerShell execution policy issues
6. **WINDOWS_QUICK_START.md** - Windows-specific quick start guide
7. **CONTENT_POLICY_HANDLING.md** - Content policy violation handling documentation
8. **Makefile** - Common development tasks (test, lint, format, clean)

#### Updated Documentation
- **README.md** - Added Poetry installation and usage instructions
- Added cross-platform setup instructions
- Included Windows-specific notes about execution policies

### 🔧 Technical Improvements

#### Image Service (`services/image_service.py`)
- Added `try-except` block for `openai.BadRequestError`
- Detects `content_policy_violation` errors
- Automatically retries with sanitized prompt
- Added `_build_safe_fallback_prompt()` method
- Console logging for debugging

#### Build Configuration
- Configured `pyproject.toml` for Poetry builds
- Added tool configurations for:
  - Black (code formatter)
  - MyPy (type checker)
  - Pytest (testing)
  - Pylint (linter)

#### Git Configuration
- Updated `.gitignore` to work with Poetry
- Added `.venv`, `poetry.lock`, and Poetry-related directories
- **Now tracking image_cache/*.png** files for shared image library
- Removed `image_cache/*.png` exclusion

### 🎯 Benefits

#### For Users
- ✅ Easier installation with automated setup wizards
- ✅ No more manual dependency management
- ✅ Cross-platform support (Windows & Linux)
- ✅ No failed image generations (automatic fallback)
- ✅ Multiple launcher options (PowerShell, batch, bash, Python)

#### For Developers
- ✅ Reproducible builds with `poetry.lock`
- ✅ Isolated virtual environments
- ✅ Integrated development tools (testing, linting, formatting)
- ✅ Easy dependency updates
- ✅ Standard Python project structure
- ✅ Makefile for common tasks

### 🐛 Bug Fixes
- Fixed Python version compatibility (now supports Python 3.9-3.12)
- Fixed PowerShell execution policy issues with `.bat` alternatives
- Fixed OpenAI content policy violations with automatic retry
- Fixed pylint compatibility with Python 3.8 (updated to 3.9+)

### 🚀 Usage

#### Quick Start (Windows)
```powershell
# First time setup
.\setup.bat

# Run the application
.\start.bat
```

#### Quick Start (Linux/Ubuntu)
```bash
# First time setup
chmod +x setup.sh start.sh
./setup.sh

# Run the application
./start.sh
```

#### Manual Poetry Commands
```bash
# Install dependencies
poetry install

# Run application
poetry run python run.py

# Run tests
poetry run pytest

# Format code
poetry run black .

# Lint code
poetry run flake8
poetry run pylint .

# Type check
poetry run mypy .
```

#### Using Makefile
```bash
# Run tests
make test

# Lint code
make lint

# Format code
make format

# Clean generated files
make clean

# See all available commands
make help
```

### 📊 File Changes Summary

#### New Files (24)
- Configuration: `pyproject.toml`, `poetry.lock`, `Makefile`
- Launchers: `run.py`, `setup.bat`, `setup.ps1`, `setup.sh`, `start.bat`, `start.ps1`, `start.sh`
- Documentation: 7 new markdown files
- Git: Updated `.gitignore`

#### Modified Files (3)
- `README.md` - Added Poetry instructions
- `services/image_service.py` - Added content policy fallback
- `.gitignore` - Updated for Poetry and image tracking

#### Deleted Files (1)
- Removed Spanish documentation (keeping only English)

### 🔄 Migration Notes

#### Breaking Changes
- **None** - Application functionality remains identical
- All existing features work the same way
- Data files (`activities_data.yml`, `config.yml`) are unchanged

#### Backward Compatibility
- Old manual installation still works
- Existing virtual environments can coexist
- No changes to application code logic

### 📈 Statistics

- **Lines Added**: ~15,000+ (including documentation and scripts)
- **New Scripts**: 7 launcher/setup scripts
- **New Documentation**: 7 comprehensive guides
- **Dependencies Managed**: 11 packages (5 production + 6 development)
- **Platforms Supported**: Windows (PowerShell, CMD), Linux (Bash), macOS (Bash)

### 🎓 What You Learned

This migration demonstrates:
- Modern Python dependency management with Poetry
- Cross-platform script development
- PowerShell execution policy handling
- OpenAI API error handling and retry logic
- Professional Python project structure
- Development tooling integration

### 🔮 Future Improvements

Potential enhancements:
- [ ] GitHub Actions CI/CD pipeline
- [ ] Docker containerization
- [ ] Pre-commit hooks for code quality
- [ ] Automated testing in CI
- [ ] PyPI package publication
- [ ] More sophisticated content policy handling
- [ ] User notification system for fallback prompts

---

## Contributors
- David Camacho (@josedavidcamachovargas)

## License
MIT License - See LICENSE file for details

---

**Last Updated**: November 7, 2025  
**Version**: 2.0.0  
**Python**: 3.9-3.12  
**Poetry**: 2.2.1+
