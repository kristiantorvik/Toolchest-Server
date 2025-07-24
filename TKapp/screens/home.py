import tkinter as tk
from screens.forms import material_form, strategy_form, tooltype_form, tool_form, recipe_form, search_form, tool_search_form, edit_material_form, material_search_form, edit_tool_form, edit_recipe_form, edit_tooltype_form
from helper_func import keybinds


def show_home(app):
    keybinds.unbind_all(app)
    keybinds.bind_key(app, "q", app.kill_bill)
    keybinds.bind_key(app, "Q", app.kill_bill)
    app.content_frame.columnconfigure(0, weight=1)
    app.content_frame.columnconfigure(1, weight=1)
    app.content_frame.columnconfigure(2, weight=1)


    add_buttons = [
        ("Add Material", lambda *args: material_form.show_material_form(app)),
        ("Add Tool Type", lambda *args: tooltype_form.show_tooltype_form(app)),
        ("Add Strategy", lambda *args: strategy_form.show_strategy_form(app)),
        ("Add Tool", lambda *args: tool_form.show_tool_form(app)),
        ("Add Recipe", lambda *args: recipe_form.show_recipe_form(app)),
    ]

    search_buttons = [
        ("Recipe", lambda *args: search_form.show_search_form(app)),
        ("Tools", lambda *args: tool_search_form.show_tool_search_form(app)),
        ("Material", lambda *args: material_search_form.show_material_search_form(app))
    ]

    edit_buttons = [
        ("Edit Material", lambda *args: edit_material_form.show_edit_material_form(app)),
        ("Edit Tool", lambda *args: edit_tool_form.show_edit_tool_form(app)),
        ("Edit Recipe", lambda *args: edit_recipe_form.show_edit_recipe_form(app)),
        ("Edit Tool Type", lambda *args: edit_tooltype_form.show_edit_tooltype_form(app)),
        ("Edit Strategy", lambda *args: strategy_form.show_strategy_form(app)),
    ]


    add_frame = tk.Frame(app.content_frame)
    add_frame.grid(row=0, column=0, sticky="N", padx=5)
    tk.Label(add_frame, text="Add to DB").grid(row=0, column=0, columnspan=2)

    for idx, (text, command) in enumerate(add_buttons):
        tk.Label(add_frame, text=f"{idx}").grid(row=idx + 1, column=0)
        tk.Button(add_frame, text=text, command=command, width=25, height=2).grid(row=idx + 1, column=1, pady=10)
        keybinds.bind_key(app, f"{idx}", command)


    search_frame = tk.Frame(app.content_frame)
    search_frame.grid(row=0, column=1, sticky="N", padx=5)
    tk.Label(search_frame, text="Search DB").grid(row=0, column=0, columnspan=2)

    for idx, (text, command) in enumerate(search_buttons):
        tk.Label(search_frame, text=f"{idx + len(add_buttons)}").grid(row=idx + 1, column=0)
        tk.Button(search_frame, text=text, command=command, width=25, height=2).grid(row=idx + 1, column=1, pady=10)
        keybinds.bind_key(app, f"{idx + len(add_buttons)}", command)


    edit_frame = tk.Frame(app.content_frame)
    edit_frame.grid(row=0, column=2, sticky="N", padx=5)
    tk.Label(edit_frame, text="Edit DB").grid(row=0, column=0)

    for idx, (text, command) in enumerate(edit_buttons):
        tk.Button(edit_frame, text=text, command=command, width=25, height=2).grid(row=idx + 1, column=0, pady=10)
