import tkinter as tk
from screens.forms import material_form, strategy_form, tooltype_form, tool_form, recipe_form, search_form

def show_home(app):
    buttons = [
        ("Add Material", lambda: material_form.show_material_form(app)),
        ("Add Tool Type", lambda: tooltype_form.show_tooltype_form(app)),
        ("Add Strategy", lambda: strategy_form.show_strategy_form(app)),
        ("Add Tool", lambda: tool_form.show_tool_form(app)),
        ("Add Recipe", lambda: recipe_form.show_recipe_form(app)),
        ("Search", lambda: search_form.show_search_form(app))

    ]
    for idx, (text, command) in enumerate(buttons):
        tk.Button(app.content_frame, text=text, command=command, width=30, height=2).grid(row=idx, column=0, pady=10)