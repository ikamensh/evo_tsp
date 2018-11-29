from RouteUnit import RouteUnit
from classical.simulated_annealing import SimAnneal


def annealed_solution(cities, time_limit) -> RouteUnit:
    sa = SimAnneal(cities, alpha=1 - 1e-3)
    sa.anneal()
    return RouteUnit(sa.best_solution)

def nearest_neighbour_solution(cities, time_limit) -> RouteUnit:
    sa = SimAnneal(cities, alpha=1 - 1e-3)
    return RouteUnit(sa.cur_solution)








