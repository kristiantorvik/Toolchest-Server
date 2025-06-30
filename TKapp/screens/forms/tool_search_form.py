import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from api import fetch, post
import tkinter.font as tkfont
from helper_func import keybinds


def show_tool_search_form(app):
    keybinds.unbind_all(app)
    app.operation_label.config(text="Search Tools")
    app.clear_content()

    tool_types = fetch("tool_types/")

    if not tool_types:
        app.set_status("No tool types in DB")
        app.show_home()
        return
    
    tool_type_map = {t["name"]: t for t in tool_types}
    tool_type_keys = list(tool_type_map.keys())

    tool_type_frame = tk.Frame(app.content_frame)
    tool_type_frame.grid(row=0, column=0, sticky='NEW', padx=50, pady=10)
    tk.Label(tool_type_frame, text="Tool Type:").grid(row=0, column=0)

    tool_type_var = tk.StringVar()
    tool_type_var.set(tool_type_keys[0])
    tool_type_dropdown = ttk.Combobox(tool_type_frame, textvariable=tool_type_var, state="readonly")
    tool_type_dropdown.grid(row=0, column=1)
    tool_type_dropdown['values'] = tool_type_keys

    filter_frame = tk.Frame(app.content_frame)
    filter_frame.grid(row=1, column=0)

    # Load tool types
    tooltypes = fetch("tool_types/")
    if not tooltypes:
        app.set_status("Please create Tool Types first!")
        app.show_home()
        return

    
    # Dynamic parameter fields
    dynamic_fields = {}

    def update_fields(*args):
        # Clear old fields
        for widgets in dynamic_fields.values():
            widgets["label"].destroy()
            widgets["entry"].destroy()
        dynamic_fields.clear()

        selected_tooltype = tool_type_map[tool_type_var.get()]
        parameters = fetch(f"tooltype_parameters/{selected_tooltype['id']}")

        for i, param in enumerate(parameters):
            pname, ptype = param["name"], param["type"]
            label = tk.Label(filter_frame, text=f"{pname} ({ptype}):")
            label.grid(row=i, column=0)
            entry = tk.Entry(filter_frame)
            entry.grid(row=i, column=1)
            dynamic_fields[pname] = {"label": label, "entry": entry, "type": ptype}

    tool_type_var.trace("w", update_fields)
    update_fields()



    treeview_frame = tk.Frame(app.content_frame, width=1)
    treeview_frame.grid(row=1, column=0, sticky='NW', padx=5, pady=5)


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
        


    def submit(*args):
        
        filters = get_filters()

        tool_ids = post("/search_tools/", filters).json()

        print(tool_ids)

        app.set_status(f"Matching tools: {tool_ids}")

        # for row in tree.get_children():
        #     tree.delete(row)
        # tree["columns"] = ()
        # tree["show"] = "headings"
        # for col in tree["columns"]:
        #     tree.heading(col, text="")

        # if not recipe_ids:
        #     messagebox.showinfo("No Results", "No matching recipes found.")
        #     return



        # # Fetch all recipe details and collect their parameter keys
        # recipe_details = []
        # used_param_keys = set()

        # all_parameters = fetch(f"recipe_parameters/by_strategy/{strategy_id}")
        # all_param_keys = ([param["name"] for param in all_parameters])
        

        # for rid in recipe_ids:
        #     data = fetch(f"/recipe_detail/{rid}")
        #     recipe_details.append(data)
        #     used_param_keys.update(data["parameters"].keys())

        # used_param_keys = [name for name in all_param_keys if name in used_param_keys]

        # # Now build the final ordered column list:
        # columns = ["id", "material", "tool"] + (used_param_keys)

        # # Set columns & headings
        # tree["columns"] = columns
        # for col in columns:
        #     tree.heading(col, text=col.replace("_", " ").title())

        # # Insert rows
        # for data in recipe_details:
        #     row = [data["id"], data["material"], data["tool"]]
        #     row += [data["parameters"].get(k, "") for k in (used_param_keys)]
        #     tree.insert("", tk.END, values=row)



        # # auto resice columns
        # tree.grid_remove()
        # tree.grid(row=0, column=1)
        # for col in columns:
        #     max_width = tkfont.Font().measure(col)
        #     for item in tree.get_children():
        #         cell = str(tree.set(item, col))
        #         cell_width = tkfont.Font().measure(cell)
        #         if cell_width > max_width:
        #             max_width = cell_width
        #     tree.column(column=col, width=max_width + 10, stretch=False)


    tk.Button(tool_type_frame, text="Search", command=submit).grid(row=0, column=2, padx=20)

    # strategies = fetch("/strategies/")
    # strategy_dropdown['values'] = [f"{s['id']}: {s['name']}" for s in strategies]
    # strategy_dropdown.bind("<<ComboboxSelected>>", populate_filters)


    # tree = ttk.Treeview(treeview_frame, columns=("ID",), show='headings')
    # scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=tree.yview)
    # tree.configure(yscrollcommand=scrollbar.set)
    # scrollbar.grid(row=0, column=0)
    # tree['columns'] = ("ID",)
    # tree.heading("ID", text="Recipe ID")
    # tree.column("ID", anchor="w")
    # tree.grid(row=0, column=1)


    # keybinds.bind_key(app, "<Return>", submit)
    tool_type_dropdown.focus_set()