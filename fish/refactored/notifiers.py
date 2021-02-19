class DummyWebSocket:
    def notify(self, name):
        print(f"{self.__class__.__name__}: {name}")


class FishUINotifier:
    def __init__(self, websocket_interface=None):
        self.mwi = websocket_interface or DummyWebSocket()

    def notify(self, name_data):
        self.mwi.notify(name_data)  # side effect
