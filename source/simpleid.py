from typing import Union


class SimpleId():
    """Value object that represent a 64bits integer id."""

    value:int

    def __init__(self, sid:Union[str, int, None]=None):
        self.value = 9999999999999999999

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)
