import ctypes
import ttkbootstrap as ttk
import tkinter as tk
from screens import home, info
from helper_func import keybinds


class ToolChestApp:
    def __init__(self, root):
        self.root = root
        self.enable_dark_titlebar(root)
        self.root.title("ToolChest Server")
        self.root.geometry("800x600")

        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.create_layout()
        self.show_home()
        root.bind("<Escape>", self.show_home)

        try:
            root.iconbitmap("ICON.ico")
        except tk.TclError:
            print("Icon file not found or invalid format.")

    def create_layout(self):
        # Top frame
        self.top_frame = tk.Frame(self.root, bg="#222", height=50)
        self.top_frame.grid(row=0, column=0, sticky="ew")
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.title_label = tk.Label(self.top_frame, text="ToolChest Server", bg="#222", fg="white", font=("Arial", 16))
        self.title_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        self.operation_label = tk.Label(self.top_frame, text="Home", bg="#222", fg="lightgray", font=("Arial", 12))
        self.operation_label.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        self.info_button = ttk.Button(self.top_frame, text="Info", command=self.show_info, bootstyle="outline")
        self.info_button.grid(row=0, column=2, padx=5, pady=10, sticky="e")

        self.home_button = ttk.Button(self.top_frame, text="Home", command=self.show_home, bootstyle="outline")
        self.home_button.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="e")

        # Status bar
        self.status_frame = tk.Frame(self.root, bg="#ddd", height=30)
        self.status_frame.grid(row=2, column=0, sticky="ew")
        self.status_label = tk.Label(self.status_frame, text="", bg="#ddd", fg="black", font=("Arial", 10))
        self.status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.create_content_frame()


    def create_content_frame(self):
        self.content_frame = tk.Frame(self.root)
        self.content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")


    def clear_content(self):
        self.content_frame.destroy()
        self.create_content_frame()


    def show_home(self, *args):
        self.operation_label.config(text="Home")
        self.clear_content()
        keybinds.unbind_all(self)
        home.show_home(self)
        self.set_status("")


    def show_info(self):
        info.show_info(self)


    def kill_bill(self, *args):
        self.root.destroy()


    def set_status(self, message):
        self.status_label.config(text=message)


    def enable_dark_titlebar(self, window):
        """
        Turn a Tkinter window's title bar dark (Win10 1809+, Win11).
        """
        # Ensure window exists
        window.update_idletasks()

        # Constants
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = ctypes.c_int(1)  # 1 = dark mode, 0 = light

        # Get the HWND of the TK window
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())

        # Call the DWM API
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )


if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = ToolChestApp(root)
    root.mainloop()
