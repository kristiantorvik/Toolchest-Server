import tkinter as tk
from tkinter import ttk
from api import fetch, post
from helper_func import keybinds, validate

def show_recipe_form(app):
    keybinds.unbind_all(app)
    app.operation_label.config(text="Add Recipe")
    app.clear_content()

    # Load materials, strategies and tool data
    materials = fetch("materials/")
    strategies = fetch("strategies/")
    tools = fetch("tools/")

    if not materials or not strategies or not tools:
        app.show_home()
        app.set_status("Please create Materials, Strategies, and Tools first!")
        return

    # Build maps
    material_map = {m["name"]: m["id"] for m in materials}
    strategy_map = {s["name"]: s for s in strategies}
    tool_map = {t["name"]: t for t in tools}

    # Material selector
    tk.Label(app.content_frame, text="Material:").grid(row=0, column=0)
    material_var = tk.StringVar()
    material_keys = list(material_map.keys())
    material_var.set(material_keys[0])
    material_menu = ttk.Combobox(app.content_frame, textvariable=material_var, state="readonly")
    material_menu['values'] = material_keys
    material_menu.grid(row=0, column=1)

    # Strategy selector
    tk.Label(app.content_frame, text="Strategy:").grid(row=1, column=0)
    strategy_var = tk.StringVar()
    strategy_keys = list(strategy_map.keys())
    strategy_var.set(strategy_keys[0])
    strategy_menu = ttk.Combobox(app.content_frame, textvariable=strategy_var, state="readonly")
    strategy_menu['values'] = strategy_keys
    strategy_menu.grid(row=1, column=1)

    # Tool selector (filtered when strategy is selected)
    tk.Label(app.content_frame, text="Tool:").grid(row=2, column=0)
    tool_var = tk.StringVar()
    tool_menu = ttk.Combobox(app.content_frame, textvariable=tool_var, state="readonly")
    tool_menu.grid(row=2, column=1)

    dynamic_fields = {}

    def update_after_strategy(*args):
        selected_strategy = strategy_var.get()
        strategy_id = strategy_map[selected_strategy]["id"]
        tool_var.set("")

        # Update tool list filtered by strategy
        tools_for_strategy = fetch(f"tools/by_strategy/{strategy_id}")
        filtered_tool_map = {t["name"]: t["id"] for t in tools_for_strategy}

        tool_keys = list(filtered_tool_map.keys())
        if tool_keys: tool_var.set(tool_keys[0])
        tool_menu["values"] = tool_keys

        nonlocal tool_map
        tool_map = filtered_tool_map

        # Clear old dynamic fields
        for widget in dynamic_fields.values():
            widget["label"].destroy()
            widget["entry"].destroy()
        dynamic_fields.clear()

        # Load recipe parameters for selected strategy
        parameters = fetch(f"recipe_parameters/by_strategy/{strategy_id}")
        for idx, param in enumerate(parameters):
            pname = param["name"]
            ptype = param["type"]
            id = param["id"]

            label = tk.Label(app.content_frame, text=f"{pname} ({ptype}):")
            label.grid(row=3+idx, column=0)
            entry = tk.Entry(app.content_frame)
            entry.grid(row=3+idx, column=1)
            dynamic_fields[pname] = {"label": label, "entry": entry, "type": ptype, "id": id}

    strategy_var.trace_add(mode="write", callback=update_after_strategy)

    # Initial trigger
    update_after_strategy()

    def submit(*args):
        data = {
            "material_id": material_map[material_var.get()],
            "strategy_id": strategy_map[strategy_var.get()]["id"],
            "tool_id": tool_map[tool_var.get()],
            "parameters": {}
        }
        for pname, info in dynamic_fields.items():
            value = info["entry"].get().strip()
            ptype = info["type"]
            id = info["id"]

            if value == "": pass
            else:
                value, ok = validate.check_input(value, ptype)
                if not ok: 
                    app.set_status("Invalid inputs")
                    return

            data["parameters"][id] = value
        print(data)
        response = post("/recipes/", data)
        if response.status_code == 200:
            app.show_home()
            app.set_status("Recipe Added!")
        else:
            app.set_status(f"Error {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=0, column=3, pady=20)

    keybinds.bind_key(app, "<Return>", submit)
    material_menu.focus_set()

