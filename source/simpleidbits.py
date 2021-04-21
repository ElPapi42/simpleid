from typing import Optional
from os import getpid, urandom
from secrets import randbits
from uuid import getnode
from typing import Union
from threading import Lock
from struct import pack
from random import Random, randint

from time import time

from bitarray import bitarray
from bitarray.util import int2ba, urandom, ba2int


class SimpleId(object):
    """Value object that represent a 64bits integer id."""
    _timestamp_precision:int = 100 # 1=second, 10=milisecond, 100=microsecond
    _max_counter:int = 10000
    _max_node_id:int = 1000

    __counter:Optional[bitarray] = None
    __counter_lock = Lock()

    __logical_node:Optional[int] = None
    __logical_node_id:Optional[bitarray] = None

    def __init__(self, value:Union[str, int, None]=None):
        self._value:bitarray = self._generate()

    def _get_timestamp(self) -> bitarray:
        """Return the current timestamp as a bitarray."""
        return int2ba(int(time() * 100), length=42)

    @classmethod
    def _get_logical_node(cls) -> bitarray:
        """
        Id for machine-process pairs.

        A machine-process pair is
        also know as logical node.
        """
        # Get full integer representing logical node
        logical_node = getnode() + getpid()

        # New id if logical node no matching
        if logical_node != cls.__logical_node:
            cls.__logical_node = logical_node

            # Bitarray id using int repr
            cls.__logical_node_id = int2ba(
                logical_node % 2048,
                length=11
            )

        return cls.__logical_node_id
    
    @classmethod
    def _get_counter(cls) -> bitarray:
        """Increment and returns internal counter."""

        with cls.__counter_lock:
            # Init counter if required
            if cls.__counter is None:
                cls.__counter = urandom(length=11)

            # Get counter value
            counter = cls.__counter

            # Increment the counter
            shift = ba2int(cls.__counter) + 1
            shift = shift % 2048
            shift = int2ba(shift, length=11)
            cls.__counter = shift

        return counter

    def _generate(self) -> bitarray:
        timestamp = self._get_timestamp()

        node = SimpleId._get_logical_node()

        counter = SimpleId._get_counter()

        #print(timestamp, node, counter)

        return timestamp + node + counter

    def __repr__(self):
        return f'SimpleId({ba2int(self._value)})'

    def __str__(self):
        return str(ba2int(self._value))
