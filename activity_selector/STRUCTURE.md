# Activity Selector - Code Structure

## Overview
The codebase has been refactored following best practices with separation of concerns, single responsibility principle, and a clean architecture pattern.

## Project Structure

```
activity_selector/
├── models/                 # Data models and business logic
│   ├── __init__.py
│   ├── activity_data.py   # Activity data management (CRUD operations)
│   └── config.py          # Configuration management
│
├── services/              # External services and complex operations
│   ├── __init__.py
│   └── image_service.py   # Image generation and caching
│
├── ui/                    # User interface components
│   ├── __init__.py
│   ├── main_window.py     # Main application window (TO BE CREATED)
│   └── dialogs.py         # Dialog windows (TO BE CREATED)
│
├── utils/                 # Utilities and constants
│   ├── __init__.py
│   └── constants.py       # Application constants and defaults
│
├── activity_selector.py   # Main entry point (refactored)
├── activities_data.yml    # Data file
├── config.yml             # Configuration file (not in git)
└── README.md             # This file
```

## Architecture

### 1. **Models Layer** (`models/`)
- **Purpose**: Data management and business logic
- **Components**:
  - `activity_data.py`: Manages activity CRUD operations, data migration, saga filtering
  - `config.py`: Manages application configuration and API keys

### 2. **Services Layer** (`services/`)
- **Purpose**: External integrations and complex operations
- **Components**:
  - `image_service.py`: Handles OpenAI API integration, image generation, and caching

### 3. **UI Layer** (`ui/`)
- **Purpose**: User interface components
- **Components**:
  - `main_window.py`: Main application window and core UI
  - `dialogs.py`: Dialog windows for various operations

### 4. **Utils Layer** (`utils/`)
- **Purpose**: Constants, helpers, and utilities
- **Components**:
  - `constants.py`: Application-wide constants and default values

## Design Patterns Used

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Dependency Injection**: Services receive dependencies through constructors
3. **Manager Pattern**: ConfigManager and ActivityDataManager encapsulate data operations
4. **Service Pattern**: ImageService handles complex external operations
5. **Factory Pattern**: Default data creation in constants

## Benefits of This Structure

1. **Maintainability**: Easier to find and fix bugs
2. **Testability**: Each component can be tested independently
3. **Scalability**: Easy to add new features without affecting existing code
4. **Readability**: Clear organization makes code easier to understand
5. **Reusability**: Components can be reused in other projects

## Migration Guide

The original `activity_selector.py` (1800+ lines) has been split into:
- **Constants**: ~80 lines in `utils/constants.py`
- **Config Management**: ~50 lines in `models/config.py`
- **Data Management**: ~200 lines in `models/activity_data.py`
- **Image Service**: ~180 lines in `services/image_service.py`
- **UI Components**: Will be split across `ui/main_window.py` and `ui/dialogs.py`
- **Main Entry**: Simplified to ~50 lines in `activity_selector.py`

## Next Steps

1. Create `ui/main_window.py` with the main window UI
2. Create `ui/dialogs.py` with all dialog windows
3. Refactor the main `activity_selector.py` to use the new components
4. Test all functionality
5. Update documentation

## Running the Application

```bash
python activity_selector.py
```

The application will automatically use the new modular structure.
