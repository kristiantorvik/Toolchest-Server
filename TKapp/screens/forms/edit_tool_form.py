import tkinter as tk
from api import fetch, patch
from helper_func import keybinds

def show_edit_tool_form(app, **kwargs):
    keybinds.unbind_all(app)
    app.operation_label.config(text="Edit Tool")
    app.clear_content()


    tool_id = tk.StringVar(value="")
    tool_name = tk.StringVar(value="")
    dynamic_frame = tk.Frame(app.content_frame)
    dynamic_frame.grid(row=1, column=0, columnspan=2)

    # Dynamic parameter fields
    dynamic_fields = {}

    def clear_fields():
        for widgets in dynamic_fields.values():
            widgets["label"].destroy()
            widgets["entry"].destroy()
        dynamic_fields.clear()
        dynamic_frame.grid_forget()


    def update_fields(*args):
        id = tool_id.get()
        try:
            id = int(id)
        except ValueError:
            return
        except Exception as e:
            print(f"Unknown error: {e}")
            return
        finally:
            clear_fields()

        tool = fetch(f"/tool_detail/{id}")
        if not tool:
            app.set_status(f"No tool found with id {id}")
            clear_fields()
            return
        
        used_tool_params = fetch(f"/tools/{id}/parameters")
        all_tool_params = fetch(f"/tool_parameters/by_tooltype/{tool['tool_type_id']}")
        
        tool_name.set(tool['name'])
        app.set_status("")
        dynamic_frame.grid(row=1, column=0, columnspan=2, pady=20)

        tk.Label(dynamic_frame, text="Tool Name:").grid(row=0, column=0)
        name_entry = tk.Entry(dynamic_frame, textvariable=tool_name)
        name_entry.grid(row=0, column=1)
        

        for i, param in enumerate(all_tool_params):
            pname, ptype, pid, value = param["name"], param["type"], param['id'], ""
            for param in used_tool_params:
                if param.get('name') == pname:
                    value = param.get('value')

            label = tk.Label(dynamic_frame, text=f"{pname} ({ptype}):")
            label.grid(row=1 + i, column=0)
            entry = tk.Entry(dynamic_frame)
            entry.insert(0,value)
            entry.grid(row=1 + i, column=1)
            dynamic_fields[pname] = {"label": label, "entry": entry, "type": ptype, "id": pid}


    if 'tool_id' in kwargs:
        tool_id.set(kwargs['tool_id'])
        update_fields()

    # UI layout
    tk.Label(app.content_frame, text="Tool ID:").grid(row=0, column=0)
    id_entry = tk.Entry(app.content_frame, textvariable=tool_id)
    id_entry.grid(row=0, column=1)

    tool_id.trace_add(mode='write', callback=update_fields)

    def check_input(value, ptype):
        if ptype == "int":
            try: val = int(value)
            except ValueError:
                app.set_status("Invalid input")
                return None
            except Exception as e:
                app.set_status(f"Unknown error: {e}")
                return None

        elif ptype == "float":
            try: val = float(value)
            except ValueError:
                app.set_status("Invalid input")
                return None
            except Exception as e:
                app.set_status(f"Unknown error: {e}")
                return None
        else:
            val = value
        return val


    def submit(*args):
        tool_data = {
            "id": tool_id.get(),
            "name": tool_name.get(),
            "parameters": {}
        }

        for pname, info in dynamic_fields.items():
            value = info['entry'].get()
            ptype = info['type']
            id = info['id']

            if value == "": pass
            else: value = check_input(value, ptype)
                
            tool_data['parameters'][id] = value


        response = patch("/tool/", tool_data)
        if response.status_code == 200:
            app.set_status("Tool added!")
            app.show_home()
        else:
            app.set_status(f"Error {response.status_code}")


    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=2, column=0, columnspan=2, pady=20)
    keybinds.bind_key(app, "<Return>", submit)
    id_entry.focus_set()


