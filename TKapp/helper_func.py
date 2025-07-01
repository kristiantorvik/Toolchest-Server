# from main import app

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