import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from api import fetch, post, delete
from helper_func import keybinds, SmartTree
from screens.forms import edit_recipe_form
from screens.forms import recipe_from_old_form


def show_search_form(app):
    keybinds.unbind_all(app)
    app.operation_label.config(text="Search Recipe")
    app.clear_content()

    strategies = fetch("/strategies/")
    if not strategies:
        app.show_home()
        app.set_status("No recipes in DB")
        return

    stragegy_map = {t["name"]: t for t in strategies}
    strategy_keys = list(stragegy_map.keys())

    strategy_frame = tk.Frame(app.content_frame)
    strategy_frame.grid(row=0, column=0, sticky='NEW', padx=50, pady=10)
    tk.Label(strategy_frame, text="Strategy:").grid(row=0, column=0)

    strategy_var = tk.StringVar()
    strategy_var.set(strategy_keys[0])
    strategy_dropdown = ttk.Combobox(strategy_frame, textvariable=strategy_var, state="readonly")
    strategy_dropdown.grid(row=0, column=1)

    strategy_dropdown['values'] = strategy_keys

    listbox_frame = tk.Frame(app.content_frame, borderwidth=2, relief="flat")
    listbox_frame.grid(row=1, column=0, sticky='NW', pady=10)

    material_frame = tk.Frame(listbox_frame)
    material_frame.grid(row=0, column=0, padx=10, pady=5)
    tooltype_frame = tk.Frame(listbox_frame)
    tooltype_frame.grid(row=0, column=1, padx=10, pady=5)
    tool_frame = tk.Frame(listbox_frame)
    tool_frame.grid(row=0, column=2, padx=10, pady=5)

    button_frame = tk.Frame(app.content_frame, padx=3)
    button_frame.grid(row=1, column=1, sticky='W')


    tk.Label(material_frame, text="Materials").grid(row=0, column=0)
    tk.Label(tooltype_frame, text="Tool Types").grid(row=0, column=0)
    tk.Label(tool_frame, text="Tools").grid(row=0, column=0)

    material_listbox = tk.Listbox(material_frame, selectmode=tk.MULTIPLE, exportselection=False)
    material_listbox.grid(row=1, column=0)
    tooltype_listbox = tk.Listbox(tooltype_frame, selectmode=tk.MULTIPLE, exportselection=False)
    tooltype_listbox.grid(row=1, column=0)
    tool_listbox = tk.Listbox(tool_frame, selectmode=tk.MULTIPLE, exportselection=False)
    tool_listbox.grid(row=1, column=0)

    tree = SmartTree(app.content_frame)
    tree.grid(row=2, column=0, sticky='NW', padx=5, pady=5, columnspan=3)

    app.content_frame.grid_columnconfigure(2, weight=1)

    filters = {}
    full_tool_list = []

    def update_listbox(listbox, items):
        listbox.delete(0, tk.END)
        for item in items:
            listbox.insert(tk.END, f"{item['id']}: {item['name']}")

    def update_tools(*args):
        selected_tooltypes = [tooltype_listbox.get(i).split(':')[0] for i in tooltype_listbox.curselection()]
        if selected_tooltypes:
            filtered_tools = [t for t in full_tool_list if str(t['tool_type_id']) in selected_tooltypes]
        else:
            filtered_tools = full_tool_list
        update_listbox(tool_listbox, filtered_tools)

    def populate_filters(*args):
        selected_strategy = stragegy_map[strategy_var.get()]
        data = fetch(f"/search/options/{selected_strategy['id']}")
        filters.clear()
        if not data:
            tree.empty()
            return
        filters.update(data)

        update_listbox(material_listbox, filters['materials'])
        update_listbox(tooltype_listbox, filters['tool_types'])
        update_listbox(tool_listbox, filters['tools'])

        nonlocal full_tool_list
        full_tool_list = filters['tools']

        tooltype_listbox.bind('<<ListboxSelect>>', update_tools)
        submit()

    def submit(*args):
        tree.empty()
        selected_strategy = stragegy_map[strategy_var.get()]
        materials = [material_listbox.get(i).split(':')[0] for i in material_listbox.curselection()]
        tooltypes = [tooltype_listbox.get(i).split(':')[0] for i in tooltype_listbox.curselection()]
        tools = [tool_listbox.get(i).split(':')[0] for i in tool_listbox.curselection()]

        payload = {
            "strategy_id": selected_strategy['id'],
            "material_ids": list(map(int, materials)),
            "tool_type_ids": list(map(int, tooltypes)),
            "tool_ids": list(map(int, tools)),
        }

        recipe_ids = post("/search/", payload).json()


        if not recipe_ids:
            app.set_status("Found no matching recipe in DB")
        else:
            app.set_status(f"Found {len(recipe_ids)} matching recipes")


        # Fetch all recipe details and collect their parameter keys
        recipe_details = []
        used_param_keys = set()

        all_parameters = fetch(f"recipe_parameters/by_strategy/{selected_strategy['id']}")
        all_param_keys = ([param["name"] for param in all_parameters])


        for rid in recipe_ids:
            data = fetch(f"/recipe_detail/{rid}")
            used_param_keys.update(data["parameters"].keys())

            if "parameters" in data:
                data.update(data.pop("parameters"))

            recipe_details.append(data)


        used_param_keys = [name for name in all_param_keys if name in used_param_keys]

        # Now build the final ordered column list:
        columns = ["id", "material", "tool"] + (used_param_keys)

        tree.write(recipe_details, columns=columns)




    def edit_selected_recipe(*args):
        selected_rows = tree.selection()  # Returns a tuple of selected item IDs
        if len(selected_rows) == 1:
            item_data = tree.item(selected_rows[0])  # Returns a dictionary of attributes for first item
            id = item_data["values"][0]
            edit_recipe_form.show_edit_recipe_form(app, recipe_id=id)

        elif len(selected_rows) > 1:
            app.set_status("Select only one entry to edit")
            return

    def delete_selected_recipe(*args):
        recipes_to_delete = []
        selected_rows = tree.selection()  # Returns a tuple of selected item IDs

        for row in selected_rows:
            item_data = tree.item(row)  # Returns a dictionary of attributes
            recipes_to_delete.append(item_data['values'][0])

        if not recipes_to_delete:
            return

        ok = messagebox.askokcancel("Confirm delete!", f"Permanently delete:{recipes_to_delete}\nThis cannot be undone")
        if not ok:
            return

        for recipe_id in recipes_to_delete:
            print(recipe_id)
            response = delete(f"/recipes/{recipe_id}")

            if response:
                app.set_status(f"Deleted recipe {recipe_id}")
                submit()
            else:
                app.set_status(f"Error when deleting tool {recipe_id}")

    def create_new():
        selected_rows = tree.selection()  # Returns a tuple of selected item IDs
        if len(selected_rows) == 1:
            item_data = tree.item(selected_rows[0])  # Returns a dictionary of attributes for first item
            id = item_data["values"][0]
            recipe_from_old_form.show_recipe_from_old(app, recipe_id=id)

        elif len(selected_rows) > 1:
            app.set_status("Select only one to create new")
            return



    tk.Button(button_frame, text="Search", command=submit, width=15).grid(row=0, column=0, pady=5, sticky="W")
    tk.Label(button_frame, text="Enter").grid(row=0, column=1, sticky="W")
    tk.Button(button_frame, text="Edit", command=edit_selected_recipe, width=15).grid(row=1, column=0, pady=5, sticky="W")
    tk.Label(button_frame, text="E").grid(row=1, column=1, sticky="W")
    tk.Button(button_frame, text="Delete", command=delete_selected_recipe, width=15).grid(row=2, column=0, pady=5, sticky="W")
    tk.Label(button_frame, text="Backspace").grid(row=2, column=1, sticky="W")
    tk.Button(button_frame, text="Create new\n from selected", command=create_new, width=15).grid(row=3, column=0, pady=5, sticky="W")
    tk.Label(button_frame, text="C").grid(row=3, column=1, sticky="W")

    strategy_dropdown.bind("<<ComboboxSelected>>", populate_filters)
    populate_filters()
    keybinds.bind_key(app, "<Return>", submit)
    tree.bind("e", edit_selected_recipe)
    tree.bind("<BackSpace>", delete_selected_recipe)
    tree.bind("<Delete>", delete_selected_recipe)
    tree.bind("d", delete_selected_recipe)
    tree.bind("c", create_new)


    keybinds.bind_key(app, "<Return>", submit)
    strategy_dropdown.focus_set()
