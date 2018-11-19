from City import cities
from RouteUnit import RouteUnit
from siman.visualize_sa import plot_route
from siman.simulated_annealing import SimAnneal


def annealed_solution() -> RouteUnit:
    sa = SimAnneal(cities, alpha=1 - 1e-3)
    sa.anneal()
    return RouteUnit(sa.best_solution)


if __name__ == "__main__":
    sa = SimAnneal(cities, alpha=1-1e-3)

    solution = sa.initial_solution()
    print( sa.cur_fitness )
    plot_route([solution], save_to=f"nearest_neighbour_{RouteUnit.route_distance(sa.cur_solution):.4f}.png")


    sa.anneal()
    better_solution = sa.best_solution
    print(sa.best_fitness)

    plot_route([better_solution], save_to=f"sim_annealing_{min(solutions.keys()):.4f}.png")

# solutions = {}
# for i in range(50):
#     sa = SimAnneal(cities, alpha=1 - 5e-4)
#     sa.anneal()
#     solutions[sa.best_fitness] = sa.best_solution
#
#
# print(solutions.keys())
# print(min(solutions.keys()))
#
# plotTSP([solutions[min(solutions.keys())]], save_to=f"sim_annealing_{min(solutions.keys()):.4f}.png")
#
#
# # sa = SimAnneal(cities, alpha=1 - 1e-3)
# # sa.anneal()
# # # solutions[sa.best_fitness] = sa.best_solution
# # for i in range(19):
# #     sa = SimAnneal(cities, alpha=1 - 1e-3, initial_solution=sa.best_solution)
# #     sa.anneal()
# #     # solutions[sa.best_fitness] = sa.best_solution
# #
# # print(sa.best_solution)



