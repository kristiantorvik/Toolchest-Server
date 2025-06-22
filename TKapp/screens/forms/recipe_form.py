import tkinter as tk
from api import fetch, post

def show_recipe_form(app):
    app.operation_label.config(text="Add Recipe")
    app.clear_content()

    # Load materials
    materials = fetch("materials/")
    material_map = {m["name"]: m["id"] for m in materials}

    strategies = fetch("strategies/")
    strategy_map = {s["name"]: s for s in strategies}

    tk.Label(app.content_frame, text="Material:").grid(row=0, column=0)
    material_var = tk.StringVar()
    material_menu = tk.OptionMenu(app.content_frame, material_var, *material_map.keys())
    material_menu.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Strategy:").grid(row=1, column=0)
    strategy_var = tk.StringVar()
    strategy_menu = tk.OptionMenu(app.content_frame, strategy_var, *strategy_map.keys())
    strategy_menu.grid(row=1, column=1)

    tk.Label(app.content_frame, text="Tool:").grid(row=2, column=0)
    tool_var = tk.StringVar()
    tool_menu = tk.OptionMenu(app.content_frame, tool_var, "")
    tool_menu.grid(row=2, column=1)

    dynamic_fields = {}

    def update_after_strategy(*args):
        selected_strategy = strategy_var.get()
        if not selected_strategy:
            return
        strategy_id = strategy_map[selected_strategy]["id"]

        # Update tool list
        tool_response = fetch(f"tools/by_strategy/{strategy_id}")
        tool_map = {t["name"]: t["id"] for t in tool_response}
        tool_var.set("")
        tool_menu["menu"].delete(0, "end")
        for tname in tool_map.keys():
            tool_menu["menu"].add_command(label=tname, command=tk._setit(tool_var, tname))

        # Clear previous parameter fields
        for widget in dynamic_fields.values():
            widget["label"].destroy()
            widget["entry"].destroy()
        dynamic_fields.clear()

        # Fetch recipe parameters for selected strategy
        parameters = fetch(f"strategy_recipe_parameters/{strategy_id}")
        for idx, param in enumerate(parameters):
            pname = param["name"]
            ptype = param["type"]
            label = tk.Label(app.content_frame, text=f"{pname} ({ptype}):")
            label.grid(row=3+idx, column=0)
            entry = tk.Entry(app.content_frame)
            entry.grid(row=3+idx, column=1)
            dynamic_fields[pname] = {"label": label, "entry": entry, "type": ptype}

        app._current_tool_map = tool_map

    strategy_var.trace("w", update_after_strategy)

    def submit():
        try:
            data = {
                "material_id": material_map[material_var.get()],
                "strategy_id": strategy_map[strategy_var.get()]["id"],
                "tool_id": app._current_tool_map[tool_var.get()],
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

            response = post("recipes/", data)
            if response.status_code == 200:
                app.set_status("Recipe Added!")
                app.show_home()
            else:
                app.set_status(f"Error {response.status_code}")
        except Exception as e:
            app.set_status(f"Error: {e}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=100, column=0, columnspan=2, pady=20)
