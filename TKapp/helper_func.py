class __keybinding:
    def __init__(self):
        self.bindings = []

    def bind_key(self, app, event_type, callback):
        app.root.bind(event_type, callback)
        self.bindings.append(event_type)
        # print(f"DEBUG: Added keybind for {event_type} for callback: {callback}")

    def unbind_all(self, app):
        for event_type in self.bindings:
            app.root.unbind(event_type)
            # print(f"DEBUG: Removed keybind for {event_type}")
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

