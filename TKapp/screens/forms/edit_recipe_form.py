import tkinter as tk
from tkinter import ttk
from api import fetch, patch
from helper_func import keybinds, validate


def show_edit_recipe_form(app, **kwargs):
    keybinds.unbind_all(app)
    app.operation_label.config(text="Edit Recipe")
    app.set_status("")
    app.clear_content()

    # Load materials, strategies and tool data
    materials = fetch("materials/")
    strategies = fetch("strategies/")
    tools = fetch("tools/")

    # Build maps
    material_map = {m["name"]: m["id"] for m in materials}
    strategy_map = {s["name"]: s for s in strategies}
    tool_map = {t["name"]: t for t in tools}

    # Defining variables
    recipe_id = tk.StringVar()
    material_var = tk.StringVar()
    material_keys = list(material_map.keys())
    strategy_var = tk.StringVar()
    strategy_keys = list(strategy_map.keys())
    tool_var = tk.StringVar()

    # ID selector
    tk.Label(app.content_frame, text="Recipe ID:").grid(row=0, column=0)
    id_entry = tk.Entry(app.content_frame, textvariable=recipe_id, width=10)
    id_entry.grid(row=0, column=1)

    # Dynamic frame
    dynamic_frame = tk.Frame(app.content_frame)
    dynamic_frame.grid(row=1, column=0, columnspan=3)

    # Material selector
    tk.Label(dynamic_frame, text="Material:").grid(row=0, column=0)
    material_menu = ttk.Combobox(dynamic_frame, textvariable=material_var, state="readonly")
    material_menu['values'] = material_keys
    material_menu.grid(row=0, column=1)

    # Strategy selector
    tk.Label(dynamic_frame, text="Strategy:").grid(row=1, column=0)
    strategy_menu = ttk.Combobox(dynamic_frame, textvariable=strategy_var, state="readonly")
    strategy_menu['values'] = strategy_keys
    strategy_menu.grid(row=1, column=1)

    # Tool selector
    tk.Label(dynamic_frame, text="Tool:").grid(row=2, column=0)
    tool_menu = ttk.Combobox(dynamic_frame, textvariable=tool_var, state="readonly")
    tool_menu.grid(row=2, column=1)

    dynamic_fields = {}

    def clear_fields():
        for widget in dynamic_fields.values():
            widget["label"].destroy()
            widget["entry"].destroy()
        dynamic_fields.clear()
        dynamic_frame.grid_forget()

    def update_fields(*args, **kwargs):
        id = recipe_id.get()
        recipe = fetch(f"/recipe_detail/{id}")
        if not recipe:
            clear_fields()
            return

        if 'strategy_id' in kwargs:
            strategy_id = kwargs['strategy_id']
            tool_var.set("")
        else:
            strategy_id = recipe["strategy_id"]
            strategy_var.set(recipe['strategy'])
            tool_var.set(recipe['tool'])


        material_var.set(recipe['material'])

        used_param_keys = recipe["parameters"].keys()

        # Update tool list filtered by strategy
        tools_for_strategy = fetch(f"tools/by_strategy/{strategy_id}")
        filtered_tool_map = {t["name"]: t["id"] for t in tools_for_strategy}

        tool_keys = list(filtered_tool_map.keys())
        if not tool_keys:
            clear_fields()
            return
        tool_menu["values"] = tool_keys


        nonlocal tool_map
        tool_map = filtered_tool_map

        clear_fields()
        dynamic_frame.grid(row=1, column=0, columnspan=2)

        # Load recipe parameters for selected strategy
        parameters = fetch(f"recipe_parameters/by_strategy/{strategy_id}")
        for idx, param in enumerate(parameters):
            pname = param["name"]
            ptype = param["type"]
            pid = param["id"]

            label = tk.Label(app.content_frame, text=f"{pname} ({ptype}):")
            label.grid(row=3 + idx, column=0)
            entry = tk.Entry(app.content_frame)
            entry.grid(row=3 + idx, column=1)

            if pname in used_param_keys:
                value = recipe["parameters"][pname]
                entry.insert(0, value)

            dynamic_fields[pname] = {"label": label, "entry": entry, "type": ptype, "id": pid}

    def changed_strategy_update(*args):
        strategy_id = strategy_map[strategy_var.get()]["id"]
        update_fields(strategy_id=strategy_id)


    recipe_id.trace_add(mode="write", callback=update_fields)
    strategy_var.trace_add(mode="write", callback=(changed_strategy_update))



    def submit(*args):
        data = {
            "id": recipe_id.get(),
            "material_id": material_map[material_var.get()],
            "strategy_id": strategy_map[strategy_var.get()]["id"],
            "tool_id": tool_map[tool_var.get()],
            "parameters": {}
        }

        for pname, info in dynamic_fields.items():
            value = info["entry"].get().strip()
            ptype = info["type"]
            id = info["id"]

            if value == "":
                pass
            else:
                value, ok = validate.check_input(value, ptype)
                if not ok:
                    app.set_status("Invalid inputs")
                    return

            data["parameters"][id] = value

        response = patch("recipe/", data)
        if response.status_code == 200:
            app.show_home()
            app.set_status("Recipe Updated!")
        else:
            app.set_status(f"Error {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=0, column=3, pady=20, padx=20)

    if 'recipe_id' in kwargs:
        recipe_id.set(kwargs['recipe_id'])
    keybinds.bind_key(app, "<Return>", submit)

    material_menu.focus_set()
