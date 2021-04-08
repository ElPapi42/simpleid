from time import time
from uuid import getnode
from typing import Union
from threading import Lock


class SimpleId(object):
    """Value object that represent a 64bits integer id."""

    _inc = 1
    _inc_lock = Lock()

    def __init__(self, value:Union[str, int, None]=None):
        self._value:int = self._generate()

    def _generate(self):
        # Timestamp
        output = int(time())

        # Space for machine id
        output *= 100000

        # Machine id
        output += int(getnode() / 1000000000)

        # Space for algorith version
        output *= 10

        # Algorithm version
        output += 1

        # Space for increment
        output *= 1000

        with SimpleId._inc_lock:
            # Increment
            output += SimpleId._inc

            # Increment counter
            SimpleId._inc = (SimpleId._inc + 1) % 1000

        return output
    
    @property
    def value(self):
        return self._value

    def __repr__(self):
        return f'SimpleId({str(self._value)})'

    def __str__(self):
        return str(self._value)
