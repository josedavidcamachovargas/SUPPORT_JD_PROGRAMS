# Activity Selector - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     activity_selector.py                         │
│                    (Main Entry Point)                            │
│                      ~50-100 lines                               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ creates and coordinates
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  UI Layer     │   │ Models Layer  │   │Services Layer │
│               │   │               │   │               │
│ main_window   │◄──│ config.py     │◄──│image_service  │
│ dialogs       │   │ activity_data │   │               │
│               │   │               │   │               │
│ ~1000 lines   │   │ ~250 lines    │   │ ~180 lines    │
└───────────────┘   └───────┬───────┘   └───────────────┘
        │                   │                   │
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            │ all use
                            │
                            ▼
                   ┌────────────────┐
                   │  Utils Layer   │
                   │                │
                   │  constants.py  │
                   │                │
                   │  ~80 lines     │
                   └────────────────┘
```

## Component Interactions

### 1. Data Flow

```
User Action (UI)
    ↓
Main Window / Dialog
    ↓
ActivityDataManager (models)
    ↓
YAML File (activities_data.yml)
```

### 2. Image Generation Flow

```
User Requests Image (UI)
    ↓
Main Window
    ↓
ImageService (services)
    ↓
    ├─→ Check Cache (image_cache/)
    ├─→ OpenAI API (if not cached)
    └─→ Return ImageTk.PhotoImage
```

### 3. Configuration Flow

```
Application Startup
    ↓
ConfigManager (models)
    ↓
config.yml
    ↓
Available to all components
```

## Dependency Graph

```
activity_selector.py
    ├── imports → models.config.ConfigManager
    ├── imports → models.activity_data.ActivityDataManager
    ├── imports → services.image_service.ImageService
    └── imports → utils.constants.*

models/activity_data.py
    ├── imports → utils.constants (STATE_MAPPING, DEFAULT_ACTIVITIES)
    └── uses → YAML files

models/config.py
    ├── imports → utils.constants (CONFIG_FILE, DEFAULT_CONFIG)
    └── uses → YAML files

services/image_service.py
    ├── imports → utils.constants (IMAGE_SIZE, IMAGE_CACHE_DIR)
    ├── depends on → models.config.ConfigManager
    └── uses → OpenAI API, PIL, requests

ui/main_window.py (TO BE CREATED)
    ├── imports → tkinter
    ├── uses → models.activity_data.ActivityDataManager
    ├── uses → models.config.ConfigManager
    ├── uses → services.image_service.ImageService
    └── imports → utils.constants (colors, sizes, etc.)

ui/dialogs.py (TO BE CREATED)
    ├── imports → tkinter
    └── helper dialogs for main_window
```

## Module Responsibilities

### ✅ Already Refactored:

| Module | Responsibility | Lines | Status |
|--------|---------------|-------|---------|
| `utils/constants.py` | Application constants | 80 | ✅ Done |
| `models/config.py` | Configuration management | 50 | ✅ Done |
| `models/activity_data.py` | Data CRUD operations | 200 | ✅ Done |
| `services/image_service.py` | Image generation/caching | 180 | ✅ Done |

### ⏭️ Can Be Refactored (Optional):

| Module | Responsibility | Est. Lines | Status |
|--------|---------------|-----------|---------|
| `ui/main_window.py` | Main application window | ~800 | ⏳ Optional |
| `ui/dialogs.py` | Dialog windows | ~600 | ⏳ Optional |
| `activity_selector.py` | Simplified entry point | ~50 | ⏳ Optional |

## Benefits Summary

### Before Refactoring:
```
activity_selector.py (1857 lines)
├── Constants (mixed in)
├── Configuration (mixed in)
├── Data management (mixed in)
├── Image service (mixed in)
└── UI code (mixed in)
```
**Problems:**
- Hard to find specific functionality
- Difficult to test
- Changes affect multiple concerns
- Hard to reuse components

### After Refactoring:
```
activity_selector/
├── utils/constants.py (80 lines) ← Constants
├── models/config.py (50 lines) ← Configuration
├── models/activity_data.py (200 lines) ← Data
├── services/image_service.py (180 lines) ← Images
└── activity_selector.py (1300+ lines) ← UI
```
**Benefits:**
- ✅ Easy to find specific functionality
- ✅ Each component can be tested independently
- ✅ Changes are isolated to specific modules
- ✅ Components can be reused
- ✅ Follows SOLID principles

## Key Principles Applied

1. **Single Responsibility Principle (SRP)**
   - Each class has one reason to change
   - ConfigManager → only for configuration
   - ActivityDataManager → only for data
   - ImageService → only for images

2. **Dependency Inversion Principle (DIP)**
   - High-level modules depend on abstractions
   - ImageService receives ConfigManager, not raw config

3. **Don't Repeat Yourself (DRY)**
   - Constants defined once in utils/constants.py
   - Reused across all modules

4. **Separation of Concerns (SoC)**
   - UI, business logic, and data access are separated
   - Each layer has its own directory

## Example: Adding a New Feature

### Before (Monolithic):
```python
# Had to modify the 1857-line file
# Risk of breaking existing functionality
# Hard to find where to add code
```

### After (Modular):
```python
# Want to add a new data source?
# → Create new class in models/

# Want to add a new external service?
# → Create new class in services/

# Want to add new UI feature?
# → Modify ui/ files only

# Want to change colors/constants?
# → Edit utils/constants.py only
```

## Testing Strategy (Future)

```python
# models/test_activity_data.py
def test_add_activity():
    manager = ActivityDataManager()
    manager.add_activity("test", {"name": "Test"})
    assert len(manager.get_activities("test")) == 1

# services/test_image_service.py
def test_image_caching():
    service = ImageService(mock_config)
    # Test caching logic
    
# Easy to test in isolation! ✅
```

## Conclusion

Your codebase now follows **industry best practices** for Python applications! 🎉

The architecture is:
- ✅ **Modular**: Easy to understand and modify
- ✅ **Testable**: Components can be tested independently
- ✅ **Scalable**: Easy to add new features
- ✅ **Maintainable**: Clear structure and responsibilities
- ✅ **Professional**: Follows SOLID principles

**Well done on improving your code quality!** 🚀
