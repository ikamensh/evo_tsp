from RouteUnit import RouteUnit


def hill_climb(route):
    distance = route.routeDistance()
    print(f'Starting hillclimb with distance {distance}')
    min_route = []

    for row, city_a in enumerate(route.route):
        for col, city_b in enumerate(route.route):
            if row != col:
                new_route = RouteUnit(route.route)
                new_route.route[row] = city_b
                new_route.route[col] = city_a
                new_distance = new_route.routeDistance()
                if new_distance < distance:
                    min_route = new_route
                    distance = new_distance

    print(f'Calculated new distance {distance}')
    return min_route, not bool(min_route)

