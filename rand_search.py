import time
import random
from RouteUnit import RouteUnit


def random_search(cities, epochs):
    print('\nHillclimbing starting....')
    start_time = time.time()

    num_cities = len(cities)

    def create_route():
        all_cities = cities[:]
        route = []
        for i in range(num_cities):
            choice = random.choice(all_cities)
            route.append(choice)
            all_cities.remove(choice)
        return route

    shortest_route = 0
    min_length = 99

    for epoch in range(epochs):
        route = RouteUnit(create_route())
        length = route.routeDistance()
        if length < min_length:
            shortest_route = route
            min_length = length
            print(f'Epoch: {epoch:8} min.length: {min_length}')

    print(f'Time: {time.time() - start_time} seconds')
