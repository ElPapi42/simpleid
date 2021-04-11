import pytest
import itertools
from time import sleep
from multiprocessing import Process, Queue
from multiprocessing.queues import Empty

from source import SimpleId


def sids_factory(n):
    """
    Generate n SimpleIds.

    Returns a list of string representations
    of the generated sids for convinience
    """
    return [str(SimpleId()) for _ in range(n)]

def generate_sids_process(n, q):
    """
    Will be used on multiprocessing tests.

    Will put the sids on supplied queue
    """
    sids = sids_factory(n)

    q.put(sids)

def test_collision_single_0():
    """
    This test ensures sids work with
    100% reliability on a single logical
    node environment.
    """
    qty = 1000000

    # Generate list of ids
    sids = sids_factory(qty)

    sids_no_dupl = list(dict.fromkeys(sids))

    assert len(sids) == len(sids_no_dupl)

@pytest.mark.slow
def test_collision_multi_0():
    """
    This test ensures sids work with 
    100% reliability on a distirbuted 
    environment of multiple logical nodes.
    """
    logical_nodes = 1000
    sids_per_node = 100000

    queue = Queue()

    procs = []
    for _ in range(logical_nodes):
        proc = Process(
            target=generate_sids_process,
            args=(sids_per_node, queue)
        )
        proc.start()
        procs.append(proc)

    results = []
    while True:
        try:
            result = queue.get(timeout=1)
        except Empty:
            break

        results.append(result)

    # Flatten output resulting in list of sids generated
    sids = list(itertools.chain.from_iterable(results))

    # Get unique sids
    sids_no_dupl = list(dict.fromkeys(sids))

    assert len(sids) == len(sids_no_dupl)

def test_max_size_is_64():
    sid = SimpleId()
    sid = str(sid)

    assert len(sid) == 19
