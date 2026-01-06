import tkinter as tk
from tkinter import messagebox
from api import fetch, delete
from helper_func import keybinds, SmartTree
from screens.forms import edit_tooltype_form


def show_tooltype_search_form(app):
    keybinds.unbind_all(app)
    app.operation_label.config(text="Search ToolType")
    app.clear_content()


    button_frame = tk.Frame(app.content_frame, padx=20)
    button_frame.grid(row=0, column=0)


    tree = SmartTree(app.content_frame)
    tree.grid(row=1, column=0, sticky='NW', padx=5, pady=5)


    def get_tooltypes(*args):
        tree.empty()

        tooltypes = fetch("/tool_types/")
        if not tooltypes:
            app.show_home()
            app.set_status("Found no tooltypes in DB")
            return

        columns = ["id", "name", "comment"]

        tree.write(tooltypes, columns=columns)


    def edit_selected_tooltype(*args):
        selected_rows = tree.selection()  # Returns a tuple of selected item IDs
        if len(selected_rows) == 1:
            item_data = tree.item(selected_rows[0])  # Returns a dictionary of attributes for first item
            id = item_data["values"][0]
            edit_tooltype_form.show_edit_tooltype_form(app, tooltype_id=id)

        elif len(selected_rows) > 1:
            app.set_status("Select only one entry to edit")
            return

    def delete_selected_tooltype(*args):
        tooltypes_to_delete = []
        selected_rows = tree.selection()  # Returns a tuple of selected item IDs

        for row in selected_rows:
            item_data = tree.item(row)  # Returns a dictionary of attributes
            tooltypes_to_delete.append(item_data['values'][0])

        if not tooltypes_to_delete:
            return

        ok = messagebox.askokcancel("Confirm delete!", f"Permanently delete:{tooltypes_to_delete}\nThis cannot be undone")
        if not ok:
            return

        for tooltype_id in tooltypes_to_delete:
            ok = False
            tool_ids = fetch(f"/tools_by_tooltype/{tooltype_id}")
            if tool_ids:
                ok = messagebox.askokcancel("Tool used!", f"tooltype {tooltype_id} is used in tool_ids:\n{tool_ids}\nForce delete?\nThis will delete associated tool_ids.")
            else:
                ok = True

            if not ok:
                return

            response = delete(f"/tooltypes/{tooltype_id}")
            if response:
                app.set_status(f"Deleted tooltype {tooltype_id}")
                get_tooltypes()
            else:
                app.set_status(f"Error when deleting tooltype {tooltype_id}")



    tk.Button(button_frame, text="Search", command=get_tooltypes, width=15).grid(row=0, column=0, pady=5)
    tk.Label(button_frame, text="Enter").grid(row=0, column=1)
    tk.Button(button_frame, text="Edit", command=edit_selected_tooltype, width=15).grid(row=1, column=0, pady=5)
    tk.Label(button_frame, text="E").grid(row=1, column=1)
    tk.Button(button_frame, text="Delete", command=delete_selected_tooltype, width=15).grid(row=2, column=0, pady=5)
    tk.Label(button_frame, text="Backspace").grid(row=2, column=1)

    get_tooltypes()

    keybinds.bind_key(app, "<Return>", get_tooltypes)
    tree.bind("e", edit_selected_tooltype)
    tree.bind("<BackSpace>", delete_selected_tooltype)
    tree.bind("<Delete>", delete_selected_tooltype)
    tree.bind("d", delete_selected_tooltype)

    tree.focus_set()
