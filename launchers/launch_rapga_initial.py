from GeneticAlgorithm_RAPGA import GeneticAlgorithmRapga

from classical.sim_anneal import annealed_solution



def one_run(popsize, epochs, elite_size, mutation_rate):

    annealed = [annealed_solution() for i in range(popsize//2)]
    ga = GeneticAlgorithmRapga(annealed, maxpop=1000,
                               planned_epochs=epochs, elite_size=elite_size, mutation_rate=mutation_rate)


    ga.run()


    return ga.population[0]




from cProfile import Profile
profiler = Profile()
profiler.runcall(one_run, popsize=50,
                epochs=int( 2000 ),
                elite_size=1,
                mutation_rate= 8e-3)

profiler.print_stats('cumulative')


