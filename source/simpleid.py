from time import time, time_ns
from os import getpid
from typing import Union
from threading import Lock
from struct import pack
from random import randint


class SimpleId(object):
    """Value object that represent a 64bits integer id."""

    _pid = None
    _inc = randint(0, 100000)
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
        timestamp = int(time() * 10)

        process = SimpleId._random()

        with SimpleId._inc_lock:
            increment = SimpleId._inc

            # Increment counter
            SimpleId._inc = (SimpleId._inc + 1) % 100000

        return (timestamp * 100000000) + (process * 100000) + (increment)
    
    @property
    def value(self):
        return self._value

    def __repr__(self):
        return f'SimpleId({str(self._value)})'

    def __str__(self):
        return str(self._value)
