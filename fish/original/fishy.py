from urllib.parse import urljoin

import requests


class DummyWebSocket:
    def notify(self, name):
        print(f"{self.__class__.__name__}: {name}")


mwi = DummyWebSocket()

#  https://fishbaseapi.readme.io/docs


class Fish:
    FIELD_NAME = "GenName"

    def __init__(self, base_url):
        self.base_url = base_url
        self.name_template = "Common name: {}"

    def _get(self, path):
        """Return response from calling fish service."""
        return requests.get(urljoin(self.base_url, path))

    def format_data(self, name_data):
        return self.name_template.format(name_data)

    def get_common_names(self):
        response = []
        for data in self._get("genera").json()["data"]:
            response.append(self.format_data(data.get(self.FIELD_NAME)))
        return response

    def get_names_and_notify(self):
        for name in self.get_common_names():
            mwi.notify(name)


if __name__ == "__main__":
    fish = Fish("https://fishbase.ropensci.org/")
    print(fish.get_names_and_notify())
