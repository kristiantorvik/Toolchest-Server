import tkinter as tk
from api import post

def show_strategy_form(app):
    app.operation_label.config(text="Add Strategy")
    app.clear_content()

    tk.Label(app.content_frame, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(app.content_frame)
    name_entry.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Description:").grid(row=1, column=0)
    desc_entry = tk.Entry(app.content_frame)
    desc_entry.grid(row=1, column=1)

    tk.Label(app.content_frame, text="Relevant Recipe Parameters:").grid(row=2, column=0, sticky="n")
    recipe_parameters = ["cutting_speed", "feedrate_fu", "cut_depth", "cut_width", "lifetime", "coolant", "airblast", "pecking_depth"]
    param_listbox = tk.Listbox(app.content_frame, selectmode=tk.MULTIPLE, height=8)
    for param in recipe_parameters:
        param_listbox.insert(tk.END, param)
    param_listbox.grid(row=2, column=1)

    def submit():
        selected_params = param_listbox.curselection()
        selected_param_names = [recipe_parameters[i] for i in selected_params]
        data = {
            "name": name_entry.get(),
            "description": desc_entry.get(),
            "recipe_parameters": selected_param_names
        }
        response = post("strategies/", data)
        if response.status_code == 200:
            app.set_status("Strategy Added Successfully!")
            app.show_home()
        else:
            app.set_status(f"Error {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=10)
