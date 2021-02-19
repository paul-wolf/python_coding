Class Design Example
====================

We take an example of an application that calls a service to get fisheries data.
The following code should run fine. It will print out common names of species. 

You can find all the source code for this chapter `here. <https://github.com/paul-wolf/python_coding/tree/main/fish>`_


.. code:: python

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

It is a common way for developers to write the first version of a
class. It has various features that give it the appearance of flexibility:

* It lets the caller customise the url, allowing the called service to be changed if required

* It has separate methods for getting data vs notifying the UI or formatting that data

* The field in the returned data can be customised easily

However, there are some big drawbacks: 

* To write an application, we'd spend a lot of time inside this class, firstly studying it to determine its behaviour and then re-writing to accommodate different behaviours

* It has to be modified directly rather than extended to achieve different behaviour. That's bad (see SOLID).

* It does a *lot* of things: acquiring state, notifying the UI, formatting in a specific way

Any attempt to build on this class while retaining the basic structure will
result in a mess of unreadable, hard-to-manage code. 

Refactored Fisheries Example
----------------------------

We can refactor everything to be vastly more flexible and easier to maintain and especially easier to test. Firstly, we'd create files to hold code that separates concerns:

* notifiers.py: this has code to notify 
* clients.py: this has code to get state data from local or remote sources
* interfaces.py: this defines object types we need to instantiate that follow the protocol we want
* factories.py: this creates objects according to protocols we want
* formatters.py: this formats data in ways we need for different application purposes
* fish.py: this holds domain manager objects

In our application source, ``fisheries.py``, which might be a view function, we'll import all the tools we've created:

.. code:: python

    import notifiers
    import clients
    import factories
    import formatters
    import fish

Now we can start doing various application tasks. This code is the fastest changing, least essential code:


.. code:: python

    fish_genera = factories.fish_factory(fish.FishGenera, client=clients.FishClientFile())

    # Iterate the genera and report to the user interface via web sockets
    for data in fish_genera:
        notifiers.FishUINotifier().notify(
            formatters.get_formatted_fish(data, lambda f: f"This is the genus name: {f}")
        )

We do all the mixing and matching of tools here. See the example source code, which you can also run:

`<https://github.com/paul-wolf/python_coding/tree/main/fish>`_

