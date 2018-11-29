from pytest import fixture
from City import City

@fixture()
def cities():
    return [City(2) for _ in range(50)]