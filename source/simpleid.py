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
    _timestamp_precision:int = 100 # 1=second, 10=milisecond, 100=microsecond
    _max_counter:int = 10000
    _max_node_id:int = 1000

    __counter:Optional[int] = None
    __counter_lock = Lock()

    __logical_node:Optional[int] = None
    __logical_node_id:Optional[int] = None

    def __init__(self, value:Union[str, int, None]=None):
        self._value:int = self._generate()

    @classmethod
    def _get_logical_node(cls):
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
            cls.__logical_node_id = logical_node % cls._max_node_id

        return cls.__logical_node_id
    
    @classmethod
    def _get_counter(cls):
        """Increment ans return the internal counter."""
        # Init counter if requried
        if cls.__counter is None:
            cls.__counter = cls._get_logical_node() % cls._max_counter

        # Increment the counter
        with cls.__counter_lock:
            counter = (cls.__counter + 1) % cls._max_counter
            cls.__counter = counter

        return counter
    
    def _merge(self, timestamp, node, counter):
        """Merge the inputs into the final sid value."""
        # Creates enought space for the node
        # and counter to be added without
        # intersecting with timestamp digits
        ftimestamp = timestamp * SimpleId._max_node_id * SimpleId._max_counter

        # Creates enougth space for the counter
        # to be added safely to the node value
        fnode = node * SimpleId._max_counter

        return ftimestamp + fnode + counter

    def _generate(self):
        timestamp = int(time() * SimpleId._timestamp_precision)

        node = SimpleId._get_logical_node()

        counter = SimpleId._get_counter()

        print(timestamp, node, counter)

        return self._merge(timestamp, node, counter)

    def __repr__(self):
        return f'SimpleId({str(self._value)})'

    def __str__(self):
        return str(self._value)
