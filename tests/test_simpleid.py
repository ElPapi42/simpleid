import pytest
from dataclasses import FrozenInstanceError

from source import SimpleId


def test_instance_simpleid():
    sid = SimpleId()
    print(sid)
    assert True

def test_collision_0():
    qty = 1000000

    # Generate list of ids
    sids = [SimpleId().value for i in range(qty)]

    sids_no_dupl = list(dict.fromkeys(sids))

    assert len(sids) == len(sids_no_dupl)

def test_simpleid_is_inmutable():
    sid = SimpleId()

    try:
        sid.value = 0
    except AttributeError:
        return
    
    assert False
