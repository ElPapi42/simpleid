from time import time, time_ns
from os import getpid
from typing import Union
from threading import Lock
from struct import pack
from random import randint


class SimpleId(object):
    """Value object that represent a 64bits integer id."""

    _pid = None
    _inc = randint(0, 1000)
    _inc_lock = Lock()

    __random = None

    def __init__(self, value:Union[str, int, None]=None):
        self._value:int = self._generate()
    
    @classmethod
    def _random(cls):
        """Random int once per process."""
        pid = getpid()
        if pid != cls._pid:
            cls._pid = pid
            cls.__random = randint(0, 1000)
        return cls.__random

    def _generate(self):
        # Timestamp
        output = int(time() * 1000)

        # Space for process random id
        output *= 1000

        # Process random id
        output += SimpleId._random()

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
