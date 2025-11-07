"""
Activity data management for the Activity Selector application.
"""

import os
import yaml
from utils.constants import DATA_FILE, DEFAULT_ACTIVITIES, STATE_MAPPING


class ActivityDataManager:
    """Manages activity data including loading, saving, and migrations."""
    
    def __init__(self, data_file=None):
        self.data_file = data_file or DATA_FILE
        self.activities = self.load()
    
    def load(self):
        """Load activities from YAML file or create default data."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                activities = yaml.safe_load(f) or {}
            # Ensure all activities have the new structure with state
            self._migrate_old_data(activities)
            return activities
        else:
            # Create default activities
            activities = DEFAULT_ACTIVITIES.copy()
            self.save(activities)
            return activities
    
    def save(self, activities=None):
        """Save activities to YAML file."""
        if activities is not None:
            self.activities = activities
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.activities, f, allow_unicode=True, 
                     default_flow_style=False, sort_keys=False)
    
    def _migrate_old_data(self, activities):
        """Migrate old string-based data to new dict-based structure."""
        for category in activities:
            new_list = []
            for item in activities[category]:
                if isinstance(item, str):
                    # Old format, migrate to new format
                    state = self._get_default_state(category)
                    new_list.append({
                        "name": item, 
                        "state": state,
                        "saga": None,
                        "order": None
                    })
                elif isinstance(item, dict):
                    # Already new format, ensure it has all fields
                    if "name" not in item:
                        continue
                    if "state" not in item:
                        item["state"] = self._get_default_state(category)
                    if "saga" not in item:
                        item["saga"] = None
                    if "order" not in item:
                        item["order"] = None
                    # Add next_episode field for series
                    if category.lower() == "series" and "next_episode" not in item:
                        item["next_episode"] = None
                    new_list.append(item)
            activities[category] = new_list
        self.save(activities)
    
    def _get_default_state(self, category):
        """Get the default state based on category."""
        category_lower = category.lower()
        if category_lower in STATE_MAPPING:
            return STATE_MAPPING[category_lower]["not_started"]
        return STATE_MAPPING["default"]["not_started"]
    
    def get_categories(self):
        """Get list of all categories."""
        return list(self.activities.keys())
    
    def get_activities(self, category):
        """Get all activities in a category."""
        return self.activities.get(category, [])
    
    def add_category(self, category):
        """Add a new category."""
        if category not in self.activities:
            self.activities[category] = []
            self.save()
            return True
        return False
    
    def rename_category(self, old_name, new_name):
        """Rename a category."""
        if old_name in self.activities and new_name not in self.activities:
            self.activities[new_name] = self.activities.pop(old_name)
            self.save()
            return True
        return False
    
    def delete_category(self, category):
        """Delete a category."""
        if category in self.activities:
            del self.activities[category]
            self.save()
            return True
        return False
    
    def add_activity(self, category, activity_data):
        """Add an activity to a category."""
        if category in self.activities:
            self.activities[category].append(activity_data)
            self.save()
            return True
        return False
    
    def update_activity(self, category, old_name, updated_data):
        """Update an activity's data."""
        if category in self.activities:
            for item in self.activities[category]:
                if item["name"] == old_name:
                    item.update(updated_data)
                    self.save()
                    return True
        return False
    
    def remove_activity(self, category, activity_name):
        """Remove an activity from a category."""
        if category in self.activities:
            self.activities[category] = [
                item for item in self.activities[category] 
                if item["name"] != activity_name
            ]
            self.save()
            return True
        return False
    
    def move_activity(self, from_category, to_category, activity_name):
        """Move an activity from one category to another."""
        if from_category in self.activities and to_category in self.activities:
            activity = None
            for item in self.activities[from_category]:
                if item["name"] == activity_name:
                    activity = item
                    break
            
            if activity:
                self.activities[from_category].remove(activity)
                self.activities[to_category].append(activity)
                self.save()
                return True
        return False
    
    def get_states_for_category(self, category):
        """Get available states for a category."""
        category_lower = category.lower()
        if category_lower in STATE_MAPPING:
            mapping = STATE_MAPPING[category_lower]
        else:
            mapping = STATE_MAPPING["default"]
        
        return [mapping["not_started"], mapping["in_progress"], mapping["completed"]]
    
    def filter_saga_prerequisites(self, activities, category):
        """Filter out saga items where previous items haven't been completed."""
        filtered = []
        
        for item in activities:
            saga = item.get("saga")
            order = item.get("order")
            
            # If not part of a saga, always include
            if not saga or order is None:
                filtered.append(item)
                continue
            
            # If it's the first in the saga, include it
            if order == 1:
                filtered.append(item)
                continue
            
            # Check if all previous items in the saga are completed
            previous_completed = True
            for other_item in self.activities[category]:
                other_saga = other_item.get("saga")
                other_order = other_item.get("order")
                
                # Check if it's the same saga and has a lower order number
                if other_saga == saga and other_order is not None and other_order < order:
                    # Previous item must be completed (Seen/Played/Done)
                    if other_item["state"] not in ["Seen", "Played", "Done"]:
                        previous_completed = False
                        break
            
            if previous_completed:
                filtered.append(item)
        
        return filtered
