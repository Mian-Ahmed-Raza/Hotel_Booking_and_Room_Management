# app/views/billing.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.models.booking import Booking
from app.models.room import Room
from app.utils.style import center_window, apply_theme, make_button, card_frame, make_header, THEME, make_appbar


class BillingWindow:
    def __init__(self, master):
        self.master = master
        master.title("Billing & Invoices")
        center_window(master, 1000, 600)
        apply_theme(master)
        # App bar
        make_appbar(master, title="Billing & Invoices").pack(fill=tk.X)
        make_header(master, "Billing & Invoices").pack(pady=(12, 8))
        # Filter frame
        filter_frame = tk.Frame(master, bg=master['bg'])
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Filter:", style='Muted.TLabel').pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar(value='All')
        ttk.Combobox(filter_frame, textvariable=self.filter_var, width=15,
                     values=['All', 'Completed', 'Checked-in', 'Confirmed'], state='readonly').pack(side=tk.LEFT, padx=5)
        make_button(filter_frame, "Apply Filter", command=self.load_bookings, width=12).pack(side=tk.LEFT, padx=5)
        make_button(filter_frame, "Generate Invoice", command=self.generate_invoice, width=15, color=THEME['primary']).pack(side=tk.LEFT, padx=5)

        # Treeview for displaying bookings (card)
        tree_card = card_frame(master)
        tree_card.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_card.inner)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_card.inner, columns=('ID', 'Guest', 'Room', 'Check-in', 'Check-out', 'Nights', 'Total', 'Status'), 
                                  show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='Invoice #')
        self.tree.heading('Guest', text='Guest Name')
        self.tree.heading('Room', text='Room')
        self.tree.heading('Check-in', text='Check-in')
        self.tree.heading('Check-out', text='Check-out')
        self.tree.heading('Nights', text='Nights')
        self.tree.heading('Total', text='Total Amount')
        self.tree.heading('Status', text='Status')
        
        self.tree.column('ID', width=80)
        self.tree.column('Guest', width=150)
        self.tree.column('Room', width=100)
        self.tree.column('Check-in', width=100)
        self.tree.column('Check-out', width=100)
        self.tree.column('Nights', width=80)
        self.tree.column('Total', width=120)
        self.tree.column('Status', width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Summary card
        summary_card = card_frame(master)
        summary_card.pack(pady=10, padx=10, fill=tk.X)
        ttk.Label(summary_card.inner, text="Summary:", style='Primary.TLabel').pack(side=tk.LEFT, padx=10)
        self.total_bookings_label = ttk.Label(summary_card.inner, text="Total Bookings: 0", style='Muted.TLabel')
        self.total_bookings_label.pack(side=tk.LEFT, padx=20)
        self.total_revenue_label = ttk.Label(summary_card.inner, text="Total Revenue: $0.00", style='Accent.TLabel')
        self.total_revenue_label.pack(side=tk.LEFT, padx=20)
        
        # Load bookings
        self.load_bookings()
        
        # Back button
        make_button(master, "Back to Dashboard", command=master.destroy, width=20, color=THEME['danger']).pack(pady=10)
    
    def load_bookings(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_revenue = 0
        count = 0
        
        # Load bookings from database
        try:
            bookings = Booking.get_all()
            filter_status = self.filter_var.get()
            
            for booking in bookings:
                # Apply filter
                if filter_status != 'All' and booking.status != filter_status:
                    continue
                
                room = Room.get_by_id(booking.room_id)
                room_number = room.room_number if room else 'N/A'
                
                # Calculate nights
                checkin = booking.check_in if isinstance(booking.check_in, datetime.date) else datetime.strptime(str(booking.check_in), '%Y-%m-%d').date()
                checkout = booking.check_out if isinstance(booking.check_out, datetime.date) else datetime.strptime(str(booking.check_out), '%Y-%m-%d').date()
                nights = (checkout - checkin).days
                
                self.tree.insert('', tk.END, values=(
                    f"INV-{booking.id:04d}",
                    booking.guest_name,
                    room_number,
                    booking.check_in,
                    booking.check_out,
                    nights,
                    f"${booking.total_price:.2f}",
                    booking.status
                ))
                
                total_revenue += float(booking.total_price)
                count += 1
            
            # Update summary
            self.total_bookings_label.config(text=f"Total Bookings: {count}")
            self.total_revenue_label.config(text=f"Total Revenue: ${total_revenue:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load billing data: {str(e)}")
    
    def generate_invoice(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to generate invoice")
            return
        
        item = self.tree.item(selected[0])
        invoice_id = item['values'][0]
        booking_id = int(invoice_id.split('-')[1])
        
        booking = Booking.get_by_id(booking_id)
        if booking:
            InvoiceDialog(self.master, booking)


class InvoiceDialog:
    def __init__(self, parent, booking):
        dialog = tk.Toplevel(parent)
        dialog.title(f"Invoice - INV-{booking.id:04d}")
        center_window(dialog, 500, 600)
        dialog.transient(parent)
        apply_theme(dialog)

        # Header
        make_header(dialog, f"Invoice - INV-{booking.id:04d}").pack(pady=(12, 6))

        # Invoice details frame (card)
        details_card = card_frame(dialog)
        details_card.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        
        # Invoice number and date
        tk.Label(details_card.inner, text=f"Invoice #: INV-{booking.id:04d}", 
                font=('Segoe UI', 12, 'bold'), bg=THEME['card_bg'], fg=THEME['text']).pack(anchor='w')
        tk.Label(details_card.inner, text=f"Date: {datetime.now().strftime('%Y-%m-%d')}", 
                font=('Segoe UI', 10), bg=THEME['card_bg'], fg=THEME['muted']).pack(anchor='w', pady=(0, 10))
        
        # Divider
        ttk.Separator(details_card.inner, orient='horizontal').pack(fill='x', pady=10)
        
        # Guest information
        tk.Label(details_card.inner, text="GUEST INFORMATION", 
                font=('Segoe UI', 11, 'bold'), fg=THEME['primary'], bg=THEME['card_bg']).pack(anchor='w', pady=(10, 5))
        tk.Label(details_card.inner, text=f"Name: {booking.guest_name}", 
                font=('Segoe UI', 10), bg=THEME['card_bg'], fg=THEME['text']).pack(anchor='w')
        tk.Label(details_card.inner, text=f"Phone: {booking.guest_phone}", 
                font=('Segoe UI', 10), bg=THEME['card_bg'], fg=THEME['muted']).pack(anchor='w', pady=(0, 10))
        
        # Booking information
        room = Room.get_by_id(booking.room_id)
        
        tk.Label(details_card.inner, text="BOOKING DETAILS", 
                font=('Segoe UI', 11, 'bold'), fg=THEME['primary'], bg=THEME['card_bg']).pack(anchor='w', pady=(10, 5))
        tk.Label(details_card.inner, text=f"Room Number: {room.room_number if room else 'N/A'}", 
                font=('Segoe UI', 10), bg=THEME['card_bg'], fg=THEME['text']).pack(anchor='w')
        tk.Label(details_card.inner, text=f"Room Type: {room.room_type if room else 'N/A'}", 
                font=('Segoe UI', 10), bg=THEME['card_bg'], fg=THEME['text']).pack(anchor='w')
        tk.Label(details_card.inner, text=f"Check-in: {booking.check_in}", 
                font=('Segoe UI', 10), bg=THEME['card_bg'], fg=THEME['muted']).pack(anchor='w')
        tk.Label(details_card.inner, text=f"Check-out: {booking.check_out}", 
                font=('Segoe UI', 10), bg=THEME['card_bg'], fg=THEME['muted']).pack(anchor='w')
        
        # Calculate nights
        checkin = booking.check_in if isinstance(booking.check_in, datetime.date) else datetime.strptime(str(booking.check_in), '%Y-%m-%d').date()
        checkout = booking.check_out if isinstance(booking.check_out, datetime.date) else datetime.strptime(str(booking.check_out), '%Y-%m-%d').date()
        nights = (checkout - checkin).days
        
        tk.Label(details_card.inner, text=f"Number of Nights: {nights}", 
                font=('Segoe UI', 10), bg=THEME['card_bg'], fg=THEME['muted']).pack(anchor='w')
        tk.Label(details_card.inner, text=f"Rate per Night: ${room.price if room else 0:.2f}", 
                font=('Segoe UI', 10), bg=THEME['card_bg'], fg=THEME['muted']).pack(anchor='w', pady=(0, 10))
        
        # Divider
        ttk.Separator(details_card.inner, orient='horizontal').pack(fill='x', pady=10)
        
        # Payment summary
        tk.Label(details_card.inner, text="PAYMENT SUMMARY", 
                font=('Segoe UI', 11, 'bold'), fg=THEME['primary'], bg=THEME['card_bg']).pack(anchor='w', pady=(10, 5))
        
        subtotal = float(booking.total_price)
        tax = subtotal * 0.10  # 10% tax
        total = subtotal + tax
        
        tk.Label(details_card.inner, text=f"Subtotal: ${subtotal:.2f}", 
                font=('Segoe UI', 10), bg=THEME['card_bg'], fg=THEME['text']).pack(anchor='w')
        tk.Label(details_card.inner, text=f"Tax (10%): ${tax:.2f}", 
                font=('Segoe UI', 10), bg=THEME['card_bg'], fg=THEME['text']).pack(anchor='w')
        
        # Total in highlighted box
        total_frame = tk.Frame(details_card.inner, bg=THEME['primary'], padx=10, pady=5)
        total_frame.pack(fill='x', pady=10)
        tk.Label(total_frame, text=f"TOTAL AMOUNT: ${total:.2f}", 
                font=('Segoe UI', 14, 'bold'), bg=THEME['primary'], fg=THEME['bg']).pack()
        
        tk.Label(details_card.inner, text=f"Status: {booking.status}", 
                font=('Segoe UI', 10, 'bold'), 
                fg=THEME['accent'] if booking.status == 'Completed' else THEME['secondary'], bg=THEME['card_bg']).pack(anchor='w', pady=(10, 5))
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=dialog['bg'])
        button_frame.pack(pady=15)
        make_button(button_frame, "Print Invoice", command=lambda: self.print_invoice(booking), width=15, color=THEME['secondary']).pack(side=tk.LEFT, padx=5)
        make_button(button_frame, "Close", command=dialog.destroy, width=15, color=THEME['muted']).pack(side=tk.LEFT, padx=5)
    
    def print_invoice(self, booking):
        messagebox.showinfo("Print", f"Invoice INV-{booking.id:04d} sent to printer\n(Print functionality to be implemented)")