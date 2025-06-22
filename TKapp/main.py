import tkinter as tk
from screens import home

class ToolChestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToolChest Server")
        self.root.geometry("500x500")
        self.create_layout()
        self.show_home()

    def create_layout(self):
        self.top_frame = tk.Frame(self.root, bg="#222", height=50)
        self.top_frame.pack(fill=tk.X)

        self.title_label = tk.Label(self.top_frame, text="ToolChest Server", bg="#222", fg="white", font=("Arial", 16))
        self.title_label.pack(side=tk.LEFT, padx=10)

        self.operation_label = tk.Label(self.top_frame, text="Home", bg="#222", fg="lightgray", font=("Arial", 12))
        self.operation_label.pack(side=tk.LEFT, padx=20)

        self.home_button = tk.Button(self.top_frame, text="Home", command=self.show_home)
        self.home_button.pack(side=tk.RIGHT, padx=10)

        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.status_frame = tk.Frame(self.root, bg="#ddd", height=30)
        self.status_frame.pack(fill=tk.X)
        self.status_label = tk.Label(self.status_frame, text="", bg="#ddd", fg="black", font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT, padx=10)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.operation_label.config(text="Home")
        self.clear_content()
        home.show_home(self)

    def set_status(self, message):
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToolChestApp(root)
    root.mainloop()