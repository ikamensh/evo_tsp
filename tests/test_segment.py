from solutions.Segment import Segment
from pytest import fixture

@fixture()
def std_segment(cities):
    subset = cities[:len(cities) // 2]
    seg = Segment.from_list(subset, cities)
    return seg


def test_mutate_dominance():
    seg = Segment({},[])
    dom_before = seg.dominance
    seg.change_dominance()

    assert seg.dominance != dom_before

def test_construction(std_segment, cities):

    assert cities[0] in std_segment.from_to
    assert std_segment.from_to[cities[0]] is cities[1]

def test_mutation(monkeypatch):

    seg = Segment({},[])
    n_mutations = []

    monkeypatch.setattr( seg, "_mutate", lambda x: n_mutations.append(x))

    for _ in range(1000):
        seg.mutate(0.5)

    from collections import Counter

    ctr = Counter(n_mutations)

    assert -1 not in ctr
    assert ctr[0] > 10 # expected 500 zeros
    assert ctr[1] > 5 # expected 250
    assert ctr[3] > 0 # expected 62.5
    assert 100 not in ctr # expected 1000 / 2**100

def test_del_mutation(std_segment):
    keys_before = list(std_segment.from_to.keys())
    std_segment.del_mutation()

    assert len(std_segment.from_to.keys()) < len(keys_before)

def test_new_segm_mutation(std_segment):

    keys_before = list(std_segment.from_to.keys())
    std_segment.new_segm_mutation()
    assert len(std_segment.from_to.keys()) >= len(keys_before)


def test_new_dest_mutation(std_segment):
    keys_before = list(std_segment.from_to.keys())
    std_segment.change_dest_mutation()
    assert len(std_segment.from_to.keys()) == len(keys_before)


def test_new_dept_mutation(std_segment):
    keys_before = list(std_segment.from_to.keys())
    std_segment.change_dep_mutation()
    assert len(std_segment.from_to.keys()) <= len(keys_before)

def test_crossover(std_segment):
    new_segm = std_segment.crossover(std_segment)
    assert isinstance(new_segm, Segment)
    assert new_segm.dominance == std_segment.dominance

