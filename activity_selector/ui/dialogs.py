"""
Dialog helper functions for Activity Selector.
Contains all dialog windows for managing activities and categories.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class ActivityDialogs:
    """Helper class for activity management dialogs."""
    
    @staticmethod
    def add_activity(parent, category, data_manager, status_bar_callback=None):
        """Show dialog to add a new activity."""
        activities = data_manager.get_activities(category)
        
        # Create add activity window
        add_window = tk.Toplevel(parent)
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
        for item in activities:
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
            existing_names = [item["name"] for item in activities]
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
                for item in activities:
                    if item.get("saga") == saga and item.get("order") == order:
                        messagebox.showwarning("Duplicate Order", 
                                             f"Order #{order} already exists in '{saga}' saga!")
                        return
            
            # Create new item
            default_state = data_manager._get_default_state(category)
            new_item = {"name": activity_name, "state": default_state, "saga": saga, "order": order}
            
            # Add next_episode field for series
            if category.lower() == "series":
                new_item["next_episode"] = None
            
            data_manager.add_activity(category, new_item)
            
            saga_info = f" (Saga: {saga} #{order})" if saga else ""
            messagebox.showinfo("Success", f"Added '{activity_name}'{saga_info} to {category}!")
            if status_bar_callback:
                status_bar_callback(f"Added: {activity_name} ✅")
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
        
        # Bind Enter key
        name_entry.bind('<Return>', lambda e: do_add())
    
    @staticmethod
    def edit_activity(parent, category, data_manager, status_bar_callback=None):
        """Show dialog to edit an activity."""
        activities = data_manager.get_activities(category)
        
        if not activities:
            messagebox.showinfo("Empty", f"No activities in '{category}' to edit!")
            return
        
        # Create selection window
        edit_window = tk.Toplevel(parent)
        edit_window.title("Edit Activity")
        edit_window.geometry("600x400")
        
        tk.Label(edit_window, text=f"Select activity to edit in '{category}':",
                font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(edit_window, font=("Arial", 10), width=60)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def refresh_listbox():
            """Refresh the listbox with current data."""
            listbox.delete(0, tk.END)
            activities = data_manager.get_activities(category)
            for item in activities:
                display_text = f"{item['name']} [{item['state']}]"
                listbox.insert(tk.END, display_text)
        
        refresh_listbox()
        
        def do_edit():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select an activity to edit!")
                return
            
            idx = selection[0]
            activities = data_manager.get_activities(category)
            item = activities[idx]
            old_name = item['name']
            
            new_name = simpledialog.askstring("Edit Activity", 
                                             f"Edit activity name:",
                                             initialvalue=old_name)
            
            if new_name and new_name.strip():
                new_name = new_name.strip()
                # Check if new name already exists (excluding current item)
                existing_names = [i["name"] for i in activities if i != item]
                if new_name not in existing_names:
                    data_manager.update_activity(category, old_name, {"name": new_name})
                    messagebox.showinfo("Success", f"Renamed '{old_name}' to '{new_name}'!")
                    if status_bar_callback:
                        status_bar_callback(f"Updated: {new_name} ✏️")
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
    
    @staticmethod
    def remove_activity(parent, category, data_manager, status_bar_callback=None):
        """Show dialog to remove an activity."""
        activities = data_manager.get_activities(category)
        
        if not activities:
            messagebox.showinfo("Empty", f"No activities in '{category}' to remove!")
            return
        
        # Create selection window
        select_window = tk.Toplevel(parent)
        select_window.title("Remove Activity")
        select_window.geometry("500x350")
        
        tk.Label(select_window, text=f"Select activity to remove from '{category}':",
                font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(select_window, font=("Arial", 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for item in activities:
            display_text = f"{item['name']} [{item['state']}]"
            listbox.insert(tk.END, display_text)
        
        def do_remove():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                activities = data_manager.get_activities(category)
                item = activities[idx]
                activity_name = item['name']
                data_manager.remove_activity(category, activity_name)
                select_window.destroy()
                messagebox.showinfo("Success", f"Removed '{activity_name}'!")
                if status_bar_callback:
                    status_bar_callback(f"Removed: {activity_name} 🗑️")
        
        tk.Button(select_window, text="Remove Selected", command=do_remove,
                 bg="#f44336", fg="white", padx=20, pady=5).pack(pady=10)
    
    @staticmethod
    def change_state(parent, category, data_manager, status_bar_callback=None):
        """Show dialog to change activity state."""
        activities = data_manager.get_activities(category)
        
        if not activities:
            messagebox.showinfo("Empty", f"No activities in '{category}'!")
            return
        
        # Create selection window
        state_window = tk.Toplevel(parent)
        state_window.title("Change Activity State")
        state_window.geometry("600x450")
        
        tk.Label(state_window, text=f"Select activity to change state in '{category}':",
                font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(state_window, font=("Arial", 10), width=60)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def refresh_listbox():
            """Refresh the listbox with current data."""
            listbox.delete(0, tk.END)
            activities = data_manager.get_activities(category)
            for item in activities:
                display_text = f"{item['name']} - [{item['state']}]"
                listbox.insert(tk.END, display_text)
        
        refresh_listbox()
        
        # State selection frame
        state_frame = tk.Frame(state_window)
        state_frame.pack(pady=10)
        
        tk.Label(state_frame, text="New State:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        state_var = tk.StringVar()
        states = data_manager.get_states_for_category(category)
        
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
            activities = data_manager.get_activities(category)
            item = activities[idx]
            old_state = item['state']
            
            data_manager.update_activity(category, item['name'], {"state": new_state})
            messagebox.showinfo("Success", 
                              f"Changed '{item['name']}' from '{old_state}' to '{new_state}'!")
            if status_bar_callback:
                status_bar_callback(f"Updated: {item['name']} -> {new_state} ✏️")
            refresh_listbox()
        
        btn_frame = tk.Frame(state_window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Update State", command=do_change,
                 bg="#00BCD4", fg="white", padx=20, pady=5,
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Close", command=state_window.destroy,
                 bg="#757575", fg="white", padx=20, pady=5,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    @staticmethod
    def move_activity(parent, category, data_manager, status_bar_callback=None):
        """Show dialog to move activity to another category."""
        activities = data_manager.get_activities(category)
        
        if not activities:
            messagebox.showinfo("Empty", f"No activities in '{category}' to move!")
            return
        
        if len(data_manager.get_categories()) < 2:
            messagebox.showinfo("Need More Categories", 
                              "You need at least 2 categories to move activities between them!\n"
                              "Create a new category first.")
            return
        
        # Create selection window
        move_window = tk.Toplevel(parent)
        move_window.title("Move Activity to Another Category")
        move_window.geometry("600x500")
        
        tk.Label(move_window, text=f"Select activity to move from '{category}':",
                font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(move_window, font=("Arial", 10), width=60)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for item in activities:
            display_text = f"{item['name']} [{item['state']}]"
            listbox.insert(tk.END, display_text)
        
        # Category selection frame
        cat_frame = tk.Frame(move_window)
        cat_frame.pack(pady=10)
        
        tk.Label(cat_frame, text="Move to Category:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        target_cat_var = tk.StringVar()
        
        # Get other categories (exclude current)
        other_categories = [cat for cat in data_manager.get_categories() if cat != category]
        
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
            activities = data_manager.get_activities(category)
            item = activities[idx]
            activity_name = item['name']
            
            # Check if activity with same name already exists in target category
            target_activities = data_manager.get_activities(target_category)
            existing_names = [i["name"] for i in target_activities]
            if activity_name in existing_names:
                messagebox.showwarning("Duplicate", 
                                      f"An activity named '{activity_name}' already exists in '{target_category}'!\n"
                                      "Rename it first, then try moving.")
                return
            
            # Update state to match new category's default if needed
            old_state = item['state']
            new_default_state = data_manager._get_default_state(target_category)
            
            # Ask if user wants to update the state
            update_state = messagebox.askyesno("Update State?", 
                                              f"Do you want to update the state from '{old_state}' to '{new_default_state}'?\n\n"
                                              f"(Click 'No' to keep the current state: '{old_state}')")
            
            # Move the activity
            if data_manager.move_activity(category, target_category, activity_name):
                if update_state:
                    data_manager.update_activity(target_category, activity_name, {"state": new_default_state})
                
                move_window.destroy()
                messagebox.showinfo("Success", 
                                  f"Moved '{activity_name}' from '{category}' to '{target_category}'!")
                if status_bar_callback:
                    status_bar_callback(f"Moved: {activity_name} → {target_category} 📦")
        
        tk.Button(move_window, text="Move Activity", command=do_move,
                 bg="#009688", fg="white", padx=20, pady=5).pack(pady=10)


class CategoryDialogs:
    """Helper class for category management dialogs."""
    
    @staticmethod
    def edit_category(parent, data_manager, category_update_callback=None, status_bar_callback=None):
        """Show dialog to rename a category."""
        if not data_manager.get_categories():
            messagebox.showinfo("No Categories", "No categories to edit!")
            return
        
        # Create selection window
        edit_window = tk.Toplevel(parent)
        edit_window.title("Rename Category")
        edit_window.geometry("400x350")
        
        tk.Label(edit_window, text="Select category to rename:",
                font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(edit_window, font=("Arial", 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        categories = data_manager.get_categories()
        for cat in categories:
            count = len(data_manager.get_activities(cat))
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
                    if new_category != old_category and new_category not in data_manager.get_categories():
                        if data_manager.rename_category(old_category, new_category):
                            if category_update_callback:
                                category_update_callback(new_category)
                            edit_window.destroy()
                            messagebox.showinfo("Success", f"Renamed '{old_category}' to '{new_category}'!")
                            if status_bar_callback:
                                status_bar_callback(f"Renamed category to: {new_category} ✏️")
                    elif new_category == old_category:
                        messagebox.showinfo("No Change", "Category name is the same!")
                    else:
                        messagebox.showwarning("Duplicate", "A category with this name already exists!")
        
        tk.Button(edit_window, text="Rename Selected", command=do_rename,
                 bg="#673AB7", fg="white", padx=20, pady=5).pack(pady=10)
    
    @staticmethod
    def delete_category(parent, data_manager, category_update_callback=None, status_bar_callback=None):
        """Show dialog to delete a category."""
        if not data_manager.get_categories():
            messagebox.showinfo("No Categories", "No categories to delete!")
            return
        
        # Create selection window
        delete_window = tk.Toplevel(parent)
        delete_window.title("Delete Category")
        delete_window.geometry("400x350")
        
        tk.Label(delete_window, text="⚠️ Select category to DELETE (cannot be undone):",
                font=("Arial", 10, "bold"), fg="#f44336").pack(pady=10)
        
        listbox = tk.Listbox(delete_window, font=("Arial", 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        categories = data_manager.get_categories()
        for cat in categories:
            count = len(data_manager.get_activities(cat))
            listbox.insert(tk.END, f"{cat} ({count} activities)")
        
        def do_delete():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                category_to_delete = categories[idx]
                count = len(data_manager.get_activities(category_to_delete))
                
                # Confirm deletion
                confirm = messagebox.askyesno("Confirm Deletion", 
                                             f"Are you sure you want to delete '{category_to_delete}' "
                                             f"and all {count} activities?\n\nThis cannot be undone!",
                                             icon='warning')
                
                if confirm:
                    if data_manager.delete_category(category_to_delete):
                        if category_update_callback:
                            category_update_callback()
                        delete_window.destroy()
                        messagebox.showinfo("Deleted", f"Category '{category_to_delete}' has been deleted.")
                        if status_bar_callback:
                            status_bar_callback(f"Deleted category: {category_to_delete} 🗑️")
        
        tk.Button(delete_window, text="Delete Selected", command=do_delete,
                 bg="#E91E63", fg="white", padx=20, pady=5).pack(pady=10)


class ViewDialogs:
    """Helper class for view dialogs."""
    
    @staticmethod
    def view_all(parent, data_manager):
        """View all categories and activities with their states."""
        view_window = tk.Toplevel(parent)
        view_window.title("All Activities")
        view_window.geometry("600x450")
        
        text_widget = tk.Text(view_window, font=("Arial", 10), wrap=tk.WORD)
        scrollbar = tk.Scrollbar(view_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for category in data_manager.get_categories():
            activities = data_manager.get_activities(category)
            text_widget.insert(tk.END, f"📂 {category.upper()}\n", "category")
            if activities:
                for item in activities:
                    state = item['state']
                    name = item['name']
                    next_ep_info = ""
                    
                    # Add next episode info for series
                    if category.lower() == "series" and item.get("next_episode"):
                        next_ep_info = f" - Next: {item['next_episode']}"
                    
                    if state in ["Seen", "Played"]:
                        text_widget.insert(tk.END, f"  • {name} ", "done_name")
                        text_widget.insert(tk.END, f"[{state}]{next_ep_info}\n", "done_state")
                    else:
                        text_widget.insert(tk.END, f"  • {name} ", "pending_name")
                        text_widget.insert(tk.END, f"[{state}]{next_ep_info}\n", "pending_state")
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


class SagaDialogs:
    """Helper class for saga management dialogs."""
    
    @staticmethod
    def manage_saga(parent, category, data_manager, status_bar_callback=None):
        """Show dialog to manage saga information."""
        activities = data_manager.get_activities(category)
        
        if not activities:
            messagebox.showinfo("Empty", f"No activities in '{category}'!")
            return
        
        # Create saga management window
        saga_window = tk.Toplevel(parent)
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
        for item in activities:
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
        for item in activities:
            saga = item.get("saga")
            if saga:
                existing_sagas.add(saga)
        existing_sagas_list = sorted(list(existing_sagas))
        
        # Use combobox for saga name
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
            activities = data_manager.get_activities(category)
            item = activities[idx]
            
            saga_name = saga_var.get().strip()
            order_str = order_entry.get().strip()
            
            # If both are empty, remove saga
            if not saga_name and not order_str:
                data_manager.update_activity(category, item['name'], {"saga": None, "order": None})
                messagebox.showinfo("Success", f"Removed saga info from '{item['name']}'!")
                if status_bar_callback:
                    status_bar_callback(f"Saga removed from: {item['name']} 🎬")
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
            
            # Check for duplicate order
            for other_item in activities:
                if other_item != item and other_item.get("saga") == saga_name and other_item.get("order") == order_num:
                    overwrite = messagebox.askyesno("Duplicate Order", 
                                                   f"Order #{order_num} already exists in '{saga_name}' saga "
                                                   f"for '{other_item['name']}'.\n\n"
                                                   f"Do you want to continue anyway?",
                                                   icon='warning')
                    if not overwrite:
                        return
            
            # Set saga info
            data_manager.update_activity(category, item['name'], {"saga": saga_name, "order": order_num})
            
            messagebox.showinfo("Success", 
                              f"Set '{item['name']}' as part of '{saga_name}' saga (#{order_num})!")
            if status_bar_callback:
                status_bar_callback(f"Saga set: {saga_name} #{order_num} 🎬")
            saga_window.destroy()
        
        def on_select(event):
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                activities = data_manager.get_activities(category)
                item = activities[idx]
                saga = item.get("saga", "")
                order = item.get("order", "")
                
                current_saga = saga_var.get()
                current_order = order_entry.get()
                
                if not current_saga or (saga and current_saga != saga):
                    saga_var.set(saga if saga else "")
                
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
                 command=lambda: SagaDialogs.view_sagas(parent, category, data_manager),
                 bg="#3F51B5", fg="white", padx=20, pady=5,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    @staticmethod
    def view_sagas(parent, category, data_manager):
        """View all sagas in a category organized by saga name."""
        view_window = tk.Toplevel(parent)
        view_window.title(f"Sagas in {category}")
        view_window.geometry("600x450")
        
        text_widget = tk.Text(view_window, font=("Arial", 10), wrap=tk.WORD)
        scrollbar = tk.Scrollbar(view_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Group activities by saga
        activities = data_manager.get_activities(category)
        sagas = {}
        no_saga = []
        
        for item in activities:
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


class EpisodeDialogs:
    """Helper class for episode management dialogs."""
    
    @staticmethod
    def set_next_episode(parent, category, data_manager, status_bar_callback=None):
        """Show dialog to set next episode for a series."""
        if category.lower() != "series":
            messagebox.showinfo("Not a Series", 
                              "This feature is only available for the 'series' category!\n"
                              "Current category: " + category)
            return
        
        activities = data_manager.get_activities(category)
        if not activities:
            messagebox.showinfo("Empty", f"No series in '{category}'!")
            return
        
        # Create episode management window
        episode_window = tk.Toplevel(parent)
        episode_window.title("Set Next Episode")
        episode_window.geometry("650x500")
        
        tk.Label(episode_window, text="Set Next Episode to Watch:",
                font=("Arial", 11, "bold")).pack(pady=10)
        
        tk.Label(episode_window, text="Select a series:",
                font=("Arial", 9)).pack(pady=5)
        
        # Listbox with scrollbar
        list_frame = tk.Frame(episode_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(list_frame, font=("Arial", 10), width=70, 
                            yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Populate listbox
        for item in activities:
            next_ep = item.get("next_episode", None)
            if next_ep:
                display_text = f"{item['name']} - [{item['state']}] - Next: {next_ep}"
            else:
                display_text = f"{item['name']} - [{item['state']}] - No episode set"
            listbox.insert(tk.END, display_text)
        
        # Input frame
        input_frame = tk.Frame(episode_window)
        input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(input_frame, text="Next Episode (e.g., 'S01E05', 'Episode 12', 'Chapter 3'):", 
                font=("Arial", 9)).pack(anchor=tk.W, padx=5)
        
        episode_entry = tk.Entry(input_frame, font=("Arial", 11), width=40)
        episode_entry.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(input_frame, text="💡 Tip: Leave empty to clear the next episode", 
                font=("Arial", 8), fg="#666").pack(pady=5)
        
        def set_episode():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a series!")
                return
            
            idx = selection[0]
            activities = data_manager.get_activities(category)
            item = activities[idx]
            
            next_episode = episode_entry.get().strip()
            
            # If empty, remove next episode
            if not next_episode:
                data_manager.update_activity(category, item['name'], {"next_episode": None})
                messagebox.showinfo("Success", f"Cleared next episode for '{item['name']}'!")
                if status_bar_callback:
                    status_bar_callback(f"Next episode cleared: {item['name']} 📺")
                episode_window.destroy()
                return
            
            # Set next episode
            data_manager.update_activity(category, item['name'], {"next_episode": next_episode})
            
            messagebox.showinfo("Success", 
                              f"Set next episode for '{item['name']}' to '{next_episode}'!")
            if status_bar_callback:
                status_bar_callback(f"Next episode set: {next_episode} 📺")
            episode_window.destroy()
        
        def on_select(event):
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                activities = data_manager.get_activities(category)
                item = activities[idx]
                next_ep = item.get("next_episode", "")
                
                # Update entry with current value
                episode_entry.delete(0, tk.END)
                if next_ep:
                    episode_entry.insert(0, next_ep)
        
        listbox.bind('<<ListboxSelect>>', on_select)
        
        # Buttons
        btn_frame = tk.Frame(episode_window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="💾 Set Next Episode", command=set_episode,
                 bg="#9C27B0", fg="white", padx=20, pady=5,
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Close", command=episode_window.destroy,
                 bg="#757575", fg="white", padx=20, pady=5,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        episode_entry.bind('<Return>', lambda e: set_episode())
