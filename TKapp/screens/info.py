import tkinter as tk
from helper_func import keybinds


def show_home(app):
    app.operation_label.config(text="INFO")
    app.clear_content()
    keybinds.unbind_all(app)

    testlabel = tk.Label(app.content_frame, text="hei")
    testlabel.grid(row=0, column=0)
