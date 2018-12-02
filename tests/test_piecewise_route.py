from piecewise_route.PiecewiseRoute import PiecewiseRoute
from piecewise_route.Segment import Segment


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


def test_route(cities):
    subcities = cities[:4]
    c1, c2, c3, c4 = subcities
    seg1 = Segment({c1: c2, c2: c3, c3: c4}, subcities)
    route = PiecewiseRoute([seg1], subcities).to_route()

    assert route == [c1,c2,c3,c4]

    seg2 = Segment({c3: c2, c2: c1, c1: c4}, subcities)
    route = PiecewiseRoute([seg2], subcities).to_route()

    assert route == [c3, c2, c1, c4]


def test_dominance(cities):

    subcities = cities[:4]
    c1, c2, c3, c4 = subcities

    seg1 = Segment({c1:c2, c2:c3, c3:c4}, subcities, dominance=1)
    seg2 = Segment({c2:c4, c4:c3}, subcities, dominance=2)

    route = PiecewiseRoute([seg1, seg2], subcities).to_route()

    assert route == [c1, c2, c4, c3]


def test_souvereinity(cities):
    pwr1 = PiecewiseRoute.create_route(cities)
    pwr2 = PiecewiseRoute.create_route(cities)

    d1, d2 = pwr1.distance(), pwr2.distance()

    children = [pwr1.crossover(pwr2) for i in range(10)]
    for c in children:
        c.mutate(0.5)

    assert pwr1.distance() == d1
    assert pwr2.distance() == d2


