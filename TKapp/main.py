import ctypes
import tkinter as tk
from screens import home, info
from helper_func import keybinds


class ToolChestApp:
    def __init__(self, root):
        self.root = root
        self.enable_dark_titlebar(root)
        self.root.title("ToolChest Server")
        self.root.geometry("800x600")
        self.create_layout()
        self.show_home()
        root.bind("<Escape>", self.show_home)
        root.bind("Q", self.kill_bill)

        # Set the window icon
        try:
            root.iconbitmap("TKapp/ICON.ico")
        except tk.TclError:
            print("Icon file not found or invalid format.")


    def create_layout(self):
        self.top_frame = tk.Frame(self.root, bg="#222", height=50)
        self.top_frame.pack(fill=tk.X)

        self.title_label = tk.Label(self.top_frame, text="ToolChest Server", bg="#222", fg="white", font=("Arial", 16))
        self.title_label.pack(side=tk.LEFT, padx=10)

        self.operation_label = tk.Label(self.top_frame, text="Home", bg="#222", fg="lightgray", font=("Arial", 12))
        self.operation_label.pack(side=tk.LEFT, padx=20)

        self.home_button = tk.Button(self.top_frame, text="Home", command=self.show_home)
        self.home_button.pack(side=tk.RIGHT, padx=10)

        self.info_button = tk.Button(self.top_frame, text="info", command=self.show_info)
        self.info_button.pack(side=tk.RIGHT, padx=10)

        self.create_content_frame()

        self.status_frame = tk.Frame(self.root, bg="#ddd", height=30)
        self.status_frame.pack(fill=tk.X)
        self.status_label = tk.Label(self.status_frame, text="", bg="#ddd", fg="black", font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT, padx=10)


    def create_content_frame(self):
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


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
        info.show_home(self)


    def kill_bill(self, *args):
        root.destroy()


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
    root = tk.Tk()
    app = ToolChestApp(root)
    root.mainloop()
