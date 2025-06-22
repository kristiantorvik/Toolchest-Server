import tkinter as tk
from api import post

def show_tool_parameter_form(app):
    app.operation_label.config(text="Add Tool Parameter")
    app.clear_content()

    tk.Label(app.content_frame, text="Parameter Name:").grid(row=0, column=0)
    name_entry = tk.Entry(app.content_frame)
    name_entry.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Type (string/int/float):").grid(row=1, column=0)
    type_entry = tk.Entry(app.content_frame)
    type_entry.grid(row=1, column=1)

    tk.Label(app.content_frame, text="Description:").grid(row=2, column=0)
    desc_entry = tk.Entry(app.content_frame)
    desc_entry.grid(row=2, column=1)

    def submit():
        data = {
            "name": name_entry.get(),
            "type": type_entry.get(),
            "description": desc_entry.get()
        }
        response = post("tool_parameters/", data)
        if response.status_code == 200:
            app.set_status("Tool Parameter Added!")
            app.show_home()
        else:
            app.set_status(f"Error {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=10)

def show_recipe_parameter_form(app):
    app.operation_label.config(text="Add Recipe Parameter")
    app.clear_content()

    tk.Label(app.content_frame, text="Parameter Name:").grid(row=0, column=0)
    name_entry = tk.Entry(app.content_frame)
    name_entry.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Type (string/int/float):").grid(row=1, column=0)
    type_entry = tk.Entry(app.content_frame)
    type_entry.grid(row=1, column=1)

    tk.Label(app.content_frame, text="Description:").grid(row=2, column=0)
    desc_entry = tk.Entry(app.content_frame)
    desc_entry.grid(row=2, column=1)

    def submit():
        data = {
            "name": name_entry.get(),
            "type": type_entry.get(),
            "description": desc_entry.get()
        }
        response = post("recipe_parameters/", data)
        if response.status_code == 200:
            app.set_status("Recipe Parameter Added!")
            app.show_home()
        else:
            app.set_status(f"Error {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=10)
