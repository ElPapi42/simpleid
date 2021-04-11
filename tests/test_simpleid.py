import pytest
import itertools
from multiprocessing import Pool

from source import SimpleId


def sids_factory(n):
    """
    Generate n SimpleIds.

    Returns a list of string representations
    of the generated sids for convinience
    """
    return [str(SimpleId()) for _ in range(n)]

def test_collision_0():
    """
    This test ensures sids work with
    100% reliability on a single logical
    node environment.
    """
    qty = 100000

    # Generate list of ids
    sids = sids_factory(qty)

    sids_no_dupl = list(dict.fromkeys(sids))

    assert len(sids) == len(sids_no_dupl)

def test_collision_multi_0():
    """
    This test ensures sids work with 
    100% reliability on a distirbuted 
    environment of multiple logical nodes.
    """
    logical_nodes = 100
    sids_per_node = 1000

    # Iterable with the amount of sids to create per node
    args = [sids_per_node for _ in range(logical_nodes)]

    # Generate ids distributed in multiple logical nodes
    with Pool(logical_nodes) as pool:
        results = pool.map(sids_factory, args)
    
    # Flatten output resulting in list of sids generated
    sids = list(itertools.chain.from_iterable(results))

    # Get unique sids
    sids_no_dupl = list(dict.fromkeys(sids))

    assert len(sids) == len(sids_no_dupl)
