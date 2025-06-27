import tkinter as tk
from tkinter import ttk
from api import fetch, post

def show_search_form(app):
    app.clear_content()

    # Strategy Dropdown
    tk.Label(app.content_frame, text="Select Strategy:").grid(row=0, column=0, sticky="w")
    strategies = fetch("/strategies")
    strategy_map = {s['name']: s['id'] for s in strategies}
    strategy_var = tk.StringVar()
    strategy_dropdown = ttk.Combobox(app.content_frame, textvariable=strategy_var, values=list(strategy_map.keys()))
    strategy_dropdown.grid(row=0, column=1, sticky="ew")

    # Dynamic filter listboxes
    material_listbox = tk.Listbox(app.content_frame, selectmode=tk.MULTIPLE, exportselection=False, height=6)
    tooltype_listbox = tk.Listbox(app.content_frame, selectmode=tk.MULTIPLE, exportselection=False, height=6)
    tool_listbox = tk.Listbox(app.content_frame, selectmode=tk.MULTIPLE, exportselection=False, height=6)

    # Placeholders
    material_label = tk.Label(app.content_frame, text="Materials")
    tooltype_label = tk.Label(app.content_frame, text="Tool Types")
    tool_label = tk.Label(app.content_frame, text="Tools")

    def populate_filters(*args):
        selection = strategy_var.get()
        if not selection:
            return

        strategy_id = strategy_map[selection]

        # fetch filters from backend
        filters = fetch(f"/search/options/{strategy_id}")

        def update_listbox(listbox, values):
            listbox.delete(0, tk.END)
            for item in values:
                listbox.insert(tk.END, item['name'])

                # Store the full tool list for later filtering
        full_tool_list = filters['tools']

        def filter_tools_by_selected_types():
            selected_tooltype_names = [tooltype_listbox.get(i) for i in tooltype_listbox.curselection()]
            filtered_tools = [tool for tool in full_tool_list if tool['tool_type_name'] in selected_tooltype_names]
            update_listbox(tool_listbox, filtered_tools)

        # Rebind event for updating tools when tool types change
        def on_tooltype_select(event):
            selected_indices = tooltype_listbox.curselection()
    
            if not selected_indices:
                # No tooltypes selected: show all tools for the selected strategy
                update_listbox(tool_listbox, full_tool_list)
            else:
                filter_tools_by_selected_types()

            

        tooltype_listbox.bind('<<ListboxSelect>>', on_tooltype_select)

        # Add tool_type_name for filtering
        tooltype_id_name_map = {t['id']: t['name'] for t in filters['tool_types']}
        for tool in full_tool_list:
            tool['tool_type_name'] = tooltype_id_name_map.get(tool['tool_type_id'], "Unknown")

        # Initial full population of tools
        update_listbox(tool_listbox, full_tool_list)


        material_label.grid(row=1, column=0, sticky="w")
        material_listbox.grid(row=2, column=0, sticky="nsew")
        update_listbox(material_listbox, filters['materials'])

        tooltype_label.grid(row=1, column=1, sticky="w")
        tooltype_listbox.grid(row=2, column=1, sticky="nsew")
        update_listbox(tooltype_listbox, filters['tool_types'])

        tool_label.grid(row=1, column=2, sticky="w")
        tool_listbox.grid(row=2, column=2, sticky="nsew")
        update_listbox(tool_listbox, filters['tools'])

    strategy_dropdown.bind("<<ComboboxSelected>>", populate_filters)

    def submit():
        selection = strategy_var.get()
        if not selection:
            app.set_status("Please select a strategy")
            return

        strategy_id = strategy_map[selection]
        selected_materials = [material_listbox.get(i) for i in material_listbox.curselection()]
        selected_tooltypes = [tooltype_listbox.get(i) for i in tooltype_listbox.curselection()]
        selected_tools = [tool_listbox.get(i) for i in tool_listbox.curselection()]

        data = {
            "strategy_id": strategy_id,
            "materials": selected_materials,
            "tool_types": selected_tooltypes,
            "tools": selected_tools
        }

        results = post("/search", data)
        print("Matching Recipe IDs:", results.json())
        app.set_status(f"Found matching recipes. See console for IDs.")

    tk.Button(app.content_frame, text="Search", command=submit).grid(row=3, column=0, columnspan=3, pady=10)
