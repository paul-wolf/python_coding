from typing import Final
from abc import ABC, abstractmethod

# our interface, an abstract base class


class Fish(ABC):
    def __init__(self, client):
        self.client: Final = client
        self.data = None

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    def __iter__(self):
        self.get_data()
        return self
