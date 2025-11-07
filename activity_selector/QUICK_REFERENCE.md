# Quick Reference - Refactored Activity Selector

## 🚀 Running the Application

```bash
cd activity_selector
python activity_selector_refactored.py
```

## 📁 File Structure

```
activity_selector/
├── activity_selector_refactored.py   # ⭐ NEW MAIN FILE (use this!)
├── activity_selector.py               # Original backup
├── models/                            # Data & config management
├── services/                          # External API integration
├── utils/                             # Constants & helpers
└── ui/                                # All dialog implementations
```

## ✨ All Features Working

### Main Features
- 🎲 **Pick Random** - Select random activity with AI image
- ✅ **Quick Update** - Mark as Seen/Played instantly
- 📊 **History** - View selection history
- ⚙️ **Settings** - Configure API key, enable/disable images

### Activity Management (Manage Tab)
- ➕ **Add** - Add new activity (with saga support)
- ✏️ **Edit** - Rename activities
- 🗑️ **Remove** - Delete activities
- 🔄 **Change State** - Update activity status
- 📦 **Move** - Move between categories

### Category Management (Category Tab)
- 📁 **Add** - Create new category
- ✏️ **Rename** - Change category name
- 🗑️ **Delete** - Remove category (with confirmation)

### View Options (View Tab)
- 📋 **Show List** - View all activities
- 🎬 **Sagas** - Manage saga/series information
- 📺 **Next Episode** - Track next episode to watch

## 🔧 Module Functions

### ConfigManager (`models/config.py`)
```python
config_manager.get("key", default)
config_manager.update(key=value)
config_manager.save()
```

### ActivityDataManager (`models/activity_data.py`)
```python
data_manager.get_activities(category)
data_manager.add_activity(category, item)
data_manager.update_activity(category, name, updates)
data_manager.get_random_activity(category, state)
```

### ImageService (`services/image_service.py`)
```python
image_service.get_image(activity_name, category)
image_service.clear_cache()
```

### Dialogs (`ui/dialogs.py`)
```python
ActivityDialogs.add_activity(parent, category, data_manager, callback)
CategoryDialogs.edit_category(parent, data_manager, callback)
SagaDialogs.manage_saga(parent, category, data_manager, callback)
ViewDialogs.view_all(parent, data_manager)
```

## 📝 Key Improvements

1. **Modular** - Code split into focused modules
2. **Maintainable** - Easy to find and fix issues
3. **Testable** - Each module can be tested independently
4. **Clean** - Main file reduced from 1857 to 750 lines
5. **Organized** - Clear separation of concerns

## 🔄 Switching Versions

### Use Refactored (Recommended)
```bash
python activity_selector_refactored.py
```

### Use Original (Backup)
```bash
python activity_selector.py
```

**Both share the same data files** - switch anytime!

## 💡 Tips

- All dialogs are **fully functional** (no placeholders!)
- Data is **automatically saved** after each change
- Images are **cached** for faster loading
- **Saga management** helps organize series/trilogies
- **Episode tracking** for ongoing series
- Use **Quick Update** button for fast marking

## 🐛 Troubleshooting

### Import Errors
- Make sure all `__init__.py` files exist
- Check Python is running from activity_selector directory

### API Errors
- Go to Settings and enter OpenAI API key
- Or disable images in Settings

### Data Issues
- Both versions use same `activities_data.yml`
- Check file permissions if save fails

## 📚 Documentation

- `COMPLETE_REFACTORING.md` - Full refactoring details
- `REFACTORED_VERSION.md` - Architecture overview
- `MIGRATION_PLAN.md` - Transition guide

---

**Everything works perfectly! Enjoy your cleanly refactored application! ✨**
