import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont



class __keybinding:
    def __init__(self):
        self.bindings = []

    def bind_key(self, app, event_type, callback):
        app.root.bind(event_type, callback)
        self.bindings.append(event_type)

    def unbind_all(self, app):
        for event_type in self.bindings:
            app.root.unbind(event_type)
        self.bindings.clear()


keybinds = __keybinding()


class __validation:
    def __init__(self):
        pass

    def check_input(self, value, ptype):
        if ptype == "int":
            try:
                val = int(value)
            except ValueError:
                return None, False
            except Exception:
                return None, False

        elif ptype == "float":
            try:
                val = float(value)
            except ValueError:
                return None, False
            except Exception:
                return None, False
        else:
            val = value
        return val, True


validate = __validation()


class SmartTree(tk.Frame):
    '''A spesialiced ttk.Treeview with extra functionality'''

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.tree = ttk.Treeview(self, show="headings")
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="NS")
        self.tree.grid(row=0, column=0)


    def bind(self, *args, **kwargs):
        self.tree.bind(*args, **kwargs)


    def write(self, json_data, columns=None):
        '''Sets and builds the rows & columns and rezices the columns'''
        self.empty()

        if not json_data:
            return
        if columns is None:
            columns = list(json_data[0].keys())

        self.tree["columns"] = columns

        for col in columns:
            name = col.replace("_", " ")
            self.tree.heading(col, text=name.title(), command=lambda c=col: self.__sort(c, False))

        for data in json_data:
            row = [data.get(k, "") for k in (columns)]
            self.tree.insert("", tk.END, values=row)

        self.__resize_columns()


    def selection(self):
        return self.tree.selection()


    def item(self, *args, **kwargs):
        return self.tree.item(*args, **kwargs)


    def get_selected(self):
        """Returns the values of the selected row as a dict"""
        selected = self.tree.selection()
        if not selected:
            return None
        item = selected[0]
        values = self.tree.item(item, 'values')
        return dict(zip(self.tree["columns"], values))



    def __is_floatable(self, value):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False


    def __sort(self, col, reverse):
        # Extract values
        values = [self.tree.set(k, col) for k in self.tree.get_children('')]

        # Determine if all values are floatable
        all_numeric = all(self.__is_floatable(v) or v in (None, '') for v in values)

        if all_numeric:
            def sort_key(k):
                val = self.tree.set(k, col)
                try:
                    return float(val)
                except (ValueError, TypeError):
                    return float('-inf') if reverse else float('inf')
        else:
            def sort_key(k):
                val = self.tree.set(k, col)
                return str(val).lower() if val else ''

        data = sorted(self.tree.get_children(''), key=sort_key, reverse=reverse)

        for index, k in enumerate(data):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda c=col: self.__sort(c, not reverse))


    def __resize_columns(self):
        self.tree.grid_remove()
        self.tree.grid()

        if not self.tree.get_children():
            return

        for col in self.tree['columns']:
            max_width = tkfont.Font().measure(col)
            for item in self.tree.get_children():
                cell = str(self.tree.set(item, col))
                cell_width = tkfont.Font().measure(cell)
                if cell_width > max_width:
                    max_width = cell_width
            self.tree.column(column=col, width=max_width + 10, stretch=False)


    def empty(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.tree["columns"] = ()
        self.tree["show"] = "headings"
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")


class ScrollableFrame(ttk.Frame):
    '''Cutom frame/canvas that applies a scrollwheel binding to all children'''

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._bind_mousewheel()

    def _bind_mousewheel(self):
        # Bind mousewheel to all widgets inside scrollable_frame
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        widgets_to_bind = [self.scrollable_frame, self.canvas]
        for widget in widgets_to_bind:
            widget.bind_all("<MouseWheel>", on_mousewheel)
            widget.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Linux
            widget.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))   # Linux

        # Clean-up: remove bindings when widget is destroyed
        self.bind("<Destroy>", lambda e: self.unbind_all("<MouseWheel>"))
