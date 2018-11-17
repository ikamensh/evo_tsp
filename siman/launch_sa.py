from City import City
from siman.visualize_sa import plotTSP


cities = [City(ndim=2) for i in range(60)]

from siman.simulated_annealing import SimAnneal

sa = SimAnneal(cities)

solution = sa.initial_solution()
print( sa.cur_fitness )
plotTSP([solution])

# sa.anneal()
#
# better_solution = sa.best_solution
# print(sa.best_fitness)




