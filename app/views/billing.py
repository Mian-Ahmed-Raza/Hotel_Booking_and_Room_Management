# app/views/billing.py
import tkinter as tk


class BillingWindow:
    def __init__(self, master):
        self.master = master
        master.title("Billing")
        tk.Label(master, text="Billing UI - to be implemented").pack(padx=20, pady=20)