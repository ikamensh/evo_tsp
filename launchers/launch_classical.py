from time import time
import RouteUnit
from ga_utils.draw_route import plot_route
from ga_utils.ploting import problem_tag

def run_with_time_limit(solution_fn, cities, time_limit, name):
    t = time()

    solutions = {}

    while time() - t < time_limit:
        solution: RouteUnit = solution_fn(cities, time_limit)
        solutions[solution.distance()] = solution

    best_fitness = min( solutions.keys() )

    best = solutions[best_fitness]

    plot_route([ best ],
               save_to= (f"plots/{problem_tag(cities)}", f"{name}_{best_fitness:.4f}.png") )

from classical.hillclimb import run_hillclimb
from classical.sim_anneal import annealed_solution, nearest_neighbour_solution
from classical.rand_search import random_search

methods = {run_hillclimb: "Hillclimbing",
           annealed_solution: "Sim Annealing",
           nearest_neighbour_solution: "Nearest Neighbour",
           random_search: "Random Search"}


def run_all(cities, time_limit):
    for method, name in methods.items():
        run_with_time_limit(method, cities, time_limit, name)