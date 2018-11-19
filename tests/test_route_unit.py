from RouteUnit import RouteUnit
from City import City
import pytest


@pytest.fixture()
def cities():
    return [City(ndim=2) for _ in range(50)]


def test_hashing_set(cities):

    r1 = RouteUnit(cities)
    r2 = RouteUnit(cities)

    set_uniques = {r1, r2}

    assert len(set_uniques) == 1

    new_route = list(cities)
    new_route[2], new_route[5] = new_route[5], new_route[2]

    set_uniques.add( RouteUnit(new_route) )

    assert len(set_uniques) == 2

def test_permutations_equal(cities):

    r1 = RouteUnit(cities)

    shifted_cities = cities[len(cities)//2:] + cities[:len(cities)//2]

    r2 = RouteUnit(shifted_cities)

    set_uniques = {r1, r2}

    assert len(set_uniques) == 1




