"""
Example: Using the Refactored Components

This file demonstrates how to use the new modular structure.
"""

# Example 1: Using ConfigManager
from models.config import ConfigManager

config = ConfigManager()
api_key = config.get("openai_api_key")
config.set("image_style", "cartoon style")
config.save()


# Example 2: Using ActivityDataManager
from models.activity_data import ActivityDataManager

data_manager = ActivityDataManager()

# Get all categories
categories = data_manager.get_categories()
print(f"Categories: {categories}")

# Get activities in a category
activities = data_manager.get_activities("videogame")
print(f"Videogames: {len(activities)}")

# Add a new activity
data_manager.add_activity("videogame", {
    "name": "New Game",
    "state": "Not Played",
    "saga": None,
    "order": None
})

# Update an activity
data_manager.update_activity("videogame", "New Game", {
    "state": "Playing"
})

# Get states for a category
states = data_manager.get_states_for_category("videogame")
print(f"Available states: {states}")


# Example 3: Using ImageService
from services.image_service import ImageService

config_manager = ConfigManager()
image_service = ImageService(config_manager)

# Get or generate an image
try:
    image = image_service.get_activity_image("Mario Kart", "videogame")
    if image:
        print("Image loaded successfully!")
except Exception as e:
    print(f"Error: {e}")

# Clear image cache
count = image_service.clear_cache()
print(f"Deleted {count} cached images")


# Example 4: Using Constants
from utils.constants import (
    WINDOW_TITLE,
    WINDOW_WIDTH,
    COLOR_PRIMARY,
    STATE_MAPPING,
    IN_PROGRESS_STATES
)

print(f"App title: {WINDOW_TITLE}")
print(f"Window size: {WINDOW_WIDTH}")
print(f"Primary color: {COLOR_PRIMARY}")
print(f"In-progress states: {IN_PROGRESS_STATES}")


# Example 5: Complete Integration
def example_full_integration():
    """Example of using all components together."""
    
    # Initialize managers
    config_mgr = ConfigManager()
    data_mgr = ActivityDataManager()
    img_service = ImageService(config_mgr)
    
    # Check if images are enabled
    if config_mgr.get("enable_images", True):
        print("Images are enabled")
        
        # Get all categories
        for category in data_mgr.get_categories():
            activities = data_mgr.get_activities(category)
            print(f"\n{category}: {len(activities)} activities")
            
            # Show first activity
            if activities:
                first = activities[0]
                print(f"  - {first['name']} [{first['state']}]")
                
                # Try to get image (if API key is set)
                if config_mgr.get("openai_api_key"):
                    try:
                        img = img_service.get_activity_image(
                            first['name'], 
                            category
                        )
                        if img:
                            print(f"    ✓ Image loaded")
                    except Exception as e:
                        print(f"    ✗ Image error: {e}")


if __name__ == "__main__":
    print("=== Activity Selector - Component Examples ===\n")
    example_full_integration()
    print("\n=== Done! ===")
