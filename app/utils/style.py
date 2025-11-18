# app/utils/style.py
import tkinter as tk
from tkinter import font as tkfont


# Theme definitions
THEME = {
    'bg': '#f6f8fa',
    'card_bg': '#ffffff',
    'primary': '#2d8cf0',
    'secondary': '#9b59b6',
    'accent': '#1abc9c',
    'danger': '#e74c3c',
    'muted': '#95a5a6',
    'text': '#2c3e50'
}


def center_window(window, width=400, height=300):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(False, False)
    try:
        window.configure(bg=THEME['bg'])
    except Exception:
        pass


# Default font helpers
def default_font(size=11, weight='normal'):
    return (None, size, weight)


def make_header(master, text):
    lbl = tk.Label(master, text=text, font=('Segoe UI', 16, 'bold'), bg=THEME['bg'], fg=THEME['text'])
    return lbl


def card_frame(master, padx=12, pady=12):
    frame = tk.Frame(master, bg=THEME['card_bg'], bd=1, relief=tk.FLAT)
    # add internal padding via a container
    inner = tk.Frame(frame, bg=THEME['card_bg'])
    inner.pack(padx=padx, pady=pady, fill=tk.BOTH, expand=True)
    frame.inner = inner
    return frame


def make_button(master, text, command=None, color=None, width=15, height=1, fg='white'):
    bg = color or THEME['primary']
    btn = tk.Button(master, text=text, command=command, bg=bg, fg=fg,
                    activebackground=bg, relief=tk.FLAT,
                    font=('Segoe UI', 10, 'bold'))
    if width:
        btn.config(width=width)
    if height:
        try:
            btn.config(height=height)
        except Exception:
            pass
    return btn


def make_link(master, text, command=None):
    lbl = tk.Label(master, text=text, fg=THEME['primary'], bg=THEME['bg'], cursor='hand2')
    if command:
        lbl.bind('<Button-1>', lambda e: command())
    return lbl


def apply_theme(root):
    try:
        root.configure(bg=THEME['bg'])
    except Exception:
        pass