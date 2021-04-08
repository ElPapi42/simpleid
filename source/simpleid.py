from typing import Union


class SimpleId(object):
    """Value object that represent a 64bits integer id."""

    def __init__(self, value:Union[str, int, None]=None):
        self._value:int = self._generate()

    def _generate(self):
        return 9999999999999999999
    
    @property
    def value(self):
        return self._value

    def __repr__(self):
        return f'SimpleId({str(self._value)})'

    def __str__(self):
        return str(self._value)
