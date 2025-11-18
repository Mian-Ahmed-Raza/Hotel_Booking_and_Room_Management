# app/views/booking_management.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from app.models.booking import Booking
from app.models.room import Room
from app.utils.style import center_window, make_button, make_header, apply_theme


class BookingManagementWindow:
    def __init__(self, master):
        self.master = master
        master.title("Booking Management")
        center_window(master, 1000, 600)
        apply_theme(master)
        header = make_header(master, "Booking Management")
        header.pack(pady=(12, 6))
        
        # Top frame for buttons
        top_frame = tk.Frame(master, bg=master['bg'])
        top_frame.pack(pady=10)
        
        make_button(top_frame, "New Booking", command=self.new_booking, color='#27ae60', width=14).pack(side=tk.LEFT, padx=6)
        make_button(top_frame, "View Details", command=self.view_booking, color='#3498db', width=14).pack(side=tk.LEFT, padx=6)
        make_button(top_frame, "Cancel Booking", command=self.cancel_booking, color='#e74c3c', width=14).pack(side=tk.LEFT, padx=6)
        make_button(top_frame, "Refresh", command=self.load_bookings, width=12).pack(side=tk.LEFT, padx=6)
        
        # Treeview for displaying bookings
        tree_frame = tk.Frame(master)
        tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Guest', 'Phone', 'Room', 'Check-in', 'Check-out', 'Price', 'Status'), 
                                  show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Guest', text='Guest Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Room', text='Room')
        self.tree.heading('Check-in', text='Check-in')
        self.tree.heading('Check-out', text='Check-out')
        self.tree.heading('Price', text='Total Price')
        self.tree.heading('Status', text='Status')
        
        self.tree.column('ID', width=50)
        self.tree.column('Guest', width=150)
        self.tree.column('Phone', width=120)
        self.tree.column('Room', width=80)
        self.tree.column('Check-in', width=100)
        self.tree.column('Check-out', width=100)
        self.tree.column('Price', width=100)
        self.tree.column('Status', width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Load bookings
        self.load_bookings()
        
        # Back button
        make_button(master, "Back to Dashboard", command=master.destroy, width=20, color='#95a5a6').pack(pady=10)
    
    def load_bookings(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load bookings from database
        try:
            bookings = Booking.get_all()
            for booking in bookings:
                room = Room.get_by_id(booking.room_id)
                room_number = room.room_number if room else 'N/A'
                
                self.tree.insert('', tk.END, values=(
                    booking.id,
                    booking.guest_name,
                    booking.guest_phone,
                    room_number,
                    booking.check_in,
                    booking.check_out,
                    f"${booking.total_price:.2f}",
                    booking.status
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bookings: {str(e)}")
    
    def new_booking(self):
        NewBookingDialog(self.master, self)
    
    def view_booking(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to view")
            return
        
        item = self.tree.item(selected[0])
        booking_id = item['values'][0]
        booking = Booking.get_by_id(booking_id)
        
        if booking:
            ViewBookingDialog(self.master, booking)
    
    def cancel_booking(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to cancel")
            return
        
        item = self.tree.item(selected[0])
        booking_id = item['values'][0]
        guest_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Cancel", f"Are you sure you want to cancel booking for {guest_name}?"):
            try:
                booking = Booking.get_by_id(booking_id)
                if booking:
                    # Update booking status
                    Booking.update(booking_id, status='Cancelled')
                    # Update room status
                    Room.update(booking.room_id, status='Available')
                    messagebox.showinfo("Success", "Booking cancelled successfully")
                    self.load_bookings()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to cancel booking: {str(e)}")


class NewBookingDialog:
    def __init__(self, parent, booking_window):
        self.booking_window = booking_window
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("New Booking")
        center_window(self.dialog, 450, 450)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Guest Name
        tk.Label(self.dialog, text="Guest Name:").pack(pady=(20, 5))
        self.guest_name_entry = tk.Entry(self.dialog, width=35)
        self.guest_name_entry.pack()
        
        # Guest Phone
        tk.Label(self.dialog, text="Guest Phone:").pack(pady=(10, 5))
        self.guest_phone_entry = tk.Entry(self.dialog, width=35)
        self.guest_phone_entry.pack()
        
        # Room Selection
        tk.Label(self.dialog, text="Select Room:").pack(pady=(10, 5))
        self.room_var = tk.StringVar()
        self.room_combo = ttk.Combobox(self.dialog, textvariable=self.room_var, width=33, state='readonly')
        self.room_combo.pack()
        self.load_available_rooms()
        
        # Check-in Date
        tk.Label(self.dialog, text="Check-in Date (YYYY-MM-DD):").pack(pady=(10, 5))
        self.checkin_entry = tk.Entry(self.dialog, width=35)
        self.checkin_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.checkin_entry.pack()
        
        # Check-out Date
        tk.Label(self.dialog, text="Check-out Date (YYYY-MM-DD):").pack(pady=(10, 5))
        self.checkout_entry = tk.Entry(self.dialog, width=35)
        self.checkout_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))
        self.checkout_entry.pack()
        
        # Price per night (auto-filled)
        tk.Label(self.dialog, text="Price per Night:").pack(pady=(10, 5))
        self.price_label = tk.Label(self.dialog, text="Select a room", fg='blue')
        self.price_label.pack()
        
        # Total Price (calculated)
        self.total_label = tk.Label(self.dialog, text="Total: $0.00", font=('Arial', 12, 'bold'), fg='green')
        self.total_label.pack(pady=10)
        
        # Bind events
        self.room_combo.bind('<<ComboboxSelected>>', self.calculate_price)
        self.checkin_entry.bind('<KeyRelease>', self.calculate_price)
        self.checkout_entry.bind('<KeyRelease>', self.calculate_price)
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=15)
        make_button(button_frame, "Book Now", command=self.save_booking, color='#27ae60', width=12).pack(side=tk.LEFT, padx=6)
        make_button(button_frame, "Cancel", command=self.dialog.destroy, color='#95a5a6', width=12).pack(side=tk.LEFT, padx=6)
    
    def load_available_rooms(self):
        try:
            rooms = Room.get_available()
            room_list = [f"{room.room_number} - {room.room_type} (${room.price}/night)" for room in rooms]
            self.room_combo['values'] = room_list
            self.rooms = rooms
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load rooms: {str(e)}")
    
    def calculate_price(self, event=None):
        try:
            if not self.room_var.get():
                return
            
            # Get selected room
            room_index = self.room_combo.current()
            if room_index < 0:
                return
            
            room = self.rooms[room_index]
            self.price_label.config(text=f"${room.price:.2f}/night")
            
            # Calculate nights
            checkin = datetime.strptime(self.checkin_entry.get(), '%Y-%m-%d')
            checkout = datetime.strptime(self.checkout_entry.get(), '%Y-%m-%d')
            nights = (checkout - checkin).days
            
            if nights <= 0:
                self.total_label.config(text="Invalid dates", fg='red')
                return
            
            total = room.price * nights
            self.total_label.config(text=f"Total: ${total:.2f} ({nights} nights)", fg='green')
        except:
            self.total_label.config(text="Invalid input", fg='red')
    
    def save_booking(self):
        guest_name = self.guest_name_entry.get().strip()
        guest_phone = self.guest_phone_entry.get().strip()
        
        if not guest_name or not guest_phone or not self.room_var.get():
            messagebox.showwarning("Warning", "Please fill all required fields")
            return
        
        try:
            room_index = self.room_combo.current()
            room = self.rooms[room_index]
            
            checkin = datetime.strptime(self.checkin_entry.get(), '%Y-%m-%d')
            checkout = datetime.strptime(self.checkout_entry.get(), '%Y-%m-%d')
            nights = (checkout - checkin).days
            
            if nights <= 0:
                messagebox.showerror("Error", "Check-out date must be after check-in date")
                return
            
            total_price = room.price * nights
            
            # Create booking
            Booking.create(guest_name, guest_phone, room.id, checkin.date(), checkout.date(), total_price)
            
            # Update room status
            Room.update(room.id, status='Occupied')
            
            messagebox.showinfo("Success", f"Booking created successfully!\nTotal: ${total_price:.2f}")
            self.booking_window.load_bookings()
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create booking: {str(e)}")


class ViewBookingDialog:
    def __init__(self, parent, booking):
        dialog = tk.Toplevel(parent)
        dialog.title(f"Booking Details - #{booking.id}")
        center_window(dialog, 400, 350)
        dialog.transient(parent)
        
        room = Room.get_by_id(booking.room_id)
        
        info_frame = tk.Frame(dialog)
        info_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        details = [
            ("Booking ID:", booking.id),
            ("Guest Name:", booking.guest_name),
            ("Phone:", booking.guest_phone),
            ("Room Number:", room.room_number if room else 'N/A'),
            ("Room Type:", room.room_type if room else 'N/A'),
            ("Check-in:", booking.check_in),
            ("Check-out:", booking.check_out),
            ("Total Price:", f"${booking.total_price:.2f}"),
            ("Status:", booking.status),
            ("Booked On:", booking.created_at)
        ]
        
        for i, (label, value) in enumerate(details):
            tk.Label(info_frame, text=label, font=('Arial', 10, 'bold')).grid(row=i, column=0, sticky='w', pady=5)
            tk.Label(info_frame, text=str(value), font=('Arial', 10)).grid(row=i, column=1, sticky='w', padx=20, pady=5)
        
        make_button(dialog, "Close", command=dialog.destroy, width=15, color='#95a5a6').pack(pady=10)
