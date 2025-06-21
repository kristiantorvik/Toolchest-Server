import tkinter as tk
from tkinter import messagebox, ttk
from api import fetch, post

def show_tool_form(app):
    app.operation_label.config(text="Add Tool")
    app.clear_content()

    tooltypes = fetch("tool_types/")
    tooltype_map = {t["type_name"]: t["id"] for t in tooltypes}

    tk.Label(app.content_frame, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(app.content_frame)
    name_entry.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Tool Type:").grid(row=1, column=0)
    combo_tooltype = ttk.Combobox(app.content_frame, values=list(tooltype_map.keys()))
    combo_tooltype.grid(row=1, column=1)

    tk.Label(app.content_frame, text="Diameter:").grid(row=2, column=0)
    diameter_entry = tk.Entry(app.content_frame)
    diameter_entry.grid(row=2, column=1)

    tk.Label(app.content_frame, text="# Flutes:").grid(row=3, column=0)
    flutes_entry = tk.Entry(app.content_frame)
    flutes_entry.grid(row=3, column=1)

    tk.Label(app.content_frame, text="Designation:").grid(row=4, column=0)
    designation_entry = tk.Entry(app.content_frame)
    designation_entry.grid(row=4, column=1)

    tk.Label(app.content_frame, text="Description:").grid(row=5, column=0)
    desc_entry = tk.Entry(app.content_frame)
    desc_entry.grid(row=5, column=1)

    def submit():
        data = {
            "name": name_entry.get(),
            "tool_type_id": tooltype_map[combo_tooltype.get()],
            "diameter": float(diameter_entry.get()),
            "number_of_flutes": int(flutes_entry.get()),
            "tool_designation": designation_entry.get(),
            "description": desc_entry.get()
        }
        response = post("tools/", data)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Tool Added!")
            app.show_home()
        else:
            messagebox.showerror("Error", f"Error {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=6, column=0, columnspan=2, pady=10)