import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import yaml
import random
from datetime import datetime
import os
import json
from pathlib import Path
try:
    from PIL import Image, ImageTk
    import requests
    from io import BytesIO
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class ActivitySelector:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Activity Selector - What to do today?")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        
        # Data file
        self.data_file = "activities_data.yml"
        self.config_file = "config.yml"
        self.image_cache_dir = Path("image_cache")
        self.image_cache_dir.mkdir(exist_ok=True)
        
        self.load_config()
        self.load_data()
        
        # History
        self.history = []
        
        # Current image reference
        self.current_image = None
        
        self.create_widgets()
        
    def load_data(self):
        """Load activities from YAML file or create default data"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.activities = yaml.safe_load(f) or {}
            # Ensure all activities have the new structure with state
            self._migrate_old_data()
        else:
            # Default categories and activities with states
            self.activities = {
                "videogame": [
                    {"name": "Play Mario Kart", "state": "Not Played"},
                    {"name": "Play Minecraft together", "state": "Not Played"},
                    {"name": "Try a co-op adventure game", "state": "Not Played"},
                    {"name": "Play Overcooked 2", "state": "Not Played"}
                ],
                "series": [
                    {"name": "Watch a comedy series", "state": "Not Seen"},
                    {"name": "Start a new Netflix show", "state": "Not Seen"},
                    {"name": "Rewatch favorite episodes", "state": "Not Seen"},
                    {"name": "Binge-watch a mini-series", "state": "Not Seen"}
                ],
                "movie": [
                    {"name": "Watch a romantic comedy", "state": "Not Seen"},
                    {"name": "Watch an action movie", "state": "Not Seen"},
                    {"name": "Watch a classic film", "state": "Not Seen"},
                    {"name": "Watch a documentary", "state": "Not Seen"}
                ]
            }
            self.save_data()
    
    def load_config(self):
        """Load configuration including API key"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
        else:
            self.config = {
                "openai_api_key": "",
                "enable_images": True,
                "image_style": "vibrant digital art"
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def _migrate_old_data(self):
        """Migrate old string-based data to new dict-based structure"""
        for category in self.activities:
            new_list = []
            for item in self.activities[category]:
                if isinstance(item, str):
                    # Old format, migrate to new format
                    state = self._get_default_state(category)
                    new_list.append({"name": item, "state": state})
                elif isinstance(item, dict):
                    # Already new format, ensure it has both fields
                    if "name" not in item:
                        continue
                    if "state" not in item:
                        item["state"] = self._get_default_state(category)
                    # Add saga fields if missing
                    if "saga" not in item:
                        item["saga"] = None
                    if "order" not in item:
                        item["order"] = None
                    new_list.append(item)
            self.activities[category] = new_list
        self.save_data()
    
    def _get_default_state(self, category):
        """Get the default state based on category"""
        if category.lower() == "videogame":
            return "Not Played"
        elif category.lower() in ["series", "movie"]:
            return "Not Seen"
        else:
            return "Pending"
    
    def save_data(self):
        """Save activities to YAML file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.activities, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#4a90e2", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title = tk.Label(title_frame, text="🎲 Activity Selector 💕", 
                        font=("Arial", 24, "bold"), bg="#4a90e2", fg="white")
        title.pack(pady=20)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Category selection
        category_frame = tk.LabelFrame(main_frame, text="Select Category", 
                                      font=("Arial", 12, "bold"), bg="#f0f0f0", 
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
        filters_frame = tk.Frame(category_frame, bg="#f0f0f0")
        filters_frame.pack(side=tk.LEFT, padx=15)
        
        self.only_new_var = tk.BooleanVar(value=False)
        self.only_new_check = tk.Checkbutton(filters_frame, 
                                             text="🌟 Only New (Not Started)",
                                             variable=self.only_new_var,
                                             font=("Arial", 10),
                                             bg="#f0f0f0",
                                             cursor="hand2")
        self.only_new_check.pack(anchor=tk.W)
        
        self.include_completed_var = tk.BooleanVar(value=False)
        self.include_completed_check = tk.Checkbutton(filters_frame, 
                                                      text="✅ Include Completed",
                                                      variable=self.include_completed_var,
                                                      font=("Arial", 10),
                                                      bg="#f0f0f0",
                                                      cursor="hand2")
        self.include_completed_check.pack(anchor=tk.W)
        
        # Result display
        result_frame = tk.LabelFrame(main_frame, text="Selected Activity", 
                                    font=("Arial", 12, "bold"), bg="#f0f0f0",
                                    padx=10, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Image label
        self.result_label = tk.Label(result_frame, text="🎯 Click 'Pick Random' to start!",
                                     font=("Arial", 16), bg="#ffffff",
                                     relief=tk.RAISED, padx=20, pady=40,
                                     wraplength=600)
        self.result_label.pack(fill=tk.BOTH, expand=True)
        
        # Text label below image
        self.result_text_label = tk.Label(result_frame, text="",
                                          font=("Arial", 14, "bold"), bg="#f0f0f0",
                                          fg="#2c3e50", wraplength=600, pady=10)
        self.result_text_label.pack(fill=tk.X)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)
        
        # Inner frame to center buttons horizontally
        buttons_container = tk.Frame(button_frame, bg="#f0f0f0")
        buttons_container.pack()
        
        # Pick random button
        self.pick_btn = tk.Button(buttons_container, text="🎲 Pick Random Activity",
                                 command=self.pick_random,
                                 font=("Arial", 12, "bold"),
                                 bg="#4CAF50", fg="white",
                                 padx=20, pady=10,
                                 cursor="hand2")
        self.pick_btn.pack(side=tk.LEFT, padx=5)
        
        # Regenerate image button (initially hidden)
        self.regen_btn = tk.Button(buttons_container, text="🔄 Regenerate Image",
                                   command=self.regenerate_image,
                                   font=("Arial", 10),
                                   bg="#FF9800", fg="white",
                                   padx=15, pady=8,
                                   cursor="hand2")
        # Don't pack it yet - will show after first selection
        
        # Store current activity for regeneration
        self.current_activity = None
        self.current_category = None
        
        # Management buttons - Row 1: Activity management
        mgmt_frame1 = tk.Frame(main_frame, bg="#f0f0f0")
        mgmt_frame1.pack(fill=tk.X, pady=5)
        
        btn_style = {"font": ("Arial", 10), "padx": 10, "pady": 5, "cursor": "hand2"}
        
        tk.Label(mgmt_frame1, text="Activities:", font=("Arial", 9, "bold"), 
                bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        tk.Button(mgmt_frame1, text="➕ Add", 
                 command=self.add_activity, bg="#2196F3", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame1, text="✏️ Edit",
                 command=self.edit_activity, bg="#FF9800", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame1, text="🗑️ Remove",
                 command=self.remove_activity, bg="#f44336", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame1, text="✏️ Change State",
                 command=self.change_state, bg="#00BCD4", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame1, text="📦 Move to Category",
                 command=self.move_activity, bg="#009688", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame1, text="🎬 Manage Saga",
                 command=self.manage_saga, bg="#FF5722", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        # Management buttons - Row 2: Category & View management
        mgmt_frame2 = tk.Frame(main_frame, bg="#f0f0f0")
        mgmt_frame2.pack(fill=tk.X, pady=5)
        
        tk.Label(mgmt_frame2, text="Categories:", font=("Arial", 9, "bold"), 
                bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        tk.Button(mgmt_frame2, text="📁 New",
                 command=self.add_category, bg="#9C27B0", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame2, text="✏️ Rename",
                 command=self.edit_category, bg="#673AB7", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame2, text="�️ Delete",
                 command=self.delete_category, bg="#E91E63", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Label(mgmt_frame2, text=" | ", font=("Arial", 9), 
                bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        tk.Button(mgmt_frame2, text="� View All",
                 command=self.view_all, bg="#795548", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame2, text="📊 History",
                 command=self.view_history, bg="#607D8B", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(mgmt_frame2, text="⚙️ Settings",
                 command=self.open_settings, bg="#455A64", fg="white",
                 **btn_style).pack(side=tk.LEFT, padx=2)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready! 💑", 
                                  font=("Arial", 9), bg="#e0e0e0",
                                  anchor=tk.W, padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_category_list(self):
        """Update the category dropdown"""
        categories = list(self.activities.keys())
        self.category_combo['values'] = categories
        if categories and not self.category_var.get():
            self.category_combo.current(0)
    
    def pick_random(self):
        """Pick a random activity from selected category (excluding Seen/Played items unless checkbox enabled)"""
        category = self.category_var.get()
        
        if not category:
            messagebox.showwarning("No Category", "Please select a category first!")
            return
        
        if not self.activities.get(category):
            messagebox.showinfo("Empty Category", 
                              f"No activities in '{category}' yet. Add some first!")
            return
        
        only_new = self.only_new_var.get()
        include_completed = self.include_completed_var.get()
        
        # Filter activities based on state
        if only_new:
            # Only show items that haven't been started
            available_activities = [
                item for item in self.activities[category]
                if item["state"] in ["Not Seen", "Not Played", "Pending"]
            ]
            filter_msg = "new/unstarted"
        elif include_completed:
            # Include ALL activities (even completed)
            available_activities = self.activities[category][:]
            filter_msg = "all"
        else:
            # Exclude completed items (Seen/Played/Done)
            available_activities = [
                item for item in self.activities[category]
                if item["state"] not in ["Seen", "Played", "Done"]
            ]
            filter_msg = "available"
        
        if not available_activities:
            if only_new:
                messagebox.showinfo("No New Items!", 
                                  f"No new/unstarted activities in '{category}'!\n"
                                  "Uncheck 'Only New' or add new activities.")
            else:
                messagebox.showinfo("All Done!", 
                                  f"All activities in '{category}' are marked as completed!\n"
                                  "Add new activities or change their states.")
            return
        
        # Filter out saga items that have incomplete prerequisites (unless including completed)
        if include_completed:
            saga_filtered = available_activities
        else:
            saga_filtered = self._filter_saga_prerequisites(available_activities, category)
        
        if not saga_filtered:
            messagebox.showinfo("Saga Locked!", 
                              f"All available activities require previous items to be completed!\n"
                              "Complete earlier items in the saga first.")
            return
        
        # Weighted selection: items "in progress" get double probability
        # (Watching for series/movies, Playing for videogames, In Progress for others)
        weighted_list = []
        in_progress_states = ["Watching", "Playing", "In Progress"]
        
        for item in saga_filtered:
            weighted_list.append(item)  # Add once
            if item["state"] in in_progress_states:
                weighted_list.append(item)  # Add again for double probability
        
        selected_item = random.choice(weighted_list)
        activity_name = selected_item["name"]
        activity_state = selected_item["state"]
        
        # Update display with animation effect
        self.result_label.config(text="🎲 Selecting...", bg="#ffeb3b", image='')
        self.result_text_label.config(text="")
        self.current_image = None
        self.root.update()
        self.root.after(300)
        
        priority_marker = "⚡" if activity_state in in_progress_states else "🎯"
        info_text = f"{priority_marker} {activity_name}\n({activity_state})"
        
        # Store current activity for regeneration
        self.current_activity = activity_name
        self.current_category = category
        
        # Generate or load image if enabled
        if self.config.get("enable_images", True) and PIL_AVAILABLE:
            image = self._get_activity_image(activity_name, category)
            if image:
                self.result_label.config(image=image, text='', compound=tk.CENTER, bg="#ffffff")
                self.current_image = image  # Keep reference
                
                # Show text below the image
                self.result_text_label.config(text=info_text)
                
                # Show regenerate button next to Pick Random
                self.regen_btn.pack(side=tk.LEFT, padx=5)
            else:
                # Fallback to text only
                self.result_label.config(text=info_text, bg="#4CAF50", fg="white", image='')
                self.result_text_label.config(text="")
                self.regen_btn.pack_forget()
        else:
            # No images - text only
            self.result_label.config(text=info_text, bg="#4CAF50", fg="white", image='')
            self.result_text_label.config(text="")
            self.regen_btn.pack_forget()
        
        # Add to history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.history.append(f"[{timestamp}] {category}: {activity_name} ({activity_state})")
        
        total = len(self.activities[category])
        available = len(available_activities)
        in_progress_count = sum(1 for item in available_activities if item["state"] in in_progress_states)
        
        status_text = f"Selected: {activity_name} | {filter_msg.capitalize()}: {available}/{total}"
        if in_progress_count > 0 and not only_new:
            status_text += f" (⚡{in_progress_count} in progress)"
        self.status_bar.config(text=status_text + " 💑")
    
    def regenerate_image(self):
        """Regenerate the image for the current activity"""
        if not self.current_activity or not self.current_category:
            messagebox.showwarning("No Activity", "Pick a random activity first!")
            return
        
        if not self.config.get("enable_images", True) or not PIL_AVAILABLE:
            messagebox.showwarning("Images Disabled", "Image generation is not enabled!")
            return
        
        # Delete cached image
        safe_name = "".join(c for c in self.current_activity if c.isalnum() or c in (' ', '-', '_')).rstrip()
        cache_file = self.image_cache_dir / f"{safe_name}.png"
        
        if cache_file.exists():
            cache_file.unlink()
        
        # Show loading message
        self.result_label.config(text="🔄 Regenerating image...", bg="#9C27B0", fg="white", image='')
        self.result_text_label.config(text="Please wait...")
        self.current_image = None
        self.root.update()
        
        # Generate new image
        image = self._get_activity_image(self.current_activity, self.current_category)
        
        if image:
            self.result_label.config(image=image, text='', compound=tk.CENTER, bg="#ffffff")
            self.current_image = image
            
            # Restore text
            activity_dict = next((item for item in self.activities[self.current_category] 
                                 if item["name"] == self.current_activity), None)
            if activity_dict:
                in_progress_states = ["Watching", "Playing", "In Progress"]
                priority_marker = "⚡" if activity_dict["state"] in in_progress_states else "🎯"
                info_text = f"{priority_marker} {self.current_activity}\n({activity_dict['state']})"
                self.result_text_label.config(text=info_text)
            
            messagebox.showinfo("Success", "Image regenerated successfully!")
        else:
            self.result_label.config(text="❌ Failed to generate image", bg="#f44336", fg="white")
            self.result_text_label.config(text="")
    
    def add_activity(self):
        """Add a new activity to a category with optional saga info"""
        category = self.category_var.get()
        
        if not category:
            messagebox.showwarning("No Category", "Please select a category first!")
            return
        
        # Create add activity window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Activity")
        add_window.geometry("500x300")
        
        tk.Label(add_window, text=f"Add new activity to '{category}':",
                font=("Arial", 11, "bold")).pack(pady=10)
        
        # Activity name
        name_frame = tk.Frame(add_window)
        name_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(name_frame, text="Activity Name:", font=("Arial", 10)).pack(anchor=tk.W)
        name_entry = tk.Entry(name_frame, font=("Arial", 10), width=50)
        name_entry.pack(fill=tk.X, pady=5)
        name_entry.focus()
        
        # Saga info (optional)
        saga_frame = tk.LabelFrame(add_window, text="Saga Info (Optional)", 
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        saga_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Get existing sagas
        existing_sagas = set()
        for item in self.activities[category]:
            saga = item.get("saga")
            if saga:
                existing_sagas.add(saga)
        existing_sagas_list = sorted(list(existing_sagas))
        
        saga_inner = tk.Frame(saga_frame)
        saga_inner.pack(fill=tk.X)
        
        tk.Label(saga_inner, text="Saga:", font=("Arial", 9)).grid(row=0, column=0, sticky=tk.W, padx=5)
        saga_var = tk.StringVar()
        saga_combo = ttk.Combobox(saga_inner, textvariable=saga_var,
                                 font=("Arial", 10), width=25)
        saga_combo['values'] = existing_sagas_list
        saga_combo.grid(row=0, column=1, padx=5)
        
        tk.Label(saga_inner, text="Order:", font=("Arial", 9)).grid(row=0, column=2, sticky=tk.W, padx=5)
        order_entry = tk.Entry(saga_inner, font=("Arial", 10), width=10)
        order_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(saga_frame, text="Leave empty if not part of a saga", 
                font=("Arial", 8), fg="#666").pack(pady=5)
        
        def do_add():
            activity_name = name_entry.get().strip()
            
            if not activity_name:
                messagebox.showwarning("Empty Name", "Please enter an activity name!")
                return
            
            # Check if activity already exists
            existing_names = [item["name"] for item in self.activities[category]]
            if activity_name in existing_names:
                messagebox.showwarning("Duplicate", "This activity already exists!")
                return
            
            # Get saga info
            saga_name = saga_var.get().strip()
            order_str = order_entry.get().strip()
            
            # Validate saga info if provided
            saga = None
            order = None
            
            if saga_name or order_str:
                if not saga_name:
                    messagebox.showwarning("Missing Saga", "Please enter a saga name!")
                    return
                if not order_str:
                    messagebox.showwarning("Missing Order", "Please enter an order number!")
                    return
                
                try:
                    order = int(order_str)
                    if order < 1:
                        raise ValueError()
                except ValueError:
                    messagebox.showwarning("Invalid Order", "Order must be a positive number!")
                    return
                
                saga = saga_name
                
                # Check for duplicate order in saga
                for item in self.activities[category]:
                    if item.get("saga") == saga and item.get("order") == order:
                        messagebox.showwarning("Duplicate Order", 
                                             f"Order #{order} already exists in '{saga}' saga!")
                        return
            
            # Create new item
            default_state = self._get_default_state(category)
            new_item = {"name": activity_name, "state": default_state, "saga": saga, "order": order}
            self.activities[category].append(new_item)
            self.save_data()
            
            saga_info = f" (Saga: {saga} #{order})" if saga else ""
            messagebox.showinfo("Success", f"Added '{activity_name}'{saga_info} to {category}!")
            self.status_bar.config(text=f"Added: {activity_name} ✅")
            add_window.destroy()
        
        # Buttons
        btn_frame = tk.Frame(add_window)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Add Activity", command=do_add,
                 bg="#2196F3", fg="white", padx=20, pady=8,
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Cancel", command=add_window.destroy,
                 bg="#757575", fg="white", padx=20, pady=8,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to add
        name_entry.bind('<Return>', lambda e: do_add())
    
    def edit_activity(self):
        """Edit an existing activity's name"""
        category = self.category_var.get()
        
        if not category:
            messagebox.showwarning("No Category", "Please select a category first!")
            return
        
        if not self.activities[category]:
            messagebox.showinfo("Empty", f"No activities in '{category}' to edit!")
            return
        
        # Create selection window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Activity")
        edit_window.geometry("600x400")
        
        tk.Label(edit_window, text=f"Select activity to edit in '{category}':",
                font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(edit_window, font=("Arial", 10), width=60)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def refresh_listbox():
            """Refresh the listbox with current data"""
            listbox.delete(0, tk.END)
            for item in self.activities[category]:
                display_text = f"{item['name']} [{item['state']}]"
                listbox.insert(tk.END, display_text)
        
        refresh_listbox()
        
        def do_edit():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select an activity to edit!")
                return
            
            idx = selection[0]
            item = self.activities[category][idx]
            old_name = item['name']
            
            new_name = simpledialog.askstring("Edit Activity", 
                                             f"Edit activity name:",
                                             initialvalue=old_name)
            
            if new_name and new_name.strip():
                new_name = new_name.strip()
                # Check if new name already exists (excluding current item)
                existing_names = [i["name"] for i in self.activities[category] if i != item]
                if new_name not in existing_names:
                    item['name'] = new_name
                    self.save_data()
                    messagebox.showinfo("Success", f"Renamed '{old_name}' to '{new_name}'!")
                    self.status_bar.config(text=f"Updated: {new_name} ✏️")
                    # Refresh the listbox instead of closing
                    refresh_listbox()
                else:
                    messagebox.showwarning("Duplicate", "An activity with this name already exists!")
        
        btn_frame = tk.Frame(edit_window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Edit Selected", command=do_edit,
                 bg="#FF9800", fg="white", padx=20, pady=5,
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Close", command=edit_window.destroy,
                 bg="#757575", fg="white", padx=20, pady=5,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    def remove_activity(self):
        """Remove an activity from a category"""
        category = self.category_var.get()
        
        if not category:
            messagebox.showwarning("No Category", "Please select a category first!")
            return
        
        if not self.activities[category]:
            messagebox.showinfo("Empty", f"No activities in '{category}' to remove!")
            return
        
        # Create selection window
        select_window = tk.Toplevel(self.root)
        select_window.title("Remove Activity")
        select_window.geometry("500x350")
        
        tk.Label(select_window, text=f"Select activity to remove from '{category}':",
                font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(select_window, font=("Arial", 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for item in self.activities[category]:
            display_text = f"{item['name']} [{item['state']}]"
            listbox.insert(tk.END, display_text)
        
        def do_remove():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                item = self.activities[category][idx]
                activity_name = item['name']
                self.activities[category].remove(item)
                self.save_data()
                select_window.destroy()
                messagebox.showinfo("Success", f"Removed '{activity_name}'!")
                self.status_bar.config(text=f"Removed: {activity_name} 🗑️")
        
        tk.Button(select_window, text="Remove Selected", command=do_remove,
                 bg="#f44336", fg="white", padx=20, pady=5).pack(pady=10)
    
    def add_category(self):
        """Add a new category"""
        category = simpledialog.askstring("New Category", 
                                         "Enter new category name:")
        
        if category:
            category = category.strip().lower()
            if category not in self.activities:
                self.activities[category] = []
                self.save_data()
                self.update_category_list()
                self.category_var.set(category)
                messagebox.showinfo("Success", f"Created category '{category}'!")
                self.status_bar.config(text=f"New category: {category} 📁")
            else:
                messagebox.showinfo("Duplicate", "This category already exists!")
    
    def edit_category(self):
        """Rename an existing category"""
        if not self.activities:
            messagebox.showinfo("No Categories", "No categories to edit!")
            return
        
        # Create selection window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Rename Category")
        edit_window.geometry("400x350")
        
        tk.Label(edit_window, text="Select category to rename:",
                font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(edit_window, font=("Arial", 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        categories = list(self.activities.keys())
        for cat in categories:
            count = len(self.activities[cat])
            listbox.insert(tk.END, f"{cat} ({count} activities)")
        
        def do_rename():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                old_category = categories[idx]
                
                new_category = simpledialog.askstring("Rename Category", 
                                                     f"Enter new name for '{old_category}':",
                                                     initialvalue=old_category)
                
                if new_category and new_category.strip():
                    new_category = new_category.strip().lower()
                    if new_category != old_category and new_category not in self.activities:
                        # Rename category
                        self.activities[new_category] = self.activities.pop(old_category)
                        self.save_data()
                        self.update_category_list()
                        self.category_var.set(new_category)
                        edit_window.destroy()
                        messagebox.showinfo("Success", f"Renamed '{old_category}' to '{new_category}'!")
                        self.status_bar.config(text=f"Renamed category to: {new_category} ✏️")
                    elif new_category == old_category:
                        messagebox.showinfo("No Change", "Category name is the same!")
                    else:
                        messagebox.showwarning("Duplicate", "A category with this name already exists!")
        
        tk.Button(edit_window, text="Rename Selected", command=do_rename,
                 bg="#673AB7", fg="white", padx=20, pady=5).pack(pady=10)
    
    def delete_category(self):
        """Delete an entire category"""
        if not self.activities:
            messagebox.showinfo("No Categories", "No categories to delete!")
            return
        
        # Create selection window
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Category")
        delete_window.geometry("400x350")
        
        tk.Label(delete_window, text="⚠️ Select category to DELETE (cannot be undone):",
                font=("Arial", 10, "bold"), fg="#f44336").pack(pady=10)
        
        listbox = tk.Listbox(delete_window, font=("Arial", 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        categories = list(self.activities.keys())
        for cat in categories:
            count = len(self.activities[cat])
            listbox.insert(tk.END, f"{cat} ({count} activities)")
        
        def do_delete():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                category_to_delete = categories[idx]
                count = len(self.activities[category_to_delete])
                
                # Confirm deletion
                confirm = messagebox.askyesno("Confirm Deletion", 
                                             f"Are you sure you want to delete '{category_to_delete}' "
                                             f"and all {count} activities?\n\nThis cannot be undone!",
                                             icon='warning')
                
                if confirm:
                    del self.activities[category_to_delete]
                    self.save_data()
                    self.update_category_list()
                    delete_window.destroy()
                    messagebox.showinfo("Deleted", f"Category '{category_to_delete}' has been deleted.")
                    self.status_bar.config(text=f"Deleted category: {category_to_delete} 🗑️")
        
        tk.Button(delete_window, text="Delete Selected", command=do_delete,
                 bg="#E91E63", fg="white", padx=20, pady=5).pack(pady=10)
    
    def view_all(self):
        """View all categories and activities with their states"""
        view_window = tk.Toplevel(self.root)
        view_window.title("All Activities")
        view_window.geometry("600x450")
        
        text_widget = tk.Text(view_window, font=("Arial", 10), wrap=tk.WORD)
        scrollbar = tk.Scrollbar(view_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for category, activities in self.activities.items():
            text_widget.insert(tk.END, f"📂 {category.upper()}\n", "category")
            if activities:
                for item in activities:
                    state = item['state']
                    name = item['name']
                    if state in ["Seen", "Played"]:
                        text_widget.insert(tk.END, f"  • {name} ", "done_name")
                        text_widget.insert(tk.END, f"[{state}]\n", "done_state")
                    else:
                        text_widget.insert(tk.END, f"  • {name} ", "pending_name")
                        text_widget.insert(tk.END, f"[{state}]\n", "pending_state")
            else:
                text_widget.insert(tk.END, f"  (empty)\n", "empty")
            text_widget.insert(tk.END, "\n")
        
        text_widget.tag_config("category", font=("Arial", 11, "bold"), foreground="#2196F3")
        text_widget.tag_config("empty", foreground="#999999", font=("Arial", 9, "italic"))
        text_widget.tag_config("done_name", foreground="#888888")
        text_widget.tag_config("done_state", foreground="#888888", font=("Arial", 9, "italic"))
        text_widget.tag_config("pending_name", foreground="#000000")
        text_widget.tag_config("pending_state", foreground="#4CAF50", font=("Arial", 9, "bold"))
        text_widget.config(state=tk.DISABLED)
    
    def view_history(self):
        """View history of selected activities"""
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
            for entry in reversed(self.history):  # Most recent first
                text_widget.insert(tk.END, f"{entry}\n")
        else:
            text_widget.insert(tk.END, "No history yet. Start picking activities! 🎲")
        
        text_widget.tag_config("title", font=("Arial", 12, "bold"))
        text_widget.config(state=tk.DISABLED)
    
    def change_state(self):
        """Change the state of an activity"""
        category = self.category_var.get()
        
        if not category:
            messagebox.showwarning("No Category", "Please select a category first!")
            return
        
        if not self.activities[category]:
            messagebox.showinfo("Empty", f"No activities in '{category}'!")
            return
        
        # Create selection window
        state_window = tk.Toplevel(self.root)
        state_window.title("Change Activity State")
        state_window.geometry("600x450")
        
        tk.Label(state_window, text=f"Select activity to change state in '{category}':",
                font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(state_window, font=("Arial", 10), width=60)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def refresh_listbox():
            """Refresh the listbox with current data"""
            listbox.delete(0, tk.END)
            for item in self.activities[category]:
                display_text = f"{item['name']} - [{item['state']}]"
                listbox.insert(tk.END, display_text)
        
        refresh_listbox()
        
        # State selection frame
        state_frame = tk.Frame(state_window)
        state_frame.pack(pady=10)
        
        tk.Label(state_frame, text="New State:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        state_var = tk.StringVar()
        
        # Determine available states based on category
        if category.lower() == "videogame":
            states = ["Not Played", "Playing", "Played"]
        elif category.lower() in ["series", "movie"]:
            states = ["Not Seen", "Watching", "Seen"]
        else:
            states = ["Pending", "In Progress", "Done"]
        
        state_combo = ttk.Combobox(state_frame, textvariable=state_var,
                                  values=states, state="readonly", width=20)
        state_combo.pack(side=tk.LEFT, padx=5)
        state_combo.current(0)
        
        def do_change():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select an activity to change state!")
                return
            
            idx = selection[0]
            new_state = state_var.get()
            item = self.activities[category][idx]
            old_state = item['state']
            item['state'] = new_state
            self.save_data()
            messagebox.showinfo("Success", 
                              f"Changed '{item['name']}' from '{old_state}' to '{new_state}'!")
            self.status_bar.config(text=f"Updated: {item['name']} -> {new_state} ✏️")
            # Refresh the listbox instead of closing
            refresh_listbox()
        
        btn_frame = tk.Frame(state_window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Update State", command=do_change,
                 bg="#00BCD4", fg="white", padx=20, pady=5,
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Close", command=state_window.destroy,
                 bg="#757575", fg="white", padx=20, pady=5,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    def move_activity(self):
        """Move an activity to a different category"""
        category = self.category_var.get()
        
        if not category:
            messagebox.showwarning("No Category", "Please select a category first!")
            return
        
        if not self.activities[category]:
            messagebox.showinfo("Empty", f"No activities in '{category}' to move!")
            return
        
        if len(self.activities.keys()) < 2:
            messagebox.showinfo("Need More Categories", 
                              "You need at least 2 categories to move activities between them!\n"
                              "Create a new category first.")
            return
        
        # Create selection window
        move_window = tk.Toplevel(self.root)
        move_window.title("Move Activity to Another Category")
        move_window.geometry("600x500")
        
        tk.Label(move_window, text=f"Select activity to move from '{category}':",
                font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(move_window, font=("Arial", 10), width=60)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for item in self.activities[category]:
            display_text = f"{item['name']} [{item['state']}]"
            listbox.insert(tk.END, display_text)
        
        # Category selection frame
        cat_frame = tk.Frame(move_window)
        cat_frame.pack(pady=10)
        
        tk.Label(cat_frame, text="Move to Category:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        target_cat_var = tk.StringVar()
        
        # Get other categories (exclude current)
        other_categories = [cat for cat in self.activities.keys() if cat != category]
        
        cat_combo = ttk.Combobox(cat_frame, textvariable=target_cat_var,
                                values=other_categories, state="readonly", width=25)
        cat_combo.pack(side=tk.LEFT, padx=5)
        if other_categories:
            cat_combo.current(0)
        
        def do_move():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select an activity to move!")
                return
            
            target_category = target_cat_var.get()
            if not target_category:
                messagebox.showwarning("No Target", "Please select a target category!")
                return
            
            idx = selection[0]
            item = self.activities[category][idx]
            activity_name = item['name']
            
            # Check if activity with same name already exists in target category
            existing_names = [i["name"] for i in self.activities[target_category]]
            if activity_name in existing_names:
                messagebox.showwarning("Duplicate", 
                                      f"An activity named '{activity_name}' already exists in '{target_category}'!\n"
                                      "Rename it first, then try moving.")
                return
            
            # Update state to match new category's default if needed
            old_state = item['state']
            new_default_state = self._get_default_state(target_category)
            
            # Ask if user wants to update the state
            update_state = messagebox.askyesno("Update State?", 
                                              f"Do you want to update the state from '{old_state}' to '{new_default_state}'?\n\n"
                                              f"(Click 'No' to keep the current state: '{old_state}')")
            
            if update_state:
                item['state'] = new_default_state
            
            # Move the activity
            self.activities[category].remove(item)
            self.activities[target_category].append(item)
            self.save_data()
            
            move_window.destroy()
            messagebox.showinfo("Success", 
                              f"Moved '{activity_name}' from '{category}' to '{target_category}'!")
            self.status_bar.config(text=f"Moved: {activity_name} → {target_category} 📦")
        
        tk.Button(move_window, text="Move Activity", command=do_move,
                 bg="#009688", fg="white", padx=20, pady=5).pack(pady=10)
    
    def _filter_saga_prerequisites(self, activities, category):
        """Filter out saga items where previous items haven't been completed"""
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
    
    def manage_saga(self):
        """Manage saga information for activities"""
        category = self.category_var.get()
        
        if not category:
            messagebox.showwarning("No Category", "Please select a category first!")
            return
        
        if not self.activities[category]:
            messagebox.showinfo("Empty", f"No activities in '{category}'!")
            return
        
        # Create saga management window
        saga_window = tk.Toplevel(self.root)
        saga_window.title("Manage Sagas")
        saga_window.geometry("700x550")
        
        tk.Label(saga_window, text=f"Manage Sagas in '{category}':",
                font=("Arial", 11, "bold")).pack(pady=10)
        
        tk.Label(saga_window, text="Select an activity to set/edit saga info:",
                font=("Arial", 9)).pack(pady=5)
        
        # Listbox with scrollbar
        list_frame = tk.Frame(saga_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(list_frame, font=("Arial", 10), width=70, 
                            yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Populate listbox
        for item in self.activities[category]:
            saga = item.get("saga", None)
            order = item.get("order", None)
            if saga and order:
                display_text = f"{item['name']} - [{item['state']}] - SAGA: {saga} #{order}"
            else:
                display_text = f"{item['name']} - [{item['state']}] - No saga"
            listbox.insert(tk.END, display_text)
        
        # Input frame
        input_frame = tk.Frame(saga_window)
        input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(input_frame, text="Saga Name:", font=("Arial", 9)).grid(row=0, column=0, padx=5, sticky=tk.W)
        
        # Get existing sagas
        existing_sagas = set()
        for item in self.activities[category]:
            saga = item.get("saga")
            if saga:
                existing_sagas.add(saga)
        existing_sagas_list = sorted(list(existing_sagas))
        
        # Use combobox for saga name to allow selection of existing sagas
        saga_var = tk.StringVar()
        saga_combo = ttk.Combobox(input_frame, textvariable=saga_var,
                                 font=("Arial", 10), width=28)
        saga_combo['values'] = existing_sagas_list
        saga_combo.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="Order #:", font=("Arial", 9)).grid(row=0, column=2, padx=5, sticky=tk.W)
        order_entry = tk.Entry(input_frame, font=("Arial", 10), width=10)
        order_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(input_frame, text="(Type new saga name or select existing. Leave blank to remove)", 
                font=("Arial", 8), fg="#666").grid(row=1, column=0, columnspan=4, pady=5)
        
        def set_saga():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select an activity!")
                return
            
            idx = selection[0]
            item = self.activities[category][idx]
            
            saga_name = saga_var.get().strip()
            order_str = order_entry.get().strip()
            
            # If both are empty, remove saga
            if not saga_name and not order_str:
                item["saga"] = None
                item["order"] = None
                self.save_data()
                messagebox.showinfo("Success", f"Removed saga info from '{item['name']}'!")
                self.status_bar.config(text=f"Saga removed from: {item['name']} 🎬")
                saga_window.destroy()
                return
            
            # Validate inputs
            if not saga_name:
                messagebox.showwarning("Invalid Input", "Please enter a saga name!")
                return
            
            if not order_str:
                messagebox.showwarning("Invalid Input", "Please enter an order number!")
                return
            
            try:
                order_num = int(order_str)
                if order_num < 1:
                    raise ValueError()
            except ValueError:
                messagebox.showwarning("Invalid Input", "Order must be a positive number!")
                return
            
            # Check if this order number already exists in the same saga
            for other_item in self.activities[category]:
                if other_item != item and other_item.get("saga") == saga_name and other_item.get("order") == order_num:
                    overwrite = messagebox.askyesno("Duplicate Order", 
                                                   f"Order #{order_num} already exists in '{saga_name}' saga "
                                                   f"for '{other_item['name']}'.\n\n"
                                                   f"Do you want to continue anyway?",
                                                   icon='warning')
                    if not overwrite:
                        return
            
            # Set saga info
            item["saga"] = saga_name
            item["order"] = order_num
            self.save_data()
            
            messagebox.showinfo("Success", 
                              f"Set '{item['name']}' as part of '{saga_name}' saga (#{order_num})!")
            self.status_bar.config(text=f"Saga set: {saga_name} #{order_num} 🎬")
            saga_window.destroy()
        
        def on_select(event):
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                item = self.activities[category][idx]
                saga = item.get("saga", "")
                order = item.get("order", "")
                
                # Only update if fields are empty (first selection)
                # This prevents clearing when user clicks combobox/entry
                current_saga = saga_var.get()
                current_order = order_entry.get()
                
                # Update saga if it's empty or different from current item
                if not current_saga or (saga and current_saga != saga):
                    saga_var.set(saga if saga else "")
                
                # Update order if it's empty or different from current item  
                if not current_order or (order and current_order != str(order)):
                    order_entry.delete(0, tk.END)
                    if order:
                        order_entry.insert(0, str(order))
        
        listbox.bind('<<ListboxSelect>>', on_select)
        
        # Buttons
        btn_frame = tk.Frame(saga_window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Set Saga Info", command=set_saga,
                 bg="#FF5722", fg="white", padx=20, pady=5,
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="View Sagas in Category", 
                 command=lambda: self._view_sagas(category),
                 bg="#3F51B5", fg="white", padx=20, pady=5,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    def _view_sagas(self, category):
        """View all sagas in a category organized by saga name"""
        view_window = tk.Toplevel(self.root)
        view_window.title(f"Sagas in {category}")
        view_window.geometry("600x450")
        
        text_widget = tk.Text(view_window, font=("Arial", 10), wrap=tk.WORD)
        scrollbar = tk.Scrollbar(view_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Group activities by saga
        sagas = {}
        no_saga = []
        
        for item in self.activities[category]:
            saga = item.get("saga")
            if saga:
                if saga not in sagas:
                    sagas[saga] = []
                sagas[saga].append(item)
            else:
                no_saga.append(item)
        
        # Display sagas
        if sagas:
            text_widget.insert(tk.END, "🎬 SAGAS\n\n", "title")
            for saga_name in sorted(sagas.keys()):
                text_widget.insert(tk.END, f"📚 {saga_name}\n", "saga")
                # Sort by order
                sorted_items = sorted(sagas[saga_name], key=lambda x: x.get("order", 0))
                for item in sorted_items:
                    order = item.get("order", "?")
                    state = item["state"]
                    name = item["name"]
                    
                    if state in ["Seen", "Played", "Done"]:
                        text_widget.insert(tk.END, f"  {order}. ✓ {name} ", "done")
                        text_widget.insert(tk.END, f"[{state}]\n", "done_state")
                    else:
                        text_widget.insert(tk.END, f"  {order}. {name} ", "pending")
                        text_widget.insert(tk.END, f"[{state}]\n", "pending_state")
                text_widget.insert(tk.END, "\n")
        
        # Display non-saga items
        if no_saga:
            text_widget.insert(tk.END, "📝 STANDALONE ITEMS\n\n", "title")
            for item in no_saga:
                text_widget.insert(tk.END, f"  • {item['name']} [{item['state']}]\n")
        
        text_widget.tag_config("title", font=("Arial", 12, "bold"))
        text_widget.tag_config("saga", font=("Arial", 11, "bold"), foreground="#FF5722")
        text_widget.tag_config("done", foreground="#888888", font=("Arial", 10))
        text_widget.tag_config("done_state", foreground="#888888", font=("Arial", 9, "italic"))
        text_widget.tag_config("pending", foreground="#000000", font=("Arial", 10))
        text_widget.tag_config("pending_state", foreground="#4CAF50", font=("Arial", 9, "bold"))
        text_widget.config(state=tk.DISABLED)
    
    def _get_activity_image(self, activity_name, category):
        """Get or generate an image for the activity"""
        # Create a safe filename
        safe_name = "".join(c for c in activity_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        cache_file = self.image_cache_dir / f"{safe_name}.png"
        
        # Check cache first
        if cache_file.exists():
            try:
                img = Image.open(cache_file)
                img = img.resize((500, 500), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading cached image: {e}")
        
        # Generate new image
        if not self.config.get("openai_api_key"):
            return None
        
        try:
            # Show generating message
            self.result_label.config(text="🎨 Generating AI image...\nThis may take a few seconds", 
                                   bg="#9C27B0", fg="white")
            self.root.update()
            
            # Generate image using OpenAI DALL-E
            image_url = self._generate_dalle_image(activity_name, category)
            
            if image_url:
                # Download and cache the image
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                
                # Save to cache
                img.save(cache_file, 'PNG')
                
                # Resize and return
                img = img.resize((500, 500), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
        
        except Exception as e:
            print(f"Error generating image: {e}")
            messagebox.showwarning("Image Generation Failed", 
                                 f"Could not generate image: {str(e)}\n\nContinuing without image.")
        
        return None
    
    def _generate_dalle_image(self, activity_name, category):
        """Generate image using OpenAI DALL-E API with plot/description context"""
        try:
            import openai
        except ImportError:
            messagebox.showerror("Missing Package", 
                               "Please install OpenAI package:\npip install openai")
            return None
        
        api_key = self.config.get("openai_api_key")
        if not api_key:
            return None
        
        try:
            client = openai.OpenAI(api_key=api_key)
            
            # Step 1: Get plot/description from ChatGPT
            plot_prompt = f"In 2-3 sentences, describe the plot or main theme of: {activity_name}"
            if category.lower() == "videogame":
                plot_prompt = f"In 2-3 sentences, describe the gameplay and setting of the videogame: {activity_name}"
            elif category.lower() == "series":
                plot_prompt = f"In 2-3 sentences, describe the plot and atmosphere of the TV series: {activity_name}"
            elif category.lower() == "movie":
                plot_prompt = f"In 2-3 sentences, describe the plot and key scenes of the movie: {activity_name}"
            
            # Get description from ChatGPT
            chat_response = client.chat.completions.create(
                model="gpt-4o-mini",  # Cheaper model for descriptions
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides concise, family-friendly, artistic descriptions of movies, games, and TV shows for image generation. Focus on visual elements, settings, and themes. Avoid graphic violence, horror, or mature content descriptions."},
                    {"role": "user", "content": plot_prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            plot_description = chat_response.choices[0].message.content.strip()
            print(f"Generated description: {plot_description}")
            
            # Step 2: Generate image using the plot description with safety-friendly wording
            style = self.config.get("image_style", "vibrant digital art")
            
            # Create a safe, artistic prompt focusing on visual themes rather than explicit content
            if category.lower() == "movie":
                image_prompt = f"A cinematic scene inspired by the film '{activity_name}'. {plot_description}. Artistic style: {style}, movie poster aesthetic, professional illustration, family-friendly"
            elif category.lower() == "series":
                image_prompt = f"A scene from the TV series '{activity_name}'. {plot_description}. Artistic style: {style}, television poster design, professional illustration"
            elif category.lower() == "videogame":
                image_prompt = f"Game artwork for '{activity_name}'. {plot_description}. Artistic style: {style}, video game cover art, professional digital art"
            else:
                image_prompt = f"Artistic representation of '{activity_name}'. {plot_description}. Style: {style}, professional illustration"
            
            print(f"Image prompt: {image_prompt}")
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            return response.data[0].url
        
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def open_settings(self):
        """Open settings dialog for API configuration"""
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
        
        api_key_var = tk.StringVar(value=self.config.get("openai_api_key", ""))
        api_entry = tk.Entry(api_frame, textvariable=api_key_var, font=("Arial", 10), 
                            width=50, show="*")
        api_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(api_frame, text="Get your API key at: https://platform.openai.com/api-keys", 
                font=("Arial", 8), fg="#666").grid(row=1, column=0, columnspan=2, pady=5)
        
        # Image settings
        img_frame = tk.LabelFrame(settings_window, text="Image Settings", 
                                 font=("Arial", 11, "bold"), padx=15, pady=15)
        img_frame.pack(fill=tk.X, padx=20, pady=10)
        
        enable_var = tk.BooleanVar(value=self.config.get("enable_images", True))
        tk.Checkbutton(img_frame, text="✅ Enable AI Image Generation", 
                      variable=enable_var, font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(5, 15))
        
        tk.Label(img_frame, text="Image Style:", font=("Arial", 10, "bold")).grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        # Radio buttons for style selection
        style_var = tk.StringVar(value=self.config.get("image_style", "vibrant digital art"))
        
        styles = [
            ("🎨 Vibrant Digital Art (Default)", "vibrant digital art"),
            ("📸 Realistic Photo", "realistic photo"),
            ("🎭 Cartoon Style", "cartoon style")
        ]
        
        for i, (label, value) in enumerate(styles):
            rb = tk.Radiobutton(img_frame, text=label, variable=style_var, 
                               value=value, font=("Arial", 10))
            rb.grid(row=i+2, column=0, sticky=tk.W, pady=2, padx=20)
        
        # Info
        info_frame = tk.Frame(settings_window, bg="#E3F2FD", padx=10, pady=10)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        info_text = ("💡 Images are cached locally to save API costs.\n"
                    "Cost: ~$0.04 per image (only generated once per activity)")
        tk.Label(info_frame, text=info_text, font=("Arial", 9), 
                bg="#E3F2FD", fg="#1976D2", justify=tk.LEFT).pack()
        
        def save_settings():
            self.config["openai_api_key"] = api_key_var.get().strip()
            self.config["enable_images"] = enable_var.get()
            self.config["image_style"] = style_var.get()
            self.save_config()
            messagebox.showinfo("Success", "Settings saved!")
            settings_window.destroy()
        
        def clear_cache():
            confirm = messagebox.askyesno("Clear Cache", 
                                         "Delete all cached images?\n\nThey will be regenerated next time.")
            if confirm:
                count = 0
                for file in self.image_cache_dir.glob("*.png"):
                    file.unlink()
                    count += 1
                messagebox.showinfo("Cache Cleared", f"Deleted {count} cached images.")
        
        # Buttons
        btn_frame = tk.Frame(settings_window)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="💾 Save Settings", command=save_settings,
                 bg="#4CAF50", fg="white", padx=20, pady=8,
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Clear Image Cache", command=clear_cache,
                 bg="#FF9800", fg="white", padx=20, pady=8,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Cancel", command=settings_window.destroy,
                 bg="#757575", fg="white", padx=20, pady=8,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

def main():
    root = tk.Tk()
    app = ActivitySelector(root)
    root.mainloop()

if __name__ == "__main__":
    main()
