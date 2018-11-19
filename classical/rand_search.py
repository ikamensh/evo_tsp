import time
import random
from RouteUnit import RouteUnit
from utils.draw_route import plot_route

from City import cities


def random_search(cities, epochs):
    print('\nRandom search started....')
    start_time = time.time()

    shortest_route = RouteUnit(random.sample(cities, len(cities)))
    min_length = shortest_route.distance()

    for epoch in range(epochs):
        route = RouteUnit(random.sample(cities, len(cities)))
        length = route.distance()
        if length < min_length:
            shortest_route = route
            min_length = length
            print(f'Epoch: {epoch:8} min.length: {min_length}')

    print(f'Time: {time.time() - start_time} seconds')
    return shortest_route

best = random_search(cities, epochs=50000)
print(best.distance())

plot_route([best.route], save_to=f"300_random_search_{best.distance():.4f}.png")



