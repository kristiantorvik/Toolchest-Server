import tkinter as tk
from tkinter import messagebox
from api import post

def show_material_form(app):
    app.operation_label.config(text="Add Material")
    app.clear_content()

    tk.Label(app.content_frame, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(app.content_frame)
    name_entry.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Description:").grid(row=1, column=0)
    desc_entry = tk.Entry(app.content_frame)
    desc_entry.grid(row=1, column=1)

    def submit():
        data = {"name": name_entry.get(), "description": desc_entry.get()}
        response = post("materials/", data)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Material Added!")
            app.show_home()
        else:
            messagebox.showerror("Error", f"Error {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=2, column=0, columnspan=2, pady=10)
