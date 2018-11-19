from City import cities
from GeneticAlgorithm_RAPGA import GeneticAlgorithmRapga
import matplotlib.pyplot as plt
import os

from siman.visualize_sa import plot_route

from siman.launch_sa import annealed_solution


from collections import namedtuple
episode = namedtuple("episode", "generation min avg max similarity longest_common sel_pressure popsize")


def my_plot(array, name, folder):
    plt.clf()
    plt.plot(array)
    plt.ylabel(name)
    plt.xlabel('Generation')
    plt.grid()
    plt.savefig(os.path.join(folder, name+".png"))

def plot_many(name, folder, *args):
    plt.clf()
    for array in args:
        plt.plot(array)
    plt.ylabel(name)
    plt.xlabel('Generation')
    plt.grid()
    plt.savefig(os.path.join(folder, name + ".png"))


def one_run(popsize, epochs, elite_size, mutation_rate):
    ga = GeneticAlgorithmRapga.with_random_population(popsize, cities, planned_epochs=epochs)
    max_injections = 20
    injections = 0

    history = []
    try:
        for i in range(epochs):
            if i % 30 == 0:
                print("generation", i)
                print(i, ga.min, ga.avg, ga.max, ga.ra_percentage_common, len(ga.population))
            history.append(episode(i, ga.min, ga.avg, ga.max, ga.ra_percentage_common, ga.ra_longest_subseq, ga.ra_offspr_selection_tries, len(ga.population)))
            ga.step(elite_size, mutation_rate)

            if injections < max_injections and ga.ra_offspr_selection_tries > ga.max_tries / 4:
                ga.population.append( annealed_solution() )
                ga.rank()
                injections += 1

    except StopIteration:
        print("Terminated due to maximum selective pressure")

    folder = f"plots/RAPGA_No_elite/cities_{len(cities)}_dim{len(cities[0].coordinates)}/{popsize}_{elite_size}_{mutation_rate} --- {ga.max:.3f}"
    print(folder, epochs)
    try:
        os.makedirs(folder)
    except:
        pass

    avg = [e.avg for e in history]
    maxi = [e.max for e in history]
    plot_many("Distance", folder, avg, maxi)

    # plt.clf()
    # plt.plot(avg, color="blue")
    # plt.plot(maxi, color="black")
    # plt.ylabel('Distance')
    # plt.xlabel('Generation')
    # plt.grid()
    # plt.savefig(os.path.join(folder, "distances.png"))

    my_plot([e.similarity for e in history], "similarity", folder)
    my_plot([e.sel_pressure for e in history], "Selective Pressure", folder)
    my_plot([e.popsize for e in history], "Population Size", folder)

    plot_route([ga.population[0].route], save_to=os.path.join(folder, "best_route.png"))

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

