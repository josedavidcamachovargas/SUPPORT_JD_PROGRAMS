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
- **Python 3.x**
- **Dependencies**:
  - `tkinter` - GUI framework (usually included with Python)
  - `PyYAML` - For YAML configuration and data files
  - `Pillow (PIL)` - Image processing (optional, for image features)
  - `requests` - HTTP requests for image downloads (optional)

### File Structure
- `activity_selector.py` - Main application
- `activities_data.yml` - Your activity database
- `config.yml` - Configuration file (contains API keys - **not version controlled**)
- `image_cache/` - Directory for cached activity images
- `activities_data_example.yml` - Example activity data structure

### Data Structure
Activities are stored in YAML format with the following structure:
```yaml
category_name:
  - name: "Activity Name"
    state: "Not Seen"  # or Not Played, Watching, etc.
    saga: "Saga Name"  # null if not part of a saga
    order: 1           # null if not part of a saga
```

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install pyyaml pillow requests
   ```

2. **Configure (Optional)**:
   - Edit `config.yml` to add your OpenAI API key for image generation
   - Set `enable_images: true/false` based on your preference

3. **Run the Application**:
   ```bash
   python activity_selector.py
   ```

4. **Start Adding Activities**:
   - Use the management buttons to add your favorite movies, games, and series
   - Organize them into categories and sagas
   - Click "🎲 Pick Random Activity" to let fate decide!

## 💡 Use Cases
- **Movie Night**: Can't decide what to watch? Let the app choose!
- **Gaming Sessions**: Randomly select which co-op game to play
- **Binge Planning**: Keep track of series you want to watch together
- **Saga Completion**: Work through movie franchises in order
- **Activity Discovery**: Rediscover forgotten activities in your list

## 🔐 Privacy & Security
- Configuration files containing API keys are excluded from version control
- Local image cache ensures privacy of your activity selections
- All data is stored locally on your machine

## 👥 Credits
Created with ❤️ for quality time together!

---

**Enjoy deciding... or not deciding!** 🎲💕
