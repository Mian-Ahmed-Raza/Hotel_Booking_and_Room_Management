# app/views/feedback.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.models.review import Review
from app.models.booking import Booking
from app.utils.style import center_window, apply_theme, make_button, make_header, card_frame, THEME, make_appbar


class FeedbackWindow:
    def __init__(self, master):
        self.master = master
        master.title("Feedback & Reviews")
        center_window(master, 1000, 600)
        apply_theme(master)
        # App bar
        make_appbar(master, title="Feedback & Reviews").pack(fill=tk.X)
        make_header(master, "Guest Feedback & Reviews").pack(pady=(12, 6))

        try:
            avg_rating = Review.get_average_rating()
            total_reviews = len(Review.get_all())
        except:
            avg_rating = 0.0
            total_reviews = 0

        # Stats card
        stats_card = card_frame(master)
        stats_card.pack(pady=10, padx=10, fill=tk.X)

        stats_left = tk.Frame(stats_card.inner, bg=THEME['card_bg'])
        stats_left.pack(side=tk.LEFT, padx=20, pady=10)
        ttk.Label(stats_left, text="Average Rating:", style='Primary.TLabel').pack()
        ttk.Label(stats_left, text=f"{'⭐' * int(avg_rating)} {avg_rating:.1f}/5.0", style='Accent.TLabel').pack()

        stats_right = tk.Frame(stats_card.inner, bg=THEME['card_bg'])
        stats_right.pack(side=tk.LEFT, padx=20, pady=10)
        ttk.Label(stats_right, text="Total Reviews:", style='Primary.TLabel').pack()
        ttk.Label(stats_right, text=str(total_reviews), style='Primary.TLabel').pack()

        # Button frame
        button_frame = tk.Frame(master, bg=master['bg'])
        button_frame.pack(pady=10)

        make_button(button_frame, "Add Review", command=self.add_review, width=15, color=THEME['primary']).pack(side=tk.LEFT, padx=5)
        make_button(button_frame, "Delete Review", command=self.delete_review, width=15, color=THEME['danger']).pack(side=tk.LEFT, padx=5)
        make_button(button_frame, "Refresh", command=self.load_reviews, width=15, color=THEME['muted']).pack(side=tk.LEFT, padx=5)
        
        # Treeview for displaying reviews
        tree_frame = tk.Frame(master)
        tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Booking', 'Guest', 'Rating', 'Comment', 'Date'), 
                                  show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='Review ID')
        self.tree.heading('Booking', text='Booking ID')
        self.tree.heading('Guest', text='Guest Name')
        self.tree.heading('Rating', text='Rating')
        self.tree.heading('Comment', text='Comment')
        self.tree.heading('Date', text='Date')
        
        self.tree.column('ID', width=80)
        self.tree.column('Booking', width=100)
        self.tree.column('Guest', width=150)
        self.tree.column('Rating', width=100)
        self.tree.column('Comment', width=350)
        self.tree.column('Date', width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Load reviews
        self.load_reviews()
        
        # Back button
        make_button(master, "Back to Dashboard", command=master.destroy, width=20, color=THEME['muted']).pack(pady=10)
    
    def load_reviews(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load reviews from database
        try:
            reviews = Review.get_all()
            for review in reviews:
                rating_stars = '⭐' * review.rating
                self.tree.insert('', tk.END, values=(
                    review.id,
                    review.booking_id,
                    review.guest_name,
                    f"{rating_stars} ({review.rating}/5)",
                    review.comment or '',
                    review.created_at
                ))
            
            # Update stats
            avg_rating = Review.get_average_rating()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load reviews: {str(e)}")
    
    def add_review(self):
        AddReviewDialog(self.master, self)
    
    def delete_review(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a review to delete")
            return
        
        item = self.tree.item(selected[0])
        review_id = item['values'][0]
        guest_name = item['values'][2]
        
        if messagebox.askyesno("Confirm Delete", f"Delete review from {guest_name}?"):
            try:
                Review.delete(review_id)
                messagebox.showinfo("Success", "Review deleted successfully")
                self.load_reviews()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete review: {str(e)}")


class AddReviewDialog:
    def __init__(self, parent, feedback_window):
        self.feedback_window = feedback_window
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Review")
        center_window(self.dialog, 480, 460)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        apply_theme(self.dialog)
        container = card_frame(self.dialog)
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # Booking Selection
        tk.Label(container.inner, text="Select Completed Booking:", bg=THEME['card_bg']).pack(pady=(12, 6), anchor='w')
        self.booking_var = tk.StringVar()
        self.booking_combo = ttk.Combobox(container.inner, textvariable=self.booking_var, width=44, state='readonly')
        self.booking_combo.pack()
        self.load_completed_bookings()

        # Guest Name
        tk.Label(container.inner, text="Guest Name:", bg=THEME['card_bg']).pack(pady=(12, 6), anchor='w')
        self.guest_name_entry = tk.Entry(container.inner, width=46)
        self.guest_name_entry.pack()

        # Rating
        tk.Label(container.inner, text="Rating:", bg=THEME['card_bg']).pack(pady=(12, 6), anchor='w')
        rating_frame = tk.Frame(container.inner, bg=THEME['card_bg'])
        rating_frame.pack()

        self.rating_var = tk.IntVar(value=5)
        for i in range(1, 6):
            ttk.Radiobutton(rating_frame, text=f"{'⭐' * i} ({i})", variable=self.rating_var,
                          value=i, style='TButton').pack(anchor='w')

        # Comment
        tk.Label(container.inner, text="Comment:", bg=THEME['card_bg']).pack(pady=(12, 6), anchor='w')
        self.comment_text = tk.Text(container.inner, width=46, height=6)
        self.comment_text.pack()

        # Buttons
        button_frame = tk.Frame(container.inner, bg=THEME['card_bg'])
        button_frame.pack(pady=12)
        make_button(button_frame, "Submit Review", command=self.save_review, width=15, color=THEME['primary']).pack(side=tk.LEFT, padx=5)
        make_button(button_frame, "Cancel", command=self.dialog.destroy, width=15, color=THEME['muted']).pack(side=tk.LEFT, padx=5)

        # Bind booking selection to auto-fill guest name
        self.booking_combo.bind('<<ComboboxSelected>>', self.on_booking_selected)
    
    def load_completed_bookings(self):
        try:
            bookings = Booking.get_all()
            completed = [b for b in bookings if b.status == 'Completed']
            booking_list = [f"Booking #{b.id} - {b.guest_name}" for b in completed]
            self.booking_combo['values'] = booking_list
            self.bookings = completed
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bookings: {str(e)}")
    
    def on_booking_selected(self, event):
        index = self.booking_combo.current()
        if index >= 0:
            booking = self.bookings[index]
            self.guest_name_entry.delete(0, tk.END)
            self.guest_name_entry.insert(0, booking.guest_name)
    
    def save_review(self):
        if not self.booking_var.get():
            messagebox.showwarning("Warning", "Please select a booking")
            return
        
        guest_name = self.guest_name_entry.get().strip()
        if not guest_name:
            messagebox.showwarning("Warning", "Please enter guest name")
            return
        
        rating = self.rating_var.get()
        comment = self.comment_text.get("1.0", tk.END).strip()
        
        try:
            index = self.booking_combo.current()
            booking = self.bookings[index]
            
            Review.create(booking.id, guest_name, rating, comment)
            messagebox.showinfo("Success", "Review submitted successfully!")
            self.feedback_window.load_reviews()
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save review: {str(e)}")
