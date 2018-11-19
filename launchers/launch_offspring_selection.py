from City import cities
from GeneticAlgorithm_OS import GeneticAlgorithm
import matplotlib.pyplot as plt
import random
import os

from siman.visualize_sa import plotTSP


from collections import namedtuple
episode = namedtuple("episode", "generation min avg max similarity longest_common sel_pressure")




def one_run(popsize, epochs, elite_size, mutation_rate):
    ga = GeneticAlgorithm(popsize, cities, planned_epochs=epochs)

    history = []
    try:
        for i in range(epochs):
            if i % 500 == 0:
                print("generation", i)
                print(i, ga.min, ga.avg, ga.max, ga.ra_percentage_common, ga.ra_longest_subseq)
            history.append(episode(i, ga.min, ga.avg, ga.max, ga.ra_percentage_common, ga.ra_longest_subseq, ga.ra_offspr_selection_tries))
            ga.step(elite_size, mutation_rate)
    except StopIteration:
        print("Terminated due to maximum selective pressure")

    folder = f"plots/OS/cities_{len(cities)}_dim{len(cities[0].coordinates)}/{popsize}_{elite_size}_{mutation_rate} --- {ga.max:.3f}"
    print(folder, epochs)
    try:
        os.makedirs(folder)
    except:
        pass

    avg = [e.avg for e in history]
    maxi = [e.max for e in history]
    # mini = [e.min for e in history]
    plt.clf()
    # plt.plot(mini, color="green")
    plt.plot(avg, color="blue")
    plt.plot(maxi, color="black")
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.grid()
    plt.savefig(os.path.join(folder, "distances.png"))

    similarity = [e.similarity for e in history]
    plt.clf()
    plt.plot(similarity)
    plt.ylabel('Similarity')
    plt.xlabel('Generation')
    plt.grid()
    plt.savefig(os.path.join(folder, "similarity.png"))

    sel_pressure = [e.sel_pressure for e in history]
    plt.clf()
    plt.plot(sel_pressure)
    plt.ylabel('Selective Pressure')
    plt.xlabel('Generation')
    plt.grid()
    plt.savefig(os.path.join(folder, "sel_pressure.png"))

    plotTSP( [ga.population[0].route] , save_to=os.path.join(folder, "best_route.png"))

    return ga.population[0]

    # lc = [e.longest_common for e in history]
    #
    # plt.clf()
    # plt.plot(lc, color="green")
    # plt.ylabel('Longest Subseq')
    # plt.xlabel('Generation')
    # plt.grid()
    # plt.savefig(os.path.join(folder, "longest_common.png"))

from cProfile import Profile


from cProfile import Profile
profiler = Profile()
profiler.runcall(one_run, popsize=10,
                epochs=int( 5e3 ),
                elite_size=2,
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

