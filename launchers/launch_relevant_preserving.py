from City import cities
from GeneticAlgorithm_RAPGA import GeneticAlgorithmRapga



from collections import namedtuple
episode = namedtuple("episode", "generation min avg max similarity longest_common sel_pressure popsize")


def one_run(popsize, epochs, elite_size, mutation_rate):
    ga = GeneticAlgorithmRapga.with_random_population(popsize, cities,
                                                      elite_size=elite_size,
                                                      mutation_rate=mutation_rate,
                                                      planned_epochs=epochs)
    ga.tag = "Rapga"
    ga.run()
    ga.document()
    


from cProfile import Profile
profiler = Profile()
profiler.runcall(one_run, popsize=1000,
                epochs=int( 2000 ),
                elite_size=2,
                mutation_rate= 8e-3)

profiler.print_stats('cumulative')



