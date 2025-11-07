"""
Constants and default values for the Activity Selector application.
"""

# Window settings
WINDOW_TITLE = "🎲 Activity Selector - What to do today?"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 850
MIN_WINDOW_WIDTH = 700
MIN_WINDOW_HEIGHT = 700

# Colors
COLOR_PRIMARY = "#4a90e2"
COLOR_BACKGROUND = "#f0f0f0"
COLOR_WHITE = "#ffffff"
COLOR_SUCCESS = "#4CAF50"
COLOR_WARNING = "#FF9800"
COLOR_DANGER = "#f44336"
COLOR_INFO = "#2196F3"

# Image settings
IMAGE_SIZE = (500, 500)
IMAGE_CACHE_DIR = "image_cache"

# File paths
DATA_FILE = "activities_data.yml"
CONFIG_FILE = "config.yml"

# State mappings
STATE_MAPPING = {
    "videogame": {
        "not_started": "Not Played",
        "in_progress": "Playing",
        "completed": "Played"
    },
    "series": {
        "not_started": "Not Seen",
        "in_progress": "Watching",
        "completed": "Seen"
    },
    "movie": {
        "not_started": "Not Seen",
        "in_progress": "Watching",
        "completed": "Seen"
    },
    "default": {
        "not_started": "Pending",
        "in_progress": "In Progress",
        "completed": "Done"
    }
}

# In-progress states (for weighted selection)
IN_PROGRESS_STATES = ["Watching", "Playing", "In Progress"]

# Default activities
DEFAULT_ACTIVITIES = {
    "videogame": [
        {"name": "Play Mario Kart", "state": "Not Played", "saga": None, "order": None},
        {"name": "Play Minecraft together", "state": "Not Played", "saga": None, "order": None},
        {"name": "Try a co-op adventure game", "state": "Not Played", "saga": None, "order": None},
        {"name": "Play Overcooked 2", "state": "Not Played", "saga": None, "order": None}
    ],
    "series": [
        {"name": "Watch a comedy series", "state": "Not Seen", "saga": None, "order": None, "next_episode": None},
        {"name": "Start a new Netflix show", "state": "Not Seen", "saga": None, "order": None, "next_episode": None},
        {"name": "Rewatch favorite episodes", "state": "Not Seen", "saga": None, "order": None, "next_episode": None},
        {"name": "Binge-watch a mini-series", "state": "Not Seen", "saga": None, "order": None, "next_episode": None}
    ],
    "movie": [
        {"name": "Watch a romantic comedy", "state": "Not Seen", "saga": None, "order": None},
        {"name": "Watch an action movie", "state": "Not Seen", "saga": None, "order": None},
        {"name": "Watch a classic film", "state": "Not Seen", "saga": None, "order": None},
        {"name": "Watch a documentary", "state": "Not Seen", "saga": None, "order": None}
    ]
}

# Default config
DEFAULT_CONFIG = {
    "openai_api_key": "",
    "enable_images": True,
    "image_style": "vibrant digital art"
}
