import pytest
from dataclasses import FrozenInstanceError

from source import SimpleId


def test_instance_objectid():
    sid = SimpleId()

    assert sid._value == 0

def test_simpleid_is_inmutable():
    sid = SimpleId()

    try:
        sid.value = 0
    except AttributeError:
        return
    
    assert False
