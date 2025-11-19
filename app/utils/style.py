# app/utils/style.py
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


# Premium theme definitions
THEME = {
    'bg': '#0f1724',           # deep navy
    'card_bg': '#0b1220',      # slightly lighter
    'surface': '#0c1324',
    'primary': '#f6c85f',      # warm gold
    'secondary': '#9b9fd3',
    'accent': '#6ee7b7',
    'danger': '#e07a5f',
    'muted': '#98a0b3',
    'text': '#e6eef8'
}


def center_window(window, width=400, height=300):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    try:
        window.configure(bg=THEME['bg'])
    except Exception:
        pass


# Default font helpers
def default_font(size=12, weight='normal'):
    return ('Segoe UI', size, weight)


def _setup_ttk_styles():
    style = ttk.Style()
    # Use default theme and tweak
    try:
        style.theme_use('clam')
    except Exception:
        pass

    base_font = tkfont.nametofont('TkDefaultFont')
    base_font.configure(family='Segoe UI', size=12)

    # General labels and headers
    style.configure('TLabel', background=THEME['bg'], foreground=THEME['text'], font=default_font(13))
    style.configure('Header.TLabel', font=default_font(22, 'bold'), foreground=THEME['primary'], background=THEME['bg'])
    style.configure('Card.TLabel', background=THEME['card_bg'], foreground=THEME['text'], font=default_font(12))
    style.configure('Muted.TLabel', background=THEME['bg'], foreground=THEME['muted'], font=default_font(11))
    style.configure('Primary.TLabel', background=THEME['bg'], foreground=THEME['primary'], font=default_font(13, 'bold'))
    style.configure('Accent.TLabel', background=THEME['bg'], foreground=THEME['accent'], font=default_font(13, 'bold'))
    style.configure('Card.TFrame', background=THEME['card_bg'])

    # Buttons: larger padding for touch-friendly feel
    style.configure('TButton', font=default_font(12, 'bold'), foreground=THEME['text'], background=THEME['surface'], borderwidth=0, padding=(10, 8))
    style.map('TButton', background=[('active', THEME['primary']), ('!active', THEME['surface'])])

    # Primary and secondary accent button styles
    style.configure('Primary.TButton', foreground=THEME['bg'], background=THEME['primary'], font=default_font(12, 'bold'), padding=(12, 8))
    style.map('Primary.TButton', background=[('active', THEME['accent']), ('!active', THEME['primary'])])

    style.configure('Secondary.TButton', foreground=THEME['bg'], background=THEME['secondary'], font=default_font(12, 'bold'), padding=(12, 8))
    style.map('Secondary.TButton', background=[('active', THEME['accent']), ('!active', THEME['secondary'])])

    # Treeview sizing
    style.configure('Treeview', rowheight=30, font=default_font(12), background=THEME['card_bg'], foreground=THEME['text'])
    style.configure('Treeview.Heading', font=default_font(12, 'bold'), background=THEME['surface'], foreground=THEME['text'])


def make_header(master, text):
    lbl = ttk.Label(master, text=text, style='Header.TLabel')
    return lbl


def card_frame(master, padx=16, pady=16):
    frame = ttk.Frame(master, style='Card.TFrame')
    inner = tk.Frame(frame, bg=THEME['card_bg'])
    # Give cards a subtle border and more padding for a premium look
    frame.config(padding=(4, 4, 4, 4))
    inner.pack(padx=padx, pady=pady, fill=tk.BOTH, expand=True)
    frame.inner = inner
    return frame


def _on_enter(e, widget, bg):
    try:
        widget.configure(background=bg)
    except Exception:
        pass


def _on_leave(e, widget, bg):
    try:
        widget.configure(background=bg)
    except Exception:
        pass


