from typing import Final
import os
import json
from urllib.parse import urljoin

import requests

import constants

# we could have an abstract base class called "Client"
# duck typing makes this work because it is so simple
# but a more complicated code base would benefit from
# interface definition


class FishClient:
    """We will call the remote service to get data on fish.

    This would handle much more in real life, like errors, retries, etc.

    """

    def __init__(self, url=None):
        self.base_url: Final = url or constants.BASE_URL

    def get_data(self, route):
        print(f"We got {route} data from {self.base_url}")
        return requests.get(urljoin(self.base_url, route)).json()


class FishClientFile:
    """Here is an alternative client that reads a json file
    from the local disk.
    """

    def __init__(self, url=None):
        self.base_url: Final = url or constants.BASE_URL

    def get_data(self, route):
        print(f"We got {route} data from local disk cache")
        with open(os.path.join(constants.DATA_DIR, f"{route}.json")) as f:
            return json.loads(f.read())
