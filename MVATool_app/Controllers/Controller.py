from GUI.View import View

class Controller:

    def __init__(self):
        self._view = View()

    def connect_to_close(self, func):
        self._view.connect_to_close(func)
