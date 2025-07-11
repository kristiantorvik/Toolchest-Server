import tkinter as tk
from api import post
from helper_func import keybinds


def show_material_form(app):
    app.operation_label.config(text="Add Material")
    app.clear_content()
    keybinds.unbind_all(app)

    name_var = tk.StringVar(value="")
    comment_var = tk.StringVar(value="")

    tk.Label(app.content_frame, text="Material Name:").grid(row=0, column=0)
    name_entry = tk.Entry(app.content_frame, textvariable=name_var)
    name_entry.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Comment:").grid(row=1, column=0)
    comment_entry = tk.Entry(app.content_frame, textvariable=comment_var)
    comment_entry.grid(row=1, column=1)

    def submit(*args):
        data = {
            "name": name_var.get(),
            "comment": comment_var.get()
        }
        response = post("materials/", data)
        if response.status_code == 200:
            app.set_status("Material Added!")
            name_var.set("")
            comment_var.set("")
            name_entry.focus_set()

        else:
            app.set_status(f"Error {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=20)

    keybinds.bind_key(app, "<Return>", submit)
    name_entry.focus_set()
