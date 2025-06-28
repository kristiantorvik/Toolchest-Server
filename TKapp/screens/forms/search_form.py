import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from api import fetch, post
import tkinter.font as tkfont

def show_search_form(app):
    for widget in app.content_frame.winfo_children():
        widget.destroy()

    strategy_frame = tk.Frame(app.content_frame)
    strategy_frame.grid(row=0, column=0, sticky='NEW', padx=50, pady=10)
    tk.Label(strategy_frame, text="Strategy:").grid(row=0, column=0)

    strategy_var = tk.StringVar()
    strategy_dropdown = ttk.Combobox(strategy_frame, textvariable=strategy_var)
    strategy_dropdown.grid(row=0, column=1)

    listbox_frame = tk.Frame(app.content_frame)
    listbox_frame.grid(row=1, column=0, sticky='NEW', pady=10)

    material_frame = tk.Frame(listbox_frame)
    material_frame.grid(row=0, column=0, padx=10, pady=5)
    tooltype_frame = tk.Frame(listbox_frame)
    tooltype_frame.grid(row=0, column=1, padx=10, pady=5)
    tool_frame = tk.Frame(listbox_frame)
    tool_frame.grid(row=0, column=2, padx=10, pady=5)


    tk.Label(material_frame, text="Materials").grid(row=0, column=0)
    tk.Label(tooltype_frame, text="Tool Types").grid(row=0, column=0)
    tk.Label(tool_frame, text="Tools").grid(row=0, column=0)

    material_listbox = tk.Listbox(material_frame, selectmode=tk.MULTIPLE, exportselection=False)
    material_listbox.grid(row=1, column=0)
    tooltype_listbox = tk.Listbox(tooltype_frame, selectmode=tk.MULTIPLE, exportselection=False)
    tooltype_listbox.grid(row=1, column=0)
    tool_listbox = tk.Listbox(tool_frame, selectmode=tk.MULTIPLE, exportselection=False)
    tool_listbox.grid(row=1, column=0)

    treeview_frame = tk.Frame(app.content_frame, width=1)
    treeview_frame.grid(row=3, column=0, sticky='NW', padx=5, pady=5)


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
        strategy_id = strategy_var.get().split(':')[0]
        data = fetch(f"/search/options/{strategy_id}")
        filters.clear()
        filters.update(data)

        update_listbox(material_listbox, filters['materials'])
        update_listbox(tooltype_listbox, filters['tool_types'])
        update_listbox(tool_listbox, filters['tools'])

        nonlocal full_tool_list
        full_tool_list = filters['tools']

        tooltype_listbox.bind('<<ListboxSelect>>', update_tools)

    def submit():
        strategy_id = strategy_var.get().split(':')[0]
        materials = [material_listbox.get(i).split(':')[0] for i in material_listbox.curselection()]
        tooltypes = [tooltype_listbox.get(i).split(':')[0] for i in tooltype_listbox.curselection()]
        tools = [tool_listbox.get(i).split(':')[0] for i in tool_listbox.curselection()]

        payload = {
            "strategy_id": int(strategy_id),
            "material_ids": list(map(int, materials)),
            "tool_type_ids": list(map(int, tooltypes)),
            "tool_ids": list(map(int, tools)),
        }

        recipe_ids = post("/search/", payload).json()

        for row in tree.get_children():
            tree.delete(row)
        tree["columns"] = ()
        tree["show"] = "headings"
        for col in tree["columns"]:
            tree.heading(col, text="")

        if not recipe_ids:
            messagebox.showinfo("No Results", "No matching recipes found.")
            return

        first = fetch(f"/recipe_detail/{recipe_ids[0]}")
        columns = ["id", "material", "tool"] + list(first["parameters"].keys())

        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())

        for rid in recipe_ids:
            data = fetch(f"/recipe_detail/{rid}")
            row = [data["id"], data["material"], data["tool"]]
            row += [data["parameters"].get(k, "") for k in first["parameters"].keys()]
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


    tk.Button(strategy_frame, text="Search", command=submit).grid(row=0, column=2, padx=20)

    strategies = fetch("/strategies/")
    strategy_dropdown['values'] = [f"{s['id']}: {s['name']}" for s in strategies]
    strategy_dropdown.bind("<<ComboboxSelected>>", populate_filters)


    tree = ttk.Treeview(treeview_frame, columns=("ID",), show='headings')
    scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=0)
    tree['columns'] = ("ID",)
    tree.heading("ID", text="Recipe ID")
    tree.column("ID", anchor="w")
    tree.grid(row=0, column=1)
