import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from api import fetch, post, delete
import tkinter.font as tkfont
from helper_func import keybinds
from screens.forms import edit_tool_form

def show_tool_search_form(app):
    keybinds.unbind_all(app)
    app.operation_label.config(text="Search Tools")
    app.set_status("")
    app.clear_content()

    tool_types = fetch("tool_types/")
    if not tool_types:
        app.show_home()
        app.set_status("No tool types in DB")
        return
    
    
    tool_type_map = {t["name"]: t for t in tool_types}
    tool_type_keys = list(tool_type_map.keys())

    tool_type_frame = tk.Frame(app.content_frame)
    tool_type_frame.grid(row=0, column=0, sticky='NEW', padx=20, pady=10)
    tk.Label(tool_type_frame, text="Tool Type:").grid(row=0, column=0)

    tool_type_var = tk.StringVar()
    tool_type_var.set(tool_type_keys[0])
    tool_type_dropdown = ttk.Combobox(tool_type_frame, textvariable=tool_type_var, state="readonly")
    tool_type_dropdown.grid(row=0, column=1)
    tool_type_dropdown['values'] = tool_type_keys

    filter_frame = tk.Frame(app.content_frame)
    filter_frame.grid(row=1, column=0)

    button_frame = tk.Frame(app.content_frame, padx=20)
    button_frame.grid(row=0, column=1, rowspan=2)


    
    # Dynamic parameter fields
    dynamic_fields = {}

    def update_fields(*args):
        # Clear old fields
        for widgets in dynamic_fields.values():
            widgets["label"].destroy()
            widgets["entry"].destroy()
        dynamic_fields.clear()

        selected_tooltype = tool_type_map[tool_type_var.get()]
        parameters = fetch(f"tool_parameters/by_tooltype/{selected_tooltype['id']}")

        for i, param in enumerate(parameters):
            pname, ptype = param["name"], param["type"]
            label = tk.Label(filter_frame, text=f"{pname} ({ptype}):")
            label.grid(row=i, column=0)
            entry = tk.Entry(filter_frame)
            entry.grid(row=i, column=1)
            dynamic_fields[pname] = {"label": label, "entry": entry, "type": ptype}

        submit()

    



    # treeview_frame = tk.Frame(app.content_frame, width=1)
    treeview_frame = tk.Frame(app.content_frame)

    treeview_frame.grid(row=2, column=0, sticky='NW', padx=5, pady=5, columnspan=2)


    def get_filters():
        filters = {
            "tool_type_id": tool_type_map[tool_type_var.get().split(':')[0]]['id'],
            "parameters": {}
        }
        for pname, field in dynamic_fields.items():
            val = field["entry"].get().strip()
            ptype = field["type"]

            if val == "":
                continue  # Skip empty values

            try:
                if ptype == "int":
                    val = int(val)
                elif ptype == "float":
                    val = float(val)
                # No conversion needed for "str"
            except ValueError:
                app.set_status(f"Invalid input for parameter '{pname}'")
                return

            filters["parameters"][pname] = val
        return filters
    

    def empty_treeview():
        for row in tree.get_children():
            tree.delete(row)
        tree["columns"] = ()
        tree["show"] = "headings"
        for col in tree["columns"]:
            tree.heading(col, text="")

    
    def get_tool_data(tool_type_id, tool_ids):
        tool_details = []
        used_param_keys = set()

        all_parameters = fetch(f"tool_parameters/by_tooltype/{tool_type_id}")
        all_param_keys = ([param["name"] for param in all_parameters])

        

        for tid in tool_ids:
            data = fetch(f"/tool_detail/{tid}")
            tool_details.append(data)
            used_param_keys.update(data["parameters"].keys())

        used_param_keys = [name for name in all_param_keys if name in used_param_keys]
        return used_param_keys, tool_details

    

    def submit(*args):
        
        filters = get_filters()

        tool_ids = post("/search_tools/", filters).json()


        if not tool_ids:
            app.set_status("Found no matching tools in DB")
        else:
            app.set_status(f"Found {len(tool_ids)} matching tools")

        empty_treeview()
        selected_tooltype = tool_type_map[tool_type_var.get()]
        used_param_keys, tool_details= get_tool_data(selected_tooltype['id'], tool_ids)

        columns = ["id", "name"] + (used_param_keys)

        # Set columns & headings
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())

        # Insert rows
        for data in tool_details:
            row = [data["id"], data["name"]]
            row += [data["parameters"].get(k, "") for k in (used_param_keys)]
            tree.insert("", tk.END, values=row)



        # auto resice columns
        tree.grid_remove()
        tree.grid(row=0, column=1)
        for col in columns:
            max_width = tkfont.Font().measure(col)
            for item in tree.get_children():
                cell = str(tree.set(item, col))
                cell_width = tkfont.Font().measure(cell)
                if cell_width > max_width:
                    max_width = cell_width
            tree.column(column=col, width=max_width + 10, stretch=False)


    # strategies = fetch("/strategies/")
    # strategy_dropdown['values'] = [f"{s['id']}: {s['name']}" for s in strategies]
    # strategy_dropdown.bind("<<ComboboxSelected>>", populate_filters)


    tree = ttk.Treeview(treeview_frame, columns=("ID",), show='headings')
    # scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=tree.yview)
    # tree.configure(yscrollcommand=scrollbar.set)
    # scrollbar.grid(row=0, column=0)
    tree['columns'] = ("ID",)
    tree.heading("ID", text="Recipe ID")
    tree.column("ID", anchor="w")
    tree.grid(row=0, column=1)

    def edit_selected_tool(*args):
        selected_rows = tree.selection()  # Returns a tuple of selected item IDs
        if len(selected_rows) == 1:
            item_data = tree.item(selected_rows[0])  # Returns a dictionary of attributes for first item
            id = item_data["values"][0]
            edit_tool_form.show_edit_tool_form(app, tool_id = id)
        elif len(selected_rows) > 1:
            app.set_status("Select only one entry to edit")
            return
        
    def delete_selected_tool(*args):
        tools_to_delete = []
        selected_rows = tree.selection()  # Returns a tuple of selected item IDs

        for row in selected_rows:
            item_data = tree.item(row)  # Returns a dictionary of attributes
            tools_to_delete.append(item_data['values'][0])

        if not tools_to_delete:
            return
        
        ok = messagebox.askokcancel("Confirm delete!", f"Permanently delete:{tools_to_delete}\nThis cannot be undone")
        if not ok:
            return

        for tool_id in tools_to_delete:
            ok = False
            recipes = fetch(f"/recipes_by_tool/{tool_id}")
            if recipes:
                ok = messagebox.askokcancel("Tool used!", f"Tool {tool_id} is used in recipes:\n{recipes}\nForce delete?\nThis will delete associated recipes.")
            else: ok = True

            if not ok:
                return
            
            response = delete(f"/tool/{tool_id}")
            if response:
                app.set_status(f"Deleted tool {tool_id}")
                submit()
            else: app.set_status(f"Error when deleting tool {tool_id}")
        



    tk.Button(button_frame, text="Search", command=submit, width=15).grid(row=0, column=0, pady=5)
    tk.Label(button_frame, text="Enter").grid(row=0, column=1)
    tk.Button(button_frame, text="Edit", command=edit_selected_tool, width=15).grid(row=1, column=0, pady=5)
    tk.Label(button_frame, text="E").grid(row=1, column=1)
    tk.Button(button_frame, text="Delete", command=delete_selected_tool, width=15).grid(row=2, column=0, pady=5)
    tk.Label(button_frame, text="Backspace").grid(row=2, column=1)



    tool_type_dropdown.bind("<<ComboboxSelected>>", update_fields)
    update_fields()
    keybinds.bind_key(app, "<Return>", submit)
    tree.bind("e", edit_selected_tool)
    tree.bind("<BackSpace>", delete_selected_tool)
    tree.bind("<Delete>", delete_selected_tool)
    tree.bind("d", delete_selected_tool)


    tool_type_dropdown.focus_set()