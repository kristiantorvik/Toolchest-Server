import tkinter as tk
from api import fetch, post

def show_tooltype_form(app):
    app.operation_label.config(text="Add Tool Type")
    app.clear_content()

    strategies = fetch("strategies/")
    strategy_map = {s["name"]: s["id"] for s in strategies}

    tk.Label(app.content_frame, text="Type Name:").grid(row=0, column=0)
    type_entry = tk.Entry(app.content_frame)
    type_entry.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Supported Strategies:").grid(row=1, column=0, sticky="n")
    strategy_listbox = tk.Listbox(app.content_frame, selectmode=tk.MULTIPLE, height=8)
    for s in strategy_map.keys():
        strategy_listbox.insert(tk.END, s)
    strategy_listbox.grid(row=1, column=1)

    tk.Label(app.content_frame, text="Relevant Tool Parameters:").grid(row=2, column=0, sticky="n")
    tool_parameters = ["diameter", "number_of_flutes", "tool_designation", "description"]
    param_listbox = tk.Listbox(app.content_frame, selectmode=tk.MULTIPLE, height=6)
    for param in tool_parameters:
        param_listbox.insert(tk.END, param)
    param_listbox.grid(row=2, column=1)

    def submit():
        selected_strategies = strategy_listbox.curselection()
        selected_strategy_ids = [strategy_map[list(strategy_map.keys())[i]] for i in selected_strategies]
        selected_params = param_listbox.curselection()
        selected_param_names = [tool_parameters[i] for i in selected_params]

        data = {
            "type_name": type_entry.get(),
            "strategy_ids": selected_strategy_ids,
            "tool_parameters": selected_param_names
        }
        response = post("tool_types/", data)
        if response.status_code == 200:
            app.set_status("Tool Type Added Successfully!")
            app.show_home()
        else:
            app.set_status(f"Error {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=10)