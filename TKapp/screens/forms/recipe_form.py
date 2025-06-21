import tkinter as tk
from tkinter import messagebox, ttk
from api import fetch, post

def show_recipe_form(app):
    app.operation_label.config(text="Add Recipe")
    app.clear_content()

    materials = fetch("materials/")
    tools = fetch("tools/")
    strategies = fetch("strategies/")

    material_map = {m["name"]: m["id"] for m in materials}
    tool_map = {t["name"]: t["id"] for t in tools}
    strategy_map = {s["name"]: s["id"] for s in strategies}

    tk.Label(app.content_frame, text="Tool:").grid(row=0, column=0)
    combo_tool = ttk.Combobox(app.content_frame, values=list(tool_map.keys()))
    combo_tool.grid(row=0, column=1)

    tk.Label(app.content_frame, text="Material:").grid(row=1, column=0)
    combo_material = ttk.Combobox(app.content_frame, values=list(material_map.keys()))
    combo_material.grid(row=1, column=1)

    tk.Label(app.content_frame, text="Strategy:").grid(row=2, column=0)
    combo_strategy = ttk.Combobox(app.content_frame, values=list(strategy_map.keys()))
    combo_strategy.grid(row=2, column=1)

    tk.Label(app.content_frame, text="Cutting Speed:").grid(row=3, column=0)
    cutting_entry = tk.Entry(app.content_frame)
    cutting_entry.grid(row=3, column=1)

    tk.Label(app.content_frame, text="Feedrate FU:").grid(row=4, column=0)
    feed_entry = tk.Entry(app.content_frame)
    feed_entry.grid(row=4, column=1)

    tk.Label(app.content_frame, text="Cut Depth:").grid(row=5, column=0)
    depth_entry = tk.Entry(app.content_frame)
    depth_entry.grid(row=5, column=1)

    tk.Label(app.content_frame, text="Cut Width:").grid(row=6, column=0)
    width_entry = tk.Entry(app.content_frame)
    width_entry.grid(row=6, column=1)

    tk.Label(app.content_frame, text="Lifetime:").grid(row=7, column=0)
    life_entry = tk.Entry(app.content_frame)
    life_entry.grid(row=7, column=1)

    coolant_var = tk.IntVar()
    airblast_var = tk.IntVar()
    tk.Checkbutton(app.content_frame, text="Coolant", variable=coolant_var).grid(row=8, column=0)
    tk.Checkbutton(app.content_frame, text="Airblast", variable=airblast_var).grid(row=8, column=1)

    def submit():
        data = {
            "tool_id": tool_map[combo_tool.get()],
            "material_id": material_map[combo_material.get()],
            "strategy_id": strategy_map[combo_strategy.get()],
            "cutting_speed": float(cutting_entry.get()),
            "feedrate_fu": float(feed_entry.get()),
            "cut_depth": float(depth_entry.get()),
            "cut_width": float(width_entry.get()),
            "lifetime": int(life_entry.get()),
            "coolant": bool(coolant_var.get()),
            "airblast": bool(airblast_var.get())
        }
        response = post("recipes/", data)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Recipe Added!")
            app.show_home()
        else:
            messagebox.showerror("Error", f"Error {response.status_code}")

    tk.Button(app.content_frame, text="Submit", command=submit).grid(row=9, column=0, columnspan=2, pady=10)
