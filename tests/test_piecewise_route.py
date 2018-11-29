from piecewise_route.PiecewiseRoute import PiecewiseRoute
from piecewise_route.Segment import Segment


def test_missing_penalty(cities):
    for i in range(100):
        pwr = PiecewiseRoute.create_route(cities)

        fitness_before = pwr.fitness

        pwr.segments = [pwr.segments[0]]
        pwr._fitness = None

        assert fitness_before > pwr.fitness

def test_extremely_short(cities):
    pwr = PiecewiseRoute.create_route(cities)

    fitness_before = pwr.fitness

    pwr.segments = [pwr.segments[0]]
    pwr.segments[0].from_to = {k:v for k,v in pwr.segments[0].from_to.items() if k is list(pwr.segments[0].from_to.keys())[0]}
    pwr._fitness = None
    fitness_after = pwr.fitness

    assert fitness_before > fitness_after


def test_cyclic_dicts(cities):
    pwr = PiecewiseRoute.create_route(cities)
    dicts = [seg.from_to for seg in pwr.segments]

    for i, d in enumerate(dicts[:-1]):
        routes_end = list(d.values())[-1]
        next_route = dicts[i+1]
        next_start = list(next_route.keys())[0]
        assert routes_end is next_start

    last_route = dicts[-1]
    very_end = list(last_route.values())[-1]
    first_route = dicts[0]
    very_start = list(first_route.keys())[0]
    assert very_start is very_end


    def is_cyclic_dict(d):
        start = list(d.keys())[0]
        current = start
        try:
            for _ in range(len(d)):
                current = d[current]
        except KeyError:
            return False
        else:
            return current is start

    merged = {}
    for d in dicts:
        merged.update(d)

    assert is_cyclic_dict(merged)

def test_construction(cities):
    pwr = PiecewiseRoute.create_route(cities)
    route = pwr.to_route()

    assert len(pwr.segments) > 1
    assert len(route) == len(cities)
    for c in cities:
        ind = route.index(c)
        # No ValueError expected - all cities present

def test_missing_cities_low_fit(cities):

    s1 = Segment.from_list(cities, cities)
    s2 = Segment.from_list(cities[:len(cities)//2], cities)

    pwr1 = PiecewiseRoute([s1], cities)
    pwr2 = PiecewiseRoute([s2], cities)

    assert pwr1.fitness >= pwr2.fitness


def test_route(cities):
    c1, c2, c3, c4 = cities[:4]
    seg1 = Segment({c1: c2, c2: c3, c3: c4}, cities)
    route = PiecewiseRoute([seg1], cities).to_route()

    assert route == [c1,c2,c3,c4]

    seg2 = Segment({c3: c2, c2: c1, c1: c4}, cities)
    route = PiecewiseRoute([seg2], cities).to_route()

    assert route == [c3, c2, c1, c4]


def test_dominance(cities):

    c1, c2, c3, c4 = cities[:4]

    seg1 = Segment({c1:c2, c2:c3, c3:c4}, cities, dominance=1)
    seg2 = Segment({c2:c4, c4:c3}, cities, dominance=2)

    route = PiecewiseRoute([seg1, seg2], cities).to_route()

    assert route == [c1, c2, c4, c3]