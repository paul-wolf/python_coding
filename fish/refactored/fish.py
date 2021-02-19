import interfaces

# Implement the interface in various ways depending on what we require


class FishGenera(interfaces.Fish):
    def get_data(self):
        self.data = self.client.get_data("genera")["data"]

    def __next__(self):
        if self.data:
            return self.data.pop()["GenName"]
        raise StopIteration


class FishSpecies(interfaces.Fish):
    def get_data(self):
        self.data = self.client.get_data("species")["data"]

    def __next__(self):
        if self.data:
            return self.data.pop()["Species"]
        raise StopIteration
