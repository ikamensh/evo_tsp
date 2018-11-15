import random
from City import City
from GeneticAlgorithm import GeneticAlgorithm
import matplotlib.pyplot as plt

import os

from collections import namedtuple
episode = namedtuple("episode", "generation min avg max similarity longest_common")

cities = [City(x=int(random.random() * 200), y=int(random.random() * 200)) for i in range(60)]

def one_run(popsize, epochs, elite_size, mutation_rate):
    ga = GeneticAlgorithm(popsize, cities)

    history = []
    for i in range(epochs):
        # if i % 50 == 0:
        #     print("generation", i)
        history.append(episode(i, ga.min, ga.avg, ga.max, ga.ra_percentage_common, ga.ra_longest_subseq))
        ga.step(elite_size, mutation_rate)

    folder = f"plots/{popsize}_{elite_size}_{mutation_rate}"
    print(folder, epochs)
    try:
        os.mkdir(folder)
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

    # lc = [e.longest_common for e in history]
    #
    # plt.clf()
    # plt.plot(lc, color="green")
    # plt.ylabel('Longest Subseq')
    # plt.xlabel('Generation')
    # plt.grid()
    # plt.savefig(os.path.join(folder, "longest_common.png"))

for popsize in [10, 30, 100, 300]:
    for mutation_rate in [5e-3, 1e-3, 1e-2]:
        one_run(popsize, 1e6 // popsize, min(popsize//4,15) + popsize//25, mutation_rate)
        # one_run(popsize, int( (1000000/popsize)**0.9 ), min(popsize//4,15) + popsize//25, mutation_rate)








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

