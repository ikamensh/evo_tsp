import time
import random
from RouteUnit import RouteUnit

def _random_search(cities, epochs):

    shortest_route = RouteUnit(random.sample(cities, len(cities)))
    min_length = shortest_route.distance()

    for epoch in range(epochs):
        route = RouteUnit(random.sample(cities, len(cities)))
        length = route.distance()
        if length < min_length:
            shortest_route = route
            min_length = length

    return shortest_route

def random_search(cities, time_limit):
    return _random_search(cities, epochs=100)




