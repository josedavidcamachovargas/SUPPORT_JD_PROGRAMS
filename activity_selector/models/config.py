"""
Configuration management for the Activity Selector application.
"""

import os
import yaml
from pathlib import Path
from utils.constants import CONFIG_FILE, DEFAULT_CONFIG


class ConfigManager:
    """Manages application configuration including API keys."""
    
    def __init__(self, config_file=None):
        self.config_file = config_file or CONFIG_FILE
        self.config = self.load()
    
    def load(self):
        """Load configuration from YAML file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or DEFAULT_CONFIG.copy()
        else:
            config = DEFAULT_CONFIG.copy()
            self.save(config)
            return config
    
    def save(self, config=None):
        """Save configuration to YAML file."""
        if config is not None:
            self.config = config
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value."""
        self.config[key] = value
    
    def update(self, **kwargs):
        """Update multiple configuration values."""
        self.config.update(kwargs)
