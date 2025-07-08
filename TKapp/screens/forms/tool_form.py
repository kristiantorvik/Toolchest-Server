import tkinter as tk
from api import fetch, post
from helper_func import keybinds, validate


def show_tool_form(app):
    keybinds.unbind_all(app)
    app.operation_label.config(text="Add Tool")
    app.clear_content()

    # Load tool types
    tooltypes = fetch("tool_types/")
    if not tooltypes:
        app.show_home()
        app.set_status("Please create Tool Types first!")
        return

    tooltype_map = {t["name"]: t for t in tooltypes}
    tooltype_names = list(tooltype_map.keys())

    # UI layout
    tk.Label(app.content_frame, text="Tool Name:").grid(row=0, column=0)
    name_entry = tk.Entry(app.content_frame)
    name_entry.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Tool Type:").grid(row=1, column=0)
    tooltype_var = tk.StringVar(value=tooltype_names[0])
    tk.OptionMenu(app.content_frame, tooltype_var, *tooltype_names).grid(row=1, column=1)

    # Dynamic parameter fields
    dynamic_fields = {}

    def update_fields(*_):
        # Clear old fields
        for widgets in dynamic_fields.values():
            widgets["label"].destroy()
            widgets["entry"].destroy()
        dynamic_fields.clear()

        selected_tooltype = tooltype_map[tooltype_var.get()]
        parameters = fetch(f"/tool_parameters/by_tooltype/{selected_tooltype['id']}")

        for i, param in enumerate(parameters):
            pname, ptype = param["name"], param["type"]
            label = tk.Label(app.content_frame, text=f"{pname} ({ptype}):")
            label.grid(row=2 + i, column=0)
            entry = tk.Entry(app.content_frame)
            entry.grid(row=2 + i, column=1)
            dynamic_fields[pname] = {"label": label, "entry": entry, "type": ptype}

    tooltype_var.trace("w", update_fields)
    update_fields()

    def submit(*args):
        tool_data = {
            "name": name_entry.get(),
            "tool_type_id": tooltype_map[tooltype_var.get()]["id"],
            "parameters": {}
        }

        for pname, info in dynamic_fields.items():
            value = info["entry"].get()
            ptype = info["type"]
            if value == "": pass
            else:
                value, ok = validate.check_input(value, ptype)
                if not ok: 
                    app.set_status("Invalid inputs")
                    return

            tool_data["parameters"][pname] = value

        response = post("tools/", tool_data)
        if response.status_code == 200:
            app.show_home()
            app.set_status("Tool added!")
        else:
            app.set_status(f"Error {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=100, column=0, columnspan=2, pady=20)
    keybinds.bind_key(app, "<Return>", submit)
    name_entry.focus_set()


