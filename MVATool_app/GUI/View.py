from GUI.MVAQWidget import MVAQWidget


class View():

    def __init__(self, parent=None):
        self._window = MVAQWidget(parent=parent)

    def connect_to_close(self, func):
        self._window.close_signal.connect(func)

    def connect_to_resize(self, func):
        self._window.resize_signal.connect(func)