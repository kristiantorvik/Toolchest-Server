import tkinter as tk
from api import fetch, patch
from helper_func import keybinds


def show_edit_tooltype_form(app, **kwargs):
    keybinds.unbind_all(app)
    app.operation_label.config(text="Edit Tool-Type")
    app.clear_content()
    app.set_status("")

    # Fetch tool parameters and strategies from API
    tool_parameters = fetch("tool_parameters/")
    strategies = fetch("strategies/")

    # Map ids to names for both
    tool_param_map = {param["name"]: param["id"] for param in tool_parameters}
    strategy_map = {strategy["name"]: strategy["id"] for strategy in strategies}

    # ID
    id_var = tk.StringVar()
    tk.Label(app.content_frame, text="ID").grid(row=0, column=0)
    id_entry = tk.Entry(app.content_frame, textvariable=id_var)
    id_entry.grid(row=0, column=1)

    dynamic_frame = tk.Frame(app.content_frame)
    dynamic_frame.grid(row=1, column=0, columnspan=3)

    # Name
    name_var = tk.StringVar()
    tk.Label(dynamic_frame, text="Tool Type Name:").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(dynamic_frame, textvariable=name_var)
    name_entry.grid(row=0, column=1)

    # Tool Parameters Listbox
    tk.Label(dynamic_frame, text="Tool Parameters:").grid(row=1, column=0, sticky="nw")
    tool_param_listbox = tk.Listbox(dynamic_frame, selectmode=tk.MULTIPLE, height=8, exportselection=False)
    tool_param_listbox.grid(row=1, column=1, sticky="w")

    # Strategies Listbox
    tk.Label(dynamic_frame, text="Strategies:").grid(row=2, column=0, sticky="nw")
    strategy_listbox = tk.Listbox(dynamic_frame, selectmode=tk.MULTIPLE, height=8, exportselection=False)
    strategy_listbox.grid(row=2, column=1, sticky="w")


    def update_listbox(*args):
        strategy_listbox.delete(0, tk.END)
        tool_param_listbox.delete(0, tk.END)
        name_var.set("")

        id = id_entry.get()
        try:
            id = int(id)
        except ValueError:
            return

        selected_tooltype = fetch(f"/tooltype/detail/{id}")

        if not selected_tooltype:
            app.set_status(f"No tooltype with ID:{id}")
            return

        name_var.set(selected_tooltype["name"])

        for name in tool_param_map.keys():
            tool_param_listbox.insert(tk.END, name)
            id = tool_param_map[name]
            if id in selected_tooltype["tool_parameter_ids"]:
                tool_param_listbox.selection_set(tk.END)

        for name in strategy_map.keys():
            strategy_listbox.insert(tk.END, name)
            id = strategy_map[name]
            if id in selected_tooltype["strategy_ids"]:
                strategy_listbox.selection_set(tk.END)


    def submit(*args):
        selected_parameters = [tool_param_map[tool_param_listbox.get(i)] for i in tool_param_listbox.curselection()]
        selected_strategies = [strategy_map[strategy_listbox.get(i)] for i in strategy_listbox.curselection()]
        id = id_var.get()
        try:
            id = int(id)
        except ValueError:
            app.set_status("ID must be an integer")
            return
        except Exception as e:
            app.set_status(f"Error: {e}")
            return

        data = {
            "id": id,
            "name": name_entry.get(),
            "tool_parameter_ids": selected_parameters,
            "strategy_ids": selected_strategies,
            "force": False
        }

        response = patch("tooltype/", data)
        if response.ok:
            app.show_home()
            app.set_status("Tooltype changed successfully!")
        elif response.status_code == 403:
            app.set_status("Cannot delete strategy because it is used by recipe.")
        else:
            app.set_status(f"Error: {response.status_code}")



    if 'tooltype_id' in kwargs:
        id_var.set(kwargs['tooltype_id'])
        update_listbox()


    id_var.trace("w", update_listbox)
    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=20)
    keybinds.bind_key(app, "<Return>", submit)
    keybinds.bind_key(app, "c", update_listbox)
    id_entry.focus_set()
