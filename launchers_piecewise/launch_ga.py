from GeneticAlgorithm import GeneticAlgorithm
from City import City
from solutions.PiecewiseRoute import PiecewiseRoute
from classical.sim_anneal import nearest_neighbour_solution

cities = [City(2) for i in range(60)]

def one_run(popsize, epochs, elite_size, mutation_rate):

    ga = GeneticAlgorithm(popsize, cities, PiecewiseRoute)
    # nn_pop = [PiecewiseRoute.create_route( nearest_neighbour_solution(cities).route, shuffle= False ) for i in range(popsize)]
    # ga.population = nn_pop
    # ga.rank()
    # ga.tag = "from nearest neighbour"
    ga.run(epochs, elite_size, mutation_rate)
    ga.document(epochs, elite_size, mutation_rate)


    return ga.population[0]


# one_run(popsize=50,epochs=100,elite_size=1,mutation_rate=0.005)

from concurrent import futures

if __name__ == "__main__":


    with futures.ProcessPoolExecutor() as executor:

        todo = []

        for popsize in [50, 200]:
            for mutation_rate in [0.01, 0.05, 0.005, 0.001]:
                future = executor.submit(one_run, popsize, 3000, popsize//50, mutation_rate)
                todo.append( future )

        for future in futures.as_completed(todo):
            print(future.result())




# from cProfile import Profile
# profiler = Profile()
# profiler.runcall(one_run, popsize=50,
#                 epochs=int( 50000 ),
#                 elite_size=10,
#                 mutation_rate= 0.1)
#
# profiler.print_stats('cumulative')


