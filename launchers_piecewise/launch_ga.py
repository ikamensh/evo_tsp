from GeneticAlgorithm import GeneticAlgorithm
from City import City
from piecewise_route.PiecewiseRoute import PiecewiseRoute

cities = [City(2) for i in range(60)]

def one_run(popsize, epochs, elite_size, mutation_rate):

    ga = GeneticAlgorithm(popsize, cities, PiecewiseRoute)

    ga.run(epochs, elite_size, mutation_rate)


    return ga.population[0]




from cProfile import Profile
profiler = Profile()
profiler.runcall(one_run, popsize=50,
                epochs=int( 250 ),
                elite_size=1,
                mutation_rate= 0.1)

profiler.print_stats('cumulative')


