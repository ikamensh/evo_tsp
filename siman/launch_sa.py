from City import City
from siman.visualize_sa import plotTSP


cities = [City(ndim=2) for i in range(60)]

from siman.simulated_annealing import SimAnneal

sa = SimAnneal(cities, alpha=1-1e-3)

# solution = sa.initial_solution()
# print( sa.cur_fitness )
# plotTSP([solution])

sa.anneal()
better_solution = sa.best_solution
print(sa.best_fitness)


solutions = {}
for i in range(50):
    sa = SimAnneal(cities, alpha=1 - 5e-4)
    sa.anneal()
    solutions[sa.best_fitness] = sa.best_solution


print(solutions.keys())
print(min(solutions.keys()))

plotTSP([solutions[min(solutions.keys())]], save_to=f"sim_annealing_{min(solutions.keys()):.4f}.png")


# sa = SimAnneal(cities, alpha=1 - 1e-3)
# sa.anneal()
# # solutions[sa.best_fitness] = sa.best_solution
# for i in range(19):
#     sa = SimAnneal(cities, alpha=1 - 1e-3, initial_solution=sa.best_solution)
#     sa.anneal()
#     # solutions[sa.best_fitness] = sa.best_solution
#
# print(sa.best_solution)



