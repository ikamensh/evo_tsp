from RouteUnit import RouteUnit
from siman.visualize_sa import plotTSP

from City import cities

from typing import Tuple

def hill_climb(route: RouteUnit) -> Tuple[RouteUnit, bool]:
    distance = route.distance()
    print(f'Starting hillclimb with distance {distance}')
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
                    min_route = new_route
                    distance = new_distance
                    found_better = True

    print(f'Calculated new distance {distance}')
    return min_route, not found_better

from siman.launch_sa import sa

# route = RouteUnit(sa.cur_solution)
route = RouteUnit.createRoute(cities)
done = False
while not done:
    route, done = hill_climb(route)

plotTSP([route.route], save_to=f"hill_climb_{route.distance():.4f}.png")




