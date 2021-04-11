from typing import Optional
from time import time, time_ns
from os import getpid, urandom
from secrets import randbits
from uuid import getnode
from typing import Union
from threading import Lock
from struct import pack
from random import Random, randint


class SimpleId(object):
    """Value object that represent a 64bits integer id."""

    __counter:Optional[int] = None
    __counter_lock = Lock()

    __logical_node:Optional[int] = None
    __logical_node_id:Optional[int] = None

    def __init__(self, value:Union[str, int, None]=None):
        self._value:int = self.generate()
    
    @classmethod
    def get_logical_node(cls):
        """
        Random id for machine-process pairs.

        A machine-process pair is
        also know as logical node.
        """
        # Get full integer representing logical node
        logical_node = int(f'{getnode()}{getpid()}')

        # New id if logical node not defined
        if logical_node != cls.__logical_node:
            cls.__logical_node = logical_node

            # Logical node id using the int representation as base
            cls.__logical_node_id = logical_node % 100000

        return cls.__logical_node_id
    
    @classmethod
    def get_counter(cls):
        """Increment ans return the internal counter."""
        # Init counter if requried
        if cls.__counter is None:
            cls.__counter = cls.get_logical_node() % 10000

        # Increment the counter
        with cls.__counter_lock:
            counter = (cls.__counter + 1) % 10000
            cls.__counter = counter

        return counter

    def generate(self):
        timestamp = int(time())

        process = SimpleId.get_logical_node()

        counter = SimpleId.get_counter()
        
        #print(timestamp, process, counter)

        return (timestamp * 1000000000) + (process * 10000) + (counter)

    def __repr__(self):
        return f'SimpleId({str(self._value)})'

    def __str__(self):
        return str(self._value)
