# 🎲 Activity Selector

## Overview
**Activity Selector** is a fun and interactive Python application designed to help you and your girlfriend randomly choose activities to do together! Whether it's watching a movie, playing a video game, starting a series, or exploring anime, this tool takes the stress out of decision-making.

## ✨ Features

### 🎯 Core Functionality
- **Random Activity Selection**: Pick a random activity from your personalized database
- **Category-Based Organization**: Organize activities into categories (movies, series, videogames, anime, etc.)
- **Activity States**: Track what you've completed with customizable states:
  - Movies/Series: `Not Seen`, `Watching`, `Seen`
  - Videogames: `Not Played`, `Playing`, `Played`
  - Custom states for other categories
- **Smart Filtering**: 
  - Filter to show only new/unstarted activities
  - Option to include or exclude completed items

### 🎬 Saga Management
- **Organize Series & Franchises**: Group related activities into sagas (e.g., Harry Potter movies, Terminator series)
- **Order Tracking**: Maintain proper viewing/playing order within sagas
- **Saga Filtering**: Select random activities from specific sagas

### 🖼️ Visual Enhancement
- **AI-Generated Images**: Integration with OpenAI's DALL-E to generate vibrant images for each activity
- **Image Caching**: Downloaded images are cached locally to avoid regenerating
- **Image Regeneration**: Don't like the generated image? Regenerate it with one click!
- **Customizable Image Style**: Configure the style of generated images (vibrant digital art, realistic photo, etc.)

### 📊 Management Tools
- **Activity Management**:
  - ➕ Add new activities
  - ✏️ Edit existing activities
  - 🗑️ Remove activities
  - ✏️ Change activity states
  - 📦 Move activities between categories
  - 🎬 Manage saga associations

- **Category Management**:
  - 📁 Create new categories
  - ✏️ Rename existing categories
  - 🗑️ Delete categories

- **View & History**:
  - 📋 View all activities by category
  - 📊 Check selection history
  - ⚙️ Configure settings (API keys, image preferences)

## 🛠️ Technical Details

### Requirements
- **Python 3.8+**
- **Poetry** - Modern dependency management (recommended)
- **Dependencies** (managed by Poetry):
  - `tkinter` - GUI framework (usually included with Python)
  - `PyYAML` - For YAML configuration and data files
  - `Pillow (PIL)` - Image processing for AI-generated images
  - `requests` - HTTP requests for image downloads
  - `openai` - OpenAI API client for DALL-E image generation

### Project Structure
```
activity_selector/
├── pyproject.toml                    # Poetry configuration
├── poetry.lock                       # Locked dependencies
├── run.py                           # Cross-platform launcher
├── start.ps1                        # Windows launcher
├── start.sh                         # Linux launcher
├── activity_selector_refactored.py  # Main application (refactored)
├── activity_selector.py             # Original application (backup)
├── models/                          # Data models
│   ├── config.py                   # Configuration manager
│   └── activity_data.py            # Activity data manager
├── services/                        # External services
│   └── image_service.py            # OpenAI image generation
├── utils/                           # Utilities
│   └── constants.py                # Application constants
├── ui/                              # User interface
│   └── dialogs.py                  # Dialog windows
├── image_cache/                     # Cached images
├── activities_data.yml              # Activity database
└── config.yml                       # User configuration
```

### Data Structure
Activities are stored in YAML format with the following structure:
```yaml
category_name:
  - name: "Activity Name"
    state: "Not Seen"  # or Not Played, Watching, etc.
    saga: "Saga Name"  # null if not part of a saga
    order: 1           # null if not part of a saga
    next_episode: "S01E05"  # for series category
```

## 🚀 Getting Started

### Option 1: Using Poetry (Recommended)

**Windows - Easy Method (.bat files - no policy issues):**
```cmd
REM First time setup
setup.bat

REM Run the application
start.bat
```

**Windows - PowerShell (if execution policy allows):**
```powershell
# If you get execution policy errors, use:
powershell -ExecutionPolicy Bypass -File .\setup.ps1

# Or set policy once:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then run normally:
.\start.ps1
```

**Windows - Alternative (direct Poetry):**
```powershell
# Install Poetry (if not installed)
python -m pip install poetry

# Install dependencies
poetry install

# Run the application
poetry run python run.py
```

**Ubuntu/Linux (Bash):**
```bash
# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# Make scripts executable
chmod +x setup.sh start.sh

# First time setup
./setup.sh

# Run the application
./start.sh
```

### Option 2: Traditional pip Installation

```bash
# Install dependencies
pip install pyyaml pillow requests openai

# Run the application
python activity_selector_refactored.py
```

### Configuration

1. **Configure OpenAI API (Optional)**:
   - Launch the app and go to Settings (⚙️)
   - Enter your OpenAI API key
   - Or disable image generation if you don't want to use the API

2. **Start Adding Activities**:
   - Use the management buttons to add your favorite movies, games, and series
   - Organize them into categories and sagas
   - Click "🎲 Pick Random Activity" to let fate decide!

## � Documentation

- **[POETRY_SETUP.md](POETRY_SETUP.md)** - Detailed Poetry installation and usage guide
- **[COMPLETE_REFACTORING.md](COMPLETE_REFACTORING.md)** - Architecture and refactoring details
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick command reference
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and data flow

## �💡 Use Cases
- **Movie Night**: Can't decide what to watch? Let the app choose!
- **Gaming Sessions**: Randomly select which co-op game to play
- **Binge Planning**: Keep track of series you want to watch together
- **Saga Completion**: Work through movie franchises in order
- **Activity Discovery**: Rediscover forgotten activities in your list

## 🌍 Cross-Platform Support
- ✅ **Windows 10/11** - Full support with PowerShell launcher
- ✅ **Ubuntu/Linux** - Full support with Bash launcher
- ✅ **WSL** - Works seamlessly with Windows Subsystem for Linux
- ✅ **macOS** - Should work (untested)

## 🔐 Privacy & Security
- Configuration files containing API keys are excluded from version control
- Local image cache ensures privacy of your activity selections
- All data is stored locally on your machine

## 👥 Credits
Created with ❤️ for quality time together!

Powered by:
- **Poetry** - Dependency management
- **OpenAI DALL-E 3** - AI image generation
- **Python tkinter** - Cross-platform GUI

---

**Enjoy deciding... or not deciding!** 🎲💕
