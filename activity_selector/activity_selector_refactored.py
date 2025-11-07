"""
Activity Selector - Refactored Version
Uses modular architecture with separated concerns.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
from datetime import datetime
from pathlib import Path

from models.config import ConfigManager
from models.activity_data import ActivityDataManager
from services.image_service import ImageService
from utils.constants import *
from ui.dialogs import ActivityDialogs, CategoryDialogs, ViewDialogs, SagaDialogs, EpisodeDialogs


# Import our refactored modules
from models.config import ConfigManager
from models.activity_data import ActivityDataManager
from services.image_service import ImageService
from utils.constants import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT,
    COLOR_PRIMARY, COLOR_BACKGROUND, COLOR_SUCCESS,
    COLOR_WARNING, COLOR_DANGER, COLOR_INFO,
    IN_PROGRESS_STATES
)

# Check if PIL is available
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ActivitySelectorRefactored:
    """Main application class using modular architecture."""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.root.configure(bg=COLOR_BACKGROUND)
        
        # Initialize managers and services
        self.config_manager = ConfigManager()
        self.data_manager = ActivityDataManager()
        self.image_service = ImageService(self.config_manager)
        
        # History
        self.history = []
        
        # Current selection state
        self.current_image = None
        self.current_activity = None
        self.current_category = None
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create the main UI widgets."""
        # Title
        title_frame = tk.Frame(self.root, bg=COLOR_PRIMARY, height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title = tk.Label(title_frame, text="🎲 Activity Selector 💕", 
                        font=("Arial", 24, "bold"), bg=COLOR_PRIMARY, fg="white")
        title.pack(pady=20)
        
        # Create a canvas with scrollbar for the main content
        canvas_frame = tk.Frame(self.root, bg=COLOR_BACKGROUND)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(canvas_frame, bg=COLOR_BACKGROUND, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        
        # Create a frame inside the canvas to hold all content
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLOR_BACKGROUND)
        
        # Bind the frame to the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create window in canvas - centered
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Center content when canvas is resized
        def _on_canvas_configure(event):
            canvas_width = event.width
            frame_width = self.scrollable_frame.winfo_reqwidth()
            x_position = max(0, (canvas_width - frame_width) // 2)
            self.canvas.coords(self.canvas_window, x_position, 0)
        
        self.canvas.bind("<Configure>", _on_canvas_configure)
        
        # Bind mousewheel to scroll
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Main content frame (now inside scrollable_frame)
        main_frame = tk.Frame(self.scrollable_frame, bg=COLOR_BACKGROUND)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Category selection
        category_frame = tk.LabelFrame(main_frame, text="Select Category", 
                                      font=("Arial", 12, "bold"), bg=COLOR_BACKGROUND, 
                                      padx=10, pady=10)
        category_frame.pack(fill=tk.X, pady=10)
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(category_frame, 
                                          textvariable=self.category_var,
                                          font=("Arial", 11),
                                          state="readonly",
                                          width=30)
        self.update_category_list()
        self.category_combo.pack(side=tk.LEFT, padx=5)
        
        # Filter checkboxes
        filters_frame = tk.Frame(category_frame, bg=COLOR_BACKGROUND)
        filters_frame.pack(side=tk.LEFT, padx=15)
        
        self.only_new_var = tk.BooleanVar(value=False)
        tk.Checkbutton(filters_frame, text="🌟 Only New (Not Started)",
                      variable=self.only_new_var, font=("Arial", 10),
                      bg=COLOR_BACKGROUND, cursor="hand2").pack(anchor=tk.W)
        
        self.include_completed_var = tk.BooleanVar(value=False)
        tk.Checkbutton(filters_frame, text="✅ Include Completed",
                      variable=self.include_completed_var, font=("Arial", 10),
                      bg=COLOR_BACKGROUND, cursor="hand2").pack(anchor=tk.W)
        
        self.random_category_var = tk.BooleanVar(value=False)
        tk.Checkbutton(filters_frame, text="🎰 Random Category",
                      variable=self.random_category_var, font=("Arial", 10),
                      bg=COLOR_BACKGROUND, cursor="hand2").pack(anchor=tk.W)
        
        # Result display
        result_frame = tk.LabelFrame(main_frame, text="Selected Activity", 
                                    font=("Arial", 12, "bold"), bg=COLOR_BACKGROUND,
                                    padx=10, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Image label
        self.result_label = tk.Label(result_frame, text="🎯 Click 'Pick Random' to start!",
                                     font=("Arial", 16), bg="white",
                                     relief=tk.RAISED, padx=20, pady=40,
                                     wraplength=600)
        self.result_label.pack(fill=tk.BOTH, expand=True)
        
        # Text label below image
        self.result_text_label = tk.Label(result_frame, text="",
                                          font=("Arial", 14, "bold"), bg=COLOR_BACKGROUND,
                                          fg="#2c3e50", wraplength=600, pady=10)
        self.result_text_label.pack(fill=tk.X)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=COLOR_BACKGROUND)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Inner frame to center buttons
        buttons_container = tk.Frame(button_frame, bg=COLOR_BACKGROUND)
        buttons_container.pack()
        
        # Pick random button
        tk.Button(buttons_container, text="🎲 Pick Random Activity",
                 command=self.pick_random, font=("Arial", 12, "bold"),
                 bg=COLOR_SUCCESS, fg="white", padx=20, pady=10,
                 cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Regenerate image button (initially hidden)
        self.regen_btn = tk.Button(buttons_container, text="🔄 Regenerate Image",
                                   command=self.regenerate_image, font=("Arial", 10),
                                   bg=COLOR_WARNING, fg="white", padx=15, pady=8,
                                   cursor="hand2")
        
        # Update state button (initially hidden)
        self.update_state_btn = tk.Button(buttons_container, text="✏️ Update State",
                                         command=self.quick_update_state, font=("Arial", 10),
                                         bg=COLOR_INFO, fg="white", padx=15, pady=8,
                                         cursor="hand2")
        
        # Management buttons
        self.create_management_buttons(main_frame)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready! 💑", 
                                  font=("Arial", 9), bg="#e0e0e0",
                                  anchor=tk.W, padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status_bar(self, text):
        """Helper method to update status bar text."""
        self.status_bar.config(text=text)
    
    def create_management_buttons(self, parent):
        """Create management buttons for activities and categories."""
        btn_style = {"font": ("Arial", 10), "padx": 10, "pady": 5, "cursor": "hand2"}
        
        # Row 1: Activity management
        mgmt_frame1 = tk.Frame(parent, bg=COLOR_BACKGROUND)
        mgmt_frame1.pack(fill=tk.X, pady=5)
        
        tk.Label(mgmt_frame1, text="Activities:", font=("Arial", 9, "bold"), 
                bg=COLOR_BACKGROUND).pack(side=tk.LEFT, padx=5)
        
        tk.Button(mgmt_frame1, text="➕ Add", command=self.add_activity,
                 bg=COLOR_INFO, fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame1, text="✏️ Edit", command=self.edit_activity,
                 bg=COLOR_WARNING, fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame1, text="🗑️ Remove", command=self.remove_activity,
                 bg=COLOR_DANGER, fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame1, text="✏️ Change State", command=self.change_state,
                 bg="#00BCD4", fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame1, text="📦 Move to Category", command=self.move_activity,
                 bg="#009688", fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame1, text="🎬 Manage Saga", command=self.manage_saga,
                 bg="#FF5722", fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame1, text="📺 Next Episode", command=self.set_next_episode,
                 bg="#9C27B0", fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        # Row 2: Category & View management
        mgmt_frame2 = tk.Frame(parent, bg=COLOR_BACKGROUND)
        mgmt_frame2.pack(fill=tk.X, pady=5)
        
        tk.Label(mgmt_frame2, text="Categories:", font=("Arial", 9, "bold"), 
                bg=COLOR_BACKGROUND).pack(side=tk.LEFT, padx=5)
        
        tk.Button(mgmt_frame2, text="📁 New", command=self.add_category,
                 bg="#9C27B0", fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame2, text="✏️ Rename", command=self.edit_category,
                 bg="#673AB7", fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame2, text="🗑️ Delete", command=self.delete_category,
                 bg="#E91E63", fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Label(mgmt_frame2, text=" | ", font=("Arial", 9), 
                bg=COLOR_BACKGROUND).pack(side=tk.LEFT, padx=5)
        
        tk.Button(mgmt_frame2, text="📋 View All", command=self.view_all,
                 bg="#795548", fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame2, text="📊 History", command=self.view_history,
                 bg="#607D8B", fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame2, text="⚙️ Settings", command=self.open_settings,
                 bg="#455A64", fg="white", **btn_style).pack(side=tk.LEFT, padx=2)
    
    def update_category_list(self):
        """Update the category dropdown."""
        categories = self.data_manager.get_categories()
        self.category_combo['values'] = categories
        if categories and not self.category_var.get():
            self.category_combo.current(0)
    
    def pick_random(self):
        """Pick a random activity from selected category."""
        random_category = self.random_category_var.get()
        
        # If random category is selected, pick a random category first
        if random_category:
            available_categories = [cat for cat in self.data_manager.get_categories() 
                                   if self.data_manager.get_activities(cat)]
            if not available_categories:
                messagebox.showwarning("No Categories", "No categories with activities found!")
                return
            category = random.choice(available_categories)
            self.category_var.set(category)
        else:
            category = self.category_var.get()
        
        if not category:
            messagebox.showwarning("No Category", "Please select a category first!")
            return
        
        activities = self.data_manager.get_activities(category)
        if not activities:
            messagebox.showinfo("Empty", f"No activities in '{category}'!")
            return
        
        only_new = self.only_new_var.get()
        include_completed = self.include_completed_var.get()
        
        # Filter activities based on state
        if only_new:
            available_activities = [item for item in activities 
                                   if item["state"] not in ["Seen", "Played", "Done", 
                                                           "Watching", "Playing", "In Progress"]]
            filter_msg = "new"
        elif include_completed:
            available_activities = activities
            filter_msg = "all"
        else:
            available_activities = [item for item in activities 
                                   if item["state"] not in ["Seen", "Played", "Done"]]
            filter_msg = "available"
        
        if not available_activities:
            messagebox.showinfo("No Activities", 
                              f"No {filter_msg} activities in '{category}'!")
            return
        
        # Filter out saga items with incomplete prerequisites
        if include_completed:
            saga_filtered = available_activities
        else:
            saga_filtered = self.data_manager.filter_saga_prerequisites(available_activities, category)
        
        if not saga_filtered:
            messagebox.showinfo("Saga Lock", 
                              "All available activities require completing previous saga items first!")
            return
        
        # Weighted selection: items "in progress" get double probability
        weighted_list = []
        for item in saga_filtered:
            weighted_list.append(item)
            if item["state"] in IN_PROGRESS_STATES:
                weighted_list.append(item)  # Add twice for double probability
        
        selected_item = random.choice(weighted_list)
        activity_name = selected_item["name"]
        activity_state = selected_item["state"]
        
        # Update display with animation effect
        self.result_label.config(text="🎲 Selecting...", bg="#ffeb3b", image='')
        self.result_text_label.config(text="")
        self.current_image = None
        self.root.update()
        self.root.after(300)
        
        priority_marker = "⚡" if activity_state in IN_PROGRESS_STATES else "🎯"
        info_text = f"{priority_marker} {activity_name}\n({activity_state})"
        
        # Add next episode info for series
        if category.lower() == "series" and selected_item.get("next_episode"):
            info_text += f"\n📺 Next: {selected_item['next_episode']}"
        
        # Store current activity
        self.current_activity = activity_name
        self.current_category = category
        
        # Generate or load image if enabled
        if self.config_manager.get("enable_images", True) and PIL_AVAILABLE:
            try:
                self.result_label.config(text="🎨 Loading image...", bg="#9C27B0", fg="white")
                self.root.update()
                
                image = self.image_service.get_activity_image(activity_name, category)
                if image:
                    self.result_label.config(image=image, text='', compound=tk.CENTER, bg="white")
                    self.current_image = image
                    self.result_text_label.config(text=info_text)
                    self.regen_btn.pack(side=tk.LEFT, padx=5)
                    self.update_state_btn.pack(side=tk.LEFT, padx=5)
                else:
                    self.result_label.config(text=info_text, bg=COLOR_SUCCESS, fg="white", image='')
                    self.result_text_label.config(text="")
                    self.regen_btn.pack_forget()
                    self.update_state_btn.pack(side=tk.LEFT, padx=5)
            except Exception as e:
                messagebox.showwarning("Image Error", str(e))
                self.result_label.config(text=info_text, bg=COLOR_SUCCESS, fg="white", image='')
                self.result_text_label.config(text="")
                self.regen_btn.pack_forget()
                self.update_state_btn.pack(side=tk.LEFT, padx=5)
        else:
            self.result_label.config(text=info_text, bg=COLOR_SUCCESS, fg="white", image='')
            self.result_text_label.config(text="")
            self.regen_btn.pack_forget()
            self.update_state_btn.pack(side=tk.LEFT, padx=5)
        
        # Add to history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.history.append(f"[{timestamp}] {category}: {activity_name} ({activity_state})")
        
        total = len(activities)
        available = len(available_activities)
        in_progress_count = sum(1 for item in available_activities 
                               if item["state"] in IN_PROGRESS_STATES)
        
        status_text = f"Selected: {activity_name} | {filter_msg.capitalize()}: {available}/{total}"
        if in_progress_count > 0 and not only_new:
            status_text += f" (⚡{in_progress_count} in progress)"
        self.status_bar.config(text=status_text + " 💑")
    
    def regenerate_image(self):
        """Regenerate the image for the current activity."""
        if not self.current_activity or not self.current_category:
            messagebox.showwarning("No Activity", "Pick a random activity first!")
            return
        
        if not self.config_manager.get("enable_images", True) or not PIL_AVAILABLE:
            messagebox.showwarning("Images Disabled", "Image generation is not enabled!")
            return
        
        # Delete cached image
        self.image_service.delete_cached_image(self.current_activity)
        
        # Show loading message
        self.result_label.config(text="🔄 Regenerating image...", bg="#9C27B0", fg="white", image='')
        self.result_text_label.config(text="Please wait...")
        self.current_image = None
        self.root.update()
        
        # Generate new image
        try:
            image = self.image_service.get_activity_image(self.current_activity, self.current_category)
            
            if image:
                self.result_label.config(image=image, text='', compound=tk.CENTER, bg="white")
                self.current_image = image
                
                # Restore text
                activities = self.data_manager.get_activities(self.current_category)
                activity_dict = next((item for item in activities 
                                     if item["name"] == self.current_activity), None)
                if activity_dict:
                    priority_marker = "⚡" if activity_dict["state"] in IN_PROGRESS_STATES else "🎯"
                    info_text = f"{priority_marker} {self.current_activity}\n({activity_dict['state']})"
                    if self.current_category.lower() == "series" and activity_dict.get("next_episode"):
                        info_text += f"\n📺 Next: {activity_dict['next_episode']}"
                    self.result_text_label.config(text=info_text)
                
                messagebox.showinfo("Success", "Image regenerated successfully!")
            else:
                self.result_label.config(text="❌ Failed to generate image", bg=COLOR_DANGER, fg="white")
                self.result_text_label.config(text="")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.result_label.config(text="❌ Failed to generate image", bg=COLOR_DANGER, fg="white")
            self.result_text_label.config(text="")
    
    def quick_update_state(self):
        """Quickly update the state of the currently selected activity."""
        if not self.current_activity or not self.current_category:
            messagebox.showwarning("No Activity", "Pick a random activity first!")
            return
        
        # Find the activity
        activities = self.data_manager.get_activities(self.current_category)
        activity_dict = next((item for item in activities 
                             if item["name"] == self.current_activity), None)
        
        if not activity_dict:
            messagebox.showerror("Error", "Could not find the selected activity!")
            return
        
        # Create state update window
        state_window = tk.Toplevel(self.root)
        state_window.title("Update State")
        state_window.geometry("400x250")
        
        tk.Label(state_window, text=f"Update state for:",
                font=("Arial", 10, "bold")).pack(pady=10)
        
        tk.Label(state_window, text=self.current_activity,
                font=("Arial", 12), fg=COLOR_INFO, wraplength=350).pack(pady=5)
        
        tk.Label(state_window, text=f"Current state: {activity_dict['state']}",
                font=("Arial", 10), fg="#666").pack(pady=5)
        
        # State selection
        state_frame = tk.Frame(state_window)
        state_frame.pack(pady=15)
        
        tk.Label(state_frame, text="New State:", font=("Arial", 10, "bold")).pack(pady=5)
        
        state_var = tk.StringVar(value=activity_dict['state'])
        states = self.data_manager.get_states_for_category(self.current_category)
        
        state_combo = ttk.Combobox(state_frame, textvariable=state_var,
                                  values=states, state="readonly", width=20,
                                  font=("Arial", 11))
        state_combo.pack(pady=5)
        
        def do_update():
            new_state = state_var.get()
            old_state = activity_dict['state']
            
            if new_state == old_state:
                messagebox.showinfo("No Change", "State is already set to this value!")
                return
            
            # Update using data manager
            self.data_manager.update_activity(self.current_category, self.current_activity, 
                                             {"state": new_state})
            
            # Update display
            priority_marker = "⚡" if new_state in IN_PROGRESS_STATES else "🎯"
            info_text = f"{priority_marker} {self.current_activity}\n({new_state})"
            
            if self.current_category.lower() == "series" and activity_dict.get("next_episode"):
                info_text += f"\n📺 Next: {activity_dict['next_episode']}"
            
            self.result_text_label.config(text=info_text)
            self.status_bar.config(text=f"Updated: {self.current_activity} → {new_state} ✏️")
            state_window.destroy()
            messagebox.showinfo("Success", 
                              f"Updated '{self.current_activity}' from '{old_state}' to '{new_state}'!")
        
        # Buttons
        btn_frame = tk.Frame(state_window)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="✅ Update State", command=do_update,
                 bg=COLOR_SUCCESS, fg="white", padx=20, pady=8,
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Cancel", command=state_window.destroy,
                 bg="#757575", fg="white", padx=20, pady=8,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    # Placeholder methods for management buttons
    # (These would contain the full implementation from the original file)
    
    def add_activity(self):
        """Add a new activity."""
        category = self.category_var.get()
        ActivityDialogs.add_activity(
            self.root,
            category,
            self.data_manager,
            self.update_status_bar
        )
    
    def edit_activity(self):
        """Edit an activity."""
        category = self.category_var.get()
        ActivityDialogs.edit_activity(
            self.root,
            category,
            self.data_manager,
            self.update_status_bar
        )
    
    def remove_activity(self):
        """Remove an activity."""
        category = self.category_var.get()
        ActivityDialogs.remove_activity(
            self.root,
            category,
            self.data_manager,
            self.update_status_bar
        )
    
    def change_state(self):
        """Change activity state."""
        category = self.category_var.get()
        ActivityDialogs.change_state(
            self.root,
            category,
            self.data_manager,
            self.update_status_bar
        )
    
    def move_activity(self):
        """Move activity to another category."""
        category = self.category_var.get()
        ActivityDialogs.move_activity(
            self.root,
            category,
            self.data_manager,
            self.update_status_bar
        )
    
    def manage_saga(self):
        """Manage saga information."""
        category = self.category_var.get()
        SagaDialogs.manage_saga(
            self.root,
            category,
            self.data_manager,
            self.update_status_bar
        )
    
    def set_next_episode(self):
        """Set next episode for series."""
        category = self.category_var.get()
        EpisodeDialogs.set_next_episode(
            self.root,
            category,
            self.data_manager,
            self.update_status_bar
        )
    
    def add_category(self):
        """Add a new category."""
        category = simpledialog.askstring("New Category", "Enter new category name:")
        
        if category:
            category = category.strip().lower()
            if self.data_manager.add_category(category):
                self.update_category_list()
                self.category_var.set(category)
                messagebox.showinfo("Success", f"Created category '{category}'!")
                self.status_bar.config(text=f"New category: {category} 📁")
            else:
                messagebox.showinfo("Duplicate", "This category already exists!")
    
    def edit_category(self):
        """Rename a category."""
        def on_category_update(new_category=None):
            self.update_category_list()
            if new_category:
                self.category_var.set(new_category)
        
        CategoryDialogs.edit_category(
            self.root,
            self.data_manager,
            on_category_update,
            self.update_status_bar
        )
    
    def delete_category(self):
        """Delete a category."""
        def on_category_deleted():
            self.update_category_list()
            # Set to first available category or create default
            categories = self.data_manager.get_categories()
            if categories:
                self.category_var.set(categories[0])
            else:
                self.data_manager.add_category("movies")
                self.update_category_list()
                self.category_var.set("movies")
        
        CategoryDialogs.delete_category(
            self.root,
            self.data_manager,
            on_category_deleted,
            self.update_status_bar
        )
    
    def view_all(self):
        """View all activities."""
        ViewDialogs.view_all(self.root, self.data_manager)
    
    def view_history(self):
        """View selection history."""
        history_window = tk.Toplevel(self.root)
        history_window.title("Selection History")
        history_window.geometry("500x400")
        
        text_widget = tk.Text(history_window, font=("Arial", 10), wrap=tk.WORD)
        scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if self.history:
            text_widget.insert(tk.END, "📊 Activity Selection History\n\n", "title")
            for entry in reversed(self.history):
                text_widget.insert(tk.END, f"{entry}\n")
        else:
            text_widget.insert(tk.END, "No history yet. Start picking activities! 🎲")
        
        text_widget.tag_config("title", font=("Arial", 12, "bold"))
        text_widget.config(state=tk.DISABLED)
    
    def open_settings(self):
        """Open settings dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("600x400")
        
        tk.Label(settings_window, text="⚙️ Settings", 
                font=("Arial", 14, "bold")).pack(pady=15)
        
        # API Key section
        api_frame = tk.LabelFrame(settings_window, text="OpenAI API Configuration", 
                                 font=("Arial", 11, "bold"), padx=15, pady=15)
        api_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(api_frame, text="API Key:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        api_key_var = tk.StringVar(value=self.config_manager.get("openai_api_key", ""))
        api_entry = tk.Entry(api_frame, textvariable=api_key_var, font=("Arial", 10), 
                            width=50, show="*")
        api_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(api_frame, text="Get your API key at: https://platform.openai.com/api-keys", 
                font=("Arial", 8), fg="#666").grid(row=1, column=0, columnspan=2, pady=5)
        
        # Image settings
        img_frame = tk.LabelFrame(settings_window, text="Image Settings", 
                                 font=("Arial", 11, "bold"), padx=15, pady=15)
        img_frame.pack(fill=tk.X, padx=20, pady=10)
        
        enable_var = tk.BooleanVar(value=self.config_manager.get("enable_images", True))
        tk.Checkbutton(img_frame, text="✅ Enable AI Image Generation", 
                      variable=enable_var, font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        def save_settings():
            self.config_manager.update(
                openai_api_key=api_key_var.get().strip(),
                enable_images=enable_var.get()
            )
            self.config_manager.save()
            messagebox.showinfo("Success", "Settings saved!")
            settings_window.destroy()
        
        def clear_cache():
            confirm = messagebox.askyesno("Clear Cache", 
                                         "Delete all cached images?\n\nThey will be regenerated next time.")
            if confirm:
                count = self.image_service.clear_cache()
                messagebox.showinfo("Cache Cleared", f"Deleted {count} cached images.")
        
        # Buttons
        btn_frame = tk.Frame(settings_window)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="💾 Save Settings", command=save_settings,
                 bg=COLOR_SUCCESS, fg="white", padx=20, pady=8,
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Clear Image Cache", command=clear_cache,
                 bg=COLOR_WARNING, fg="white", padx=20, pady=8,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Cancel", command=settings_window.destroy,
                 bg="#757575", fg="white", padx=20, pady=8,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = ActivitySelectorRefactored(root)
    root.mainloop()


if __name__ == "__main__":
    main()
