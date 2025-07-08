import tkinter as tk
from api import fetch, post
from helper_func import keybinds


def show_strategy_form(app):
    keybinds.unbind_all(app)
    app.operation_label.config(text="Add Strategy")
    app.clear_content()

    parameters = fetch("/recipe_parameters/")
    if not parameters:
        app.show_home()
        app.set_status("No Recipe Parameters defined. Define them first.")
        return

    tk.Label(app.content_frame, text="Strategy Name:").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(app.content_frame)
    name_entry.grid(row=0, column=1, sticky="ew")

    tk.Label(app.content_frame, text="Description:").grid(row=1, column=0, sticky="w")
    description_entry = tk.Entry(app.content_frame)
    description_entry.grid(row=1, column=1, sticky="ew")

    tk.Label(app.content_frame, text="Recipe Parameters:").grid(row=2, column=0, sticky="nw")

    listbox_frame = tk.Frame(app.content_frame)
    listbox_frame.grid(row=2, column=1, sticky="ew")
    param_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=10, width=40)
    param_listbox.pack(side="left", fill="y")

    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
    scrollbar.config(command=param_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    param_listbox.config(yscrollcommand=scrollbar.set)

    param_id_map = {}
    for idx, param in enumerate(parameters):
        param_listbox.insert(tk.END, param["name"])
        param_id_map[idx] = param["id"]

    def submit(*args):
        name = name_entry.get().strip()
        description = description_entry.get().strip()
        selected_indices = param_listbox.curselection()
        selected_param_ids = [param_id_map[idx] for idx in selected_indices]

        if not name:
            app.set_status("Error: Strategy name is required")
            return
        if not selected_param_ids:
            app.set_status("Error: At least one Recipe Parameter must be selected")
            return

        payload = {
            "name": name,
            "description": description,
            "parameter_ids": selected_param_ids
        }

        print(payload)

        response = post("/strategies/", payload)
        if response.status_code == 200:
            app.show_home()
            app.set_status("Strategy added successfully.")
        else:
            messagebox.showerror("Error", f"Failed to add strategy: {response.status_code}")

    submit_btn = tk.Button(app.content_frame, text="Submit", command=submit)
    submit_btn.grid(row=99, column=0, columnspan=2, pady=10)

    keybinds.bind_key(app, "<Return>", submit)
    name_entry.focus_set()

