import tkinter as tk
from tkinter import messagebox
from api import fetch, delete
from helper_func import keybinds, SmartTree
from screens.forms import edit_material_form


def show_material_search_form(app):
    keybinds.unbind_all(app)
    app.operation_label.config(text="Search Materials")
    app.clear_content()


    button_frame = tk.Frame(app.content_frame, padx=20)
    button_frame.grid(row=0, column=0)


    tree = SmartTree(app.content_frame)
    tree.grid(row=1, column=0, sticky='NW', padx=5, pady=5)


    def get_materials(*args):
        tree.empty()

        materials = fetch("/materials/")
        if not materials:
            app.show_home()
            app.set_status("Found no materials in DB")
            return

        columns = ["id", "name", "comment"]

        tree.write(materials, columns=columns)


    def edit_selected_material(*args):
        selected_rows = tree.selection()  # Returns a tuple of selected item IDs
        if len(selected_rows) == 1:
            item_data = tree.item(selected_rows[0])  # Returns a dictionary of attributes for first item
            id = item_data["values"][0]
            edit_material_form.show_edit_material_form(app, material_id=id)

        elif len(selected_rows) > 1:
            app.set_status("Select only one entry to edit")
            return

    def delete_selected_material(*args):
        materials_to_delete = []
        selected_rows = tree.selection()  # Returns a tuple of selected item IDs

        for row in selected_rows:
            item_data = tree.item(row)  # Returns a dictionary of attributes
            materials_to_delete.append(item_data['values'][0])

        if not materials_to_delete:
            return

        ok = messagebox.askokcancel("Confirm delete!", f"Permanently delete:{materials_to_delete}\nThis cannot be undone")
        if not ok:
            return

        for material_id in materials_to_delete:
            ok = False
            recipes = fetch(f"/recipes_by_material/{material_id}")
            if recipes:
                ok = messagebox.askokcancel("Tool used!", f"Material {material_id} is used in recipes:\n{recipes}\nForce delete?\nThis will delete associated recipes.")
            else:
                ok = True

            if not ok:
                return

            response = delete(f"/materials/{material_id}")
            if response:
                app.set_status(f"Deleted material {material_id}")
                get_materials()
            else:
                app.set_status(f"Error when deleting material {material_id}")



    tk.Button(button_frame, text="Search", command=get_materials, width=15).grid(row=0, column=0, pady=5)
    tk.Label(button_frame, text="Enter").grid(row=0, column=1)
    tk.Button(button_frame, text="Edit", command=edit_selected_material, width=15).grid(row=1, column=0, pady=5)
    tk.Label(button_frame, text="E").grid(row=1, column=1)
    tk.Button(button_frame, text="Delete", command=delete_selected_material, width=15).grid(row=2, column=0, pady=5)
    tk.Label(button_frame, text="Backspace").grid(row=2, column=1)

    get_materials()

    keybinds.bind_key(app, "<Return>", get_materials)
    tree.bind("e", edit_selected_material)
    tree.bind("<BackSpace>", delete_selected_material)
    tree.bind("<Delete>", delete_selected_material)
    tree.bind("d", delete_selected_material)

    tree.focus_set()