def make_button(master, text, command=None, color=None, width=None, height=1, fg=None, variant='primary'):
    """Create a button. By default uses themed ttk button styles (primary/secondary).
    If `color` is provided, falls back to a colored tk.Button for custom colors.
    """
    if color:
        # Fall back to tk.Button when a custom color is requested
        bg = color
        fg = fg or THEME['bg']
        btn = tk.Button(master, text=text, command=command, bg=bg, fg=fg,
                        activebackground=bg, relief=tk.FLAT, bd=0,
                        font=default_font(12, 'bold'), cursor='hand2', padx=12, pady=8)
        if width:
            try:
                btn.config(width=width)
            except Exception:
                pass
        try:
            btn.config(height=height)
        except Exception:
            pass
        btn.bind('<Enter>', lambda e: _on_enter(e, btn, THEME['accent']))
        btn.bind('<Leave>', lambda e: _on_leave(e, btn, bg))
        return btn

    # Use ttk Button with themed styles for consistency
    style_name = 'Primary.TButton' if variant == 'primary' else 'Secondary.TButton'
    try:
        btn = ttk.Button(master, text=text, command=command, style=style_name)
        if width:
            try:
                btn.config(width=width)
            except Exception:
                pass
        return btn
    except Exception:
        # Fallback to tk.Button if ttk fails
        bg = THEME['primary'] if variant == 'primary' else THEME['secondary']
        fg = fg or THEME['bg']
        btn = tk.Button(master, text=text, command=command, bg=bg, fg=fg,
                        activebackground=bg, relief=tk.FLAT, bd=0,
                        font=default_font(12, 'bold'), cursor='hand2', padx=12, pady=8)
        return btn


def make_link(master, text, command=None):
    lbl = tk.Label(master, text=text, fg=THEME['primary'], bg=THEME['bg'], cursor='hand2', font=default_font(10, 'underline'))
    if command:
        lbl.bind('<Button-1>', lambda e: command())
    return lbl


def apply_theme(root, fullscreen=False):
    try:
        root.configure(bg=THEME['bg'])
    except Exception:
        pass
    _setup_ttk_styles()

    # Make window full-screen or maximized (Windows-friendly)
    try:
        if fullscreen:
            # Try zoomed first (keeps window decorations)
            try:
                root.state('zoomed')
            except Exception:
                root.attributes('-fullscreen', True)
        else:
            # ensure window is resizable for responsive layouts
            root.resizable(True, True)
    except Exception:
        pass

    # Provide a convenient ESC binding to exit fullscreen
    def _exit_fullscreen(event=None):
        try:
            root.attributes('-fullscreen', False)
            root.state('normal')
        except Exception:
            pass

    try:
        root.bind('<Escape>', _exit_fullscreen)
    except Exception:
        pass


def make_appbar(master, title="Hotel Booking", show_logout=False, show_fullscreen=True):
    """Create a top application bar with title and controls.

    Returns the appbar frame so callers can pack/place it.
    """
    bar = tk.Frame(master, bg=THEME['surface'], height=56)

    # Left: app name / logo
    logo = tk.Label(bar, text="🏨", bg=THEME['surface'], fg=THEME['primary'], font=default_font(18, 'bold'))
    logo.pack(side=tk.LEFT, padx=(12, 6))
    title_lbl = tk.Label(bar, text=title, bg=THEME['surface'], fg=THEME['text'], font=default_font(16, 'bold'))
    title_lbl.pack(side=tk.LEFT)

    # Spacer
    spacer = tk.Frame(bar, bg=THEME['surface'])
    spacer.pack(side=tk.LEFT, expand=True, fill=tk.X)

    # Right: controls
    if show_fullscreen:
        def _toggle_fullscreen():
            try:
                # For Toplevel windows and root, toggle between zoomed and normal
                state = master.state()
                if state == 'zoomed' or master.attributes('-fullscreen'):
                    try:
                        master.attributes('-fullscreen', False)
                    except Exception:
                        pass
                    try:
                        master.state('normal')
                    except Exception:
                        pass
                else:
                    try:
                        master.state('zoomed')
                    except Exception:
                        try:
                            master.attributes('-fullscreen', True)
                        except Exception:
                            pass
            except Exception:
                pass

        fs_btn = tk.Button(bar, text='⛶', command=_toggle_fullscreen, bg=THEME['muted'], fg=THEME['text'], bd=0, relief=tk.FLAT, cursor='hand2', padx=8, pady=6)
        fs_btn.pack(side=tk.RIGHT, padx=8, pady=6)

    if show_logout:
        logout_btn = tk.Button(bar, text='Logout', bg=THEME['danger'], fg=THEME['bg'], bd=0, relief=tk.FLAT, cursor='hand2', padx=10, pady=6)
        logout_btn.pack(side=tk.RIGHT, padx=8, pady=6)

    return bar