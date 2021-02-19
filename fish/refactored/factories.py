from typing import Type
from clients import FishClient
import interfaces

# this needs to be separate from the classes it creates or uses
# notice we don't import the concrete (non-abstract) classes
# we only need their interfaces to make mypy happy


def fish_factory(fish_class: Type[interfaces.Fish], client=None):
    """Notice, we expect the second parameter to be a fully
    instantiated class instance."""
    return fish_class(client or FishClient())
