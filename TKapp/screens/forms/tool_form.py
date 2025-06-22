import tkinter as tk
from api import fetch, post

def show_tool_form(app):
    app.operation_label.config(text="Add Tool")
    app.clear_content()

    tooltypes = fetch("tool_types/")
    tooltype_map = {t["type_name"]: t for t in tooltypes}
    tooltype_keys = list(tooltype_map.keys())

    dynamic_fields = {}

    def update_after_tooltype(*args):
        selected_tooltype = tooltype_var.get()
        if not selected_tooltype:
            return
        tooltype_id = tooltype_map[selected_tooltype]["id"]

        for widget in dynamic_fields.values():
            widget["label"].destroy()
            widget["entry"].destroy()
        dynamic_fields.clear()

        parameters = fetch(f"tooltype_parameters/{tooltype_id}")
        print("DEBUG: Fetched parameters:", parameters)  # <-- You can add this print to verify!

        for idx, param in enumerate(parameters):
            pname = param["name"]
            ptype = param["type"]
            label = tk.Label(app.content_frame, text=f"{pname} ({ptype}):")
            label.grid(row=2+idx, column=0)
            entry = tk.Entry(app.content_frame)
            entry.grid(row=2+idx, column=1)
            dynamic_fields[pname] = {"label": label, "entry": entry, "type": ptype}


    import json

    def submit():
        data = {
            "name": name_entry.get(),
            "tool_type_id": tooltype_map[tooltype_var.get()]["id"],
            "parameters": {}
        }
        for pname, field in dynamic_fields.items():
            val = field["entry"].get()
            ptype = field["type"]
            if ptype == "int":
                val = int(val)
            elif ptype == "float":
                val = float(val)
            data["parameters"][pname] = val

        # DEBUG: print exactly what is being sent
        print("DEBUG - Sending data to server:")
        print(json.dumps(data, indent=2))

        response = post("tools/", data)
        if response.status_code == 200:
            app.set_status("Tool Added!")
            app.show_home()
        else:
            app.set_status(f"Error {response.status_code}")


    # GUI elements after defining functions
    tk.Label(app.content_frame, text="Tool Name:").grid(row=0, column=0)
    name_entry = tk.Entry(app.content_frame)
    name_entry.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Tool Type:").grid(row=1, column=0)

    tooltype_var = tk.StringVar()
    if tooltype_keys:
        tooltype_var.set(tooltype_keys[0])

    tooltype_menu = tk.OptionMenu(app.content_frame, tooltype_var, *tooltype_keys)
    tooltype_menu.grid(row=1, column=1)

    tooltype_var.trace("w", update_after_tooltype)

    # Manually trigger once after full setup
    if tooltype_keys:
        update_after_tooltype()

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=100, column=0, columnspan=2, pady=20)
