import tkinter as tk
from PIL import Image, ImageTk
from helper_func import ScrollableFrame, keybinds


def show_info(app):
    app.operation_label.config(text="Info")
    app.clear_content()
    keybinds.unbind_all(app)

    # Create a scrollable frame
    scroll_frame = ScrollableFrame(app.content_frame)
    scroll_frame.grid(row=0, column=0, sticky="nsew")

    app.content_frame.columnconfigure(0, weight=1)
    app.content_frame.rowconfigure(0, weight=1)
    content = scroll_frame.scrollable_frame

    # Load icon
    try:
        icon_path = "ICON.png"
        icon_img = Image.open(icon_path).resize((128, 128), Image.Resampling.LANCZOS)
        icon = ImageTk.PhotoImage(icon_img)
        icon_label = tk.Label(content, image=icon)
        icon_label.image = icon  # Prevent GC
        icon_label.grid(row=0, column=0, pady=(10, 5), padx=10)
    except Exception as e:
        print("Failed to load icon:", e)

    # Project title
    tk.Label(
        content,
        text="ToolChest Server",
        font=("Arial", 20, "bold")
    ).grid(row=1, column=0, sticky="w", padx=10, pady=(5, 2))

    # Author
    tk.Label(
        content,
        text="Author: Kristian",
        font=("Arial", 12, "italic")
    ).grid(row=2, column=0, sticky="w", padx=10, pady=(0, 10))

    # Description
    tk.Label(
        content,
        text=("This is a process parameter database application for managing industrial process applications,\n"
              "such as machining strategies, stamping, forging, casting etc.\n"
              "Built with FastAPI, SQLite and a Tkinter frontend.\n"
              "The server application can be run locally or launced with docker on fly.io\n\n"
              "The database is very dynamic and can be set up to suit your needs and level of detail.\n\n"
              "Future plans include:\n"
              "• More flexible API's with server-side logic for safe editing and customizing.\n"
              "• Better search and sorting functionality.\n"
              "• Cleaner code with documentation for ease of implementation and customizing.\n"
              "• Web based application for mobile entries etc"),
        wraplength=800,
        justify="left",
        font=("Arial", 12)
    ).grid(row=3, column=0, sticky="w", padx=10, pady=(0, 20))

    # Additional Info
    tk.Label(
        content,
        text="Version: 0.1.0\nEnvironment: Local or Hosted\nPython 3.13\nBackend: FastAPI\nFrontend: Tkinter",
        justify="left"
    ).grid(row=4, column=0, sticky="w", padx=10)

    # Spacer to allow smooth scrolling
    tk.Label(content, text="").grid(row=5, column=0, pady=30)
