from GeneticAlgorithm_RAPGA import GeneticAlgorithmRapga

from siman.launch_sa import annealed_solution


from collections import namedtuple
episode = namedtuple("episode", "generation min avg max similarity longest_common sel_pressure popsize")





def one_run(popsize, epochs, elite_size, mutation_rate):

    annealed = [annealed_solution() for i in range(popsize//2)]
    ga = GeneticAlgorithmRapga(annealed, maxpop=1000,
                               planned_epochs=epochs, elite_size=elite_size, mutation_rate=mutation_rate)

    # max_injections = 20
    # injections = 0

    ga.run()


    return ga.population[0]




from cProfile import Profile
profiler = Profile()
profiler.runcall(one_run, popsize=50,
                epochs=int( 2000 ),
                elite_size=1,
                mutation_rate= 8e-3)

profiler.print_stats('cumulative')

# import time
# t = time.time()
# for popsize in [10, 30, 80]:
#     for mutation_rate in [5e-3, 8e-3, 2e-2]:
#         one_run(popsize=popsize,
#                 epochs=int( 1e6 // popsize),
#                 elite_size=min(popsize//4,15) + popsize//25,
#                 mutation_rate= mutation_rate)
#         print(time.time()-t)
#         t = time.time()

# one_run(50,
#         epochs=50000,
#         elite_size=10,
#         mutation_rate= 1e-4)






# def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations):
#     pop = initialPopulation(popSize, population)
#     progress = []
#     progress.append(1 / rankRoutes(pop)[0][1])
#
#     for i in range(0, generations):
#         pop = nextGeneration(pop, eliteSize, mutationRate)
#         progress.append(1 / rankRoutes(pop)[0][1])
#
#     plt.plot(progress)
#     plt.ylabel('Distance')
#     plt.xlabel('Generation')
#     plt.show()
#
# geneticAlgorithmPlot(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)

