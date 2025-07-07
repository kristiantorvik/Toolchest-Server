import tkinter as tk
from api import fetch, patch
from helper_func import keybinds

def show_edit_material_form(app, **kwargs):
    app.operation_label.config(text="Edit Material")
    app.clear_content()
    keybinds.unbind_all(app)

    material_id = tk.StringVar(value="")
    material_name = tk.StringVar(value="")
    material_comment = tk.StringVar(value="")

    def fetch_material(*args):
        id = material_id.get()
        try:
            id = int(id)
        except ValueError:
            clear_boxes()
            return
        except Exception as e:
            print(f"Unknown error: {e}")
            clear_boxes()
            return
        
        material = fetch(f"/materials/by_id/{id}")
        if not material:
            app.set_status(f"No material found with id {id}")
            clear_boxes()
            return
        material_name.set(material['name'])
        material_comment.set(material['comment'])
        app.set_status("")


    def clear_boxes():
        material_name.set("")
        material_comment.set("")


    if 'material_id' in kwargs:
        material_id.set(kwargs['material_id'])
        fetch_material()

    tk.Label(app.content_frame, text="Material ID:").grid(row=0, column=0)
    id_entry = tk.Entry(app.content_frame, textvariable=material_id)
    id_entry.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Material Name:").grid(row=1, column=0)
    name_entry = tk.Entry(app.content_frame, textvariable=material_name)
    name_entry.grid(row=1, column=1)

    tk.Label(app.content_frame, text="Comment:").grid(row=2, column=0)
    comment_entry = tk.Entry(app.content_frame, textvariable=material_comment)
    comment_entry.grid(row=2, column=1)


    material_id.trace_add(mode="write", callback=fetch_material)




    def submit(*args):
        data = {
            "id": id_entry.get(),
            "name": name_entry.get(),
            "comment": comment_entry.get()
        }

        response = patch("materials/", data)
        if response.status_code == 200:
            app.set_status("Material updated")
        else:
            app.set_status(f"Error {response.status_code}")


    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=20)
    keybinds.bind_key(app, "<Return>", submit)
    if 'material_id' in kwargs: name_entry.focus_set()
    else: id_entry.focus_set()

    
