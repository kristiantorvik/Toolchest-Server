import tkinter as tk
from api import fetch, post
from main import ToolChestApp


def show_tooltype_form(app):
    app.operation_label.config(text="Add Tool Type")
    app.clear_content()

    # Fetch tool parameters and strategies from API
    tool_parameters = fetch("tool_parameters/")
    strategies = fetch("strategies/")

    # Map ids to names for both
    tool_param_map = {param["name"]: param["id"] for param in tool_parameters}
    strategy_map = {strategy["name"]: strategy["id"] for strategy in strategies}

    # Label + Entry for name
    tk.Label(app.content_frame, text="Tool Type Name:").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(app.content_frame)
    name_entry.grid(row=0, column=1)

    # Tool Parameters Listbox
    tk.Label(app.content_frame, text="Tool Parameters:").grid(row=1, column=0, sticky="nw")
    tool_param_listbox = tk.Listbox(app.content_frame, selectmode=tk.MULTIPLE, height=8, exportselection=False)
    for name in tool_param_map.keys():
        tool_param_listbox.insert(tk.END, name)
    tool_param_listbox.grid(row=1, column=1, sticky="w")

    # Strategies Listbox
    tk.Label(app.content_frame, text="Strategies:").grid(row=2, column=0, sticky="nw")
    strategy_listbox = tk.Listbox(app.content_frame, selectmode=tk.MULTIPLE, height=8, exportselection=False)
    for name in strategy_map.keys():
        strategy_listbox.insert(tk.END, name)
    strategy_listbox.grid(row=2, column=1, sticky="w")

    def submit(*args):
        selected_parameters = [tool_param_map[tool_param_listbox.get(i)] for i in tool_param_listbox.curselection()]
        selected_strategies = [strategy_map[strategy_listbox.get(i)] for i in strategy_listbox.curselection()]
        data = {
            "name": name_entry.get(),
            "tool_parameter_ids": selected_parameters,
            "strategy_ids": selected_strategies
        }
        print("DEBUG POST:", data)  # Optional debug print

        response = post("tool_types/", data)
        if response.ok:
            app.set_status("Tool Type added successfully!")
            app.show_home()
        else:
            app.set_status(f"Error: {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=20)
    ToolChestApp.bind_key(app, "<Return>", submit)
    name_entry.focus_set()

