# app/views/room_management.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.models.room import Room
from app.utils.style import center_window


class RoomManagementWindow:
    def __init__(self, master):
        self.master = master
        master.title("Room Management")
        center_window(master, 900, 600)
        
        # Top frame for buttons
        top_frame = tk.Frame(master)
        top_frame.pack(pady=10)
        
        tk.Button(top_frame, text="Add Room", command=self.add_room, width=15, bg='green', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Edit Room", command=self.edit_room, width=15, bg='blue', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Delete Room", command=self.delete_room, width=15, bg='red', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Refresh", command=self.load_rooms, width=15).pack(side=tk.LEFT, padx=5)
        
        # Treeview for displaying rooms
        tree_frame = tk.Frame(master)
        tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Room Number', 'Type', 'Price', 'Status', 'Description'), 
                                  show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Room Number', text='Room Number')
        self.tree.heading('Type', text='Room Type')
        self.tree.heading('Price', text='Price ($)')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Description', text='Description')
        
        self.tree.column('ID', width=50)
        self.tree.column('Room Number', width=100)
        self.tree.column('Type', width=120)
        self.tree.column('Price', width=100)
        self.tree.column('Status', width=100)
        self.tree.column('Description', width=300)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Load rooms
        self.load_rooms()
        
        # Back button
        tk.Button(master, text="Back to Dashboard", command=master.destroy, width=20).pack(pady=10)
    
    def load_rooms(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load rooms from database
        try:
            rooms = Room.get_all()
            for room in rooms:
                self.tree.insert('', tk.END, values=(
                    room.id,
                    room.room_number,
                    room.room_type,
                    f"{room.price:.2f}",
                    room.status,
                    room.description or ''
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load rooms: {str(e)}")
    
    def add_room(self):
        AddEditRoomDialog(self.master, self, mode='add')
    
    def edit_room(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a room to edit")
            return
        
        item = self.tree.item(selected[0])
        room_id = item['values'][0]
        room = Room.get_by_id(room_id)
        
        if room:
            AddEditRoomDialog(self.master, self, mode='edit', room=room)
    
    def delete_room(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a room to delete")
            return
        
        item = self.tree.item(selected[0])
        room_id = item['values'][0]
        room_number = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Room {room_number}?"):
            try:
                Room.delete(room_id)
                messagebox.showinfo("Success", "Room deleted successfully")
                self.load_rooms()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete room: {str(e)}")


class AddEditRoomDialog:
    def __init__(self, parent, room_window, mode='add', room=None):
        self.room_window = room_window
        self.mode = mode
        self.room = room
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Room" if mode == 'add' else "Edit Room")
        center_window(self.dialog, 400, 350)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Room Number
        tk.Label(self.dialog, text="Room Number:").pack(pady=(20, 5))
        self.room_number_entry = tk.Entry(self.dialog, width=30)
        self.room_number_entry.pack()
        
        # Room Type
        tk.Label(self.dialog, text="Room Type:").pack(pady=(10, 5))
        self.room_type_var = tk.StringVar(value='Single')
        room_type_frame = tk.Frame(self.dialog)
        room_type_frame.pack()
        ttk.Combobox(room_type_frame, textvariable=self.room_type_var, width=28,
                     values=['Single', 'Double', 'Suite', 'Deluxe', 'Presidential'], state='readonly').pack()
        
        # Price
        tk.Label(self.dialog, text="Price per Night ($):").pack(pady=(10, 5))
        self.price_entry = tk.Entry(self.dialog, width=30)
        self.price_entry.pack()
        
        # Status
        tk.Label(self.dialog, text="Status:").pack(pady=(10, 5))
        self.status_var = tk.StringVar(value='Available')
        status_frame = tk.Frame(self.dialog)
        status_frame.pack()
        ttk.Combobox(status_frame, textvariable=self.status_var, width=28,
                     values=['Available', 'Occupied', 'Maintenance', 'Reserved'], state='readonly').pack()
        
        # Description
        tk.Label(self.dialog, text="Description:").pack(pady=(10, 5))
        self.description_entry = tk.Entry(self.dialog, width=30)
        self.description_entry.pack()
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Save", command=self.save, width=12, bg='green', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.dialog.destroy, width=12).pack(side=tk.LEFT, padx=5)
        
        # Load data if editing
        if mode == 'edit' and room:
            self.room_number_entry.insert(0, room.room_number)
            self.room_type_var.set(room.room_type)
            self.price_entry.insert(0, str(room.price))
            self.status_var.set(room.status)
            if room.description:
                self.description_entry.insert(0, room.description)
    
    def save(self):
        room_number = self.room_number_entry.get().strip()
        room_type = self.room_type_var.get()
        price = self.price_entry.get().strip()
        status = self.status_var.get()
        description = self.description_entry.get().strip()
        
        if not room_number or not price:
            messagebox.showwarning("Warning", "Room number and price are required")
            return
        
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price")
            return
        
        try:
            if self.mode == 'add':
                Room.create(room_number, room_type, price, status, description)
                messagebox.showinfo("Success", "Room added successfully")
            else:
                Room.update(self.room.id, room_number=room_number, room_type=room_type, 
                          price=price, status=status, description=description)
                messagebox.showinfo("Success", "Room updated successfully")
            
            self.room_window.load_rooms()
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save room: {str(e)}")
