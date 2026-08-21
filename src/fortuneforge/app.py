"""FortuneForge desktop application."""

import tkinter as tk
from tkinter import ttk

APP_TITLE = "FortuneForge"
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 480


def build_app() -> tk.Tk:
    """Create and configure the FortuneForge main window."""
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.minsize(600, 400)

    main_frame = ttk.Frame(root, padding=24)
    main_frame.pack(fill="both", expand=True)

    title_label = ttk.Label(
        main_frame,
        text="FortuneForge",
        font=("TkDefaultFont", 20, "bold"),
    )
    title_label.pack(pady=(20, 8))

    subtitle_label = ttk.Label(
        main_frame,
        text="Multilingual Fortune Cookie Generator",
    )
    subtitle_label.pack()

    status_label = ttk.Label(
        main_frame,
        text="Application scaffold initialized successfully.",
    )
    status_label.pack(pady=(40, 0))

    return root


def main() -> None:
    """Launch the FortuneForge desktop application."""
    app = build_app()
    app.mainloop()


if __name__ == "__main__":
    main()
