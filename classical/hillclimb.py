from solutions.RouteUnit import RouteUnit
from typing import Tuple

def _hill_climb(route: RouteUnit) -> Tuple[RouteUnit, bool]:
    distance = route.distance()
    min_route = route
    found_better = False

    for row, city_a in enumerate(route.route):
        for col, city_b in enumerate(route.route):
            if row != col:
                new_route = RouteUnit(route.route)
                new_route.route[row] = city_b
                new_route.route[col] = city_a
                new_distance = new_route.distance()
                if new_distance < distance:
                    return new_route, True

    return min_route, not found_better

import time

def run_hillclimb(cities, time_limit) -> RouteUnit:

    t = time.time()

    done = False
    route = RouteUnit.create_route(cities)

    while time.time() - t > time_limit and not done:
        route, done = _hill_climb(route)

    return route





