import random
from piecewise_route.AbstractRoute import AbstractRoute
import numpy as np
from typing import List, ClassVar

from collections import deque

from collections import namedtuple
episode = namedtuple("episode", "generation min avg max similarity")

class GeneticAlgorithm:

    def __init__(self, popsize, city_list, route_cls: ClassVar ):
        assert issubclass(route_cls, AbstractRoute)
        self.route_cls = route_cls
        self.population: List[AbstractRoute] = []
        for i in range(popsize):
            self.population.append(route_cls.create_route(city_list))

        self.history = []
        self.max = None
        self.min = None
        self.avg = None
        self.rank()

        self.hist_similarity = deque(maxlen=25)
        self.hist_longest_subseq = deque(maxlen=25)
        # self.diverstity_stats()



    def rank(self):
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        self.max = self.population[0].distance()
        self.min = self.population[-1].distance()
        self.avg = sum([x.distance() for x in self.population]) / len(self.population)

    def select_parents(self, n, smoothen_chances):
        indexes = np.arange(0, len(self.population), dtype=np.int)
        chances = np.arange(len(self.population), 0, -1, dtype=np.int) + smoothen_chances / (1 - smoothen_chances + 1e-9)
        chances = chances / sum(chances)
        parent_indexes = np.random.choice(indexes, n, True, chances)
        parents = np.array(self.population)[parent_indexes]

        return parents

    def breed(self, n, smoothen_chances = 0) -> List[AbstractRoute]:

        parents = self.select_parents(n, smoothen_chances)
        children = []

        for i in range(n):
            parent_1 = parents[i]
            parent_2 = parents[len(parents) - i - 1]
            child = parent_1.crossover(parent_2)
            children.append(child)

        return children

    @staticmethod
    def offspring_selection(parent_1: AbstractRoute, parent_2: AbstractRoute, child: AbstractRoute, pressure_coef):
        best_parent_fitness = max(parent_1.fitness, parent_2.fitness)
        worst_parent_fitness = min(parent_1.fitness, parent_2.fitness)

        threshold = best_parent_fitness * pressure_coef + (1-pressure_coef) * worst_parent_fitness

        return child.fitness > threshold




    def step(self, eliteSize, mutationRate):

        new_size = len(self.population)
        next_generation = self.population[:eliteSize]
        next_generation += self.breed(new_size-eliteSize)

        for child in next_generation[eliteSize:]:
            child.mutate(mutationRate)

        self.population = next_generation
        self.rank()
        # self.diverstity_stats()


    def run(self, epochs, elite_size, mutation_rate):

        for i in range(epochs):
            # if i % 30 == 0:
            print("generation", i)
            print(i, self.min, self.avg, self.max, self.ra_percentage_common)

            best_not_visited = self.population[0].cities_not_visited()
            worst_not_visited = self.population[-1].cities_not_visited()
            print(best_not_visited, worst_not_visited)

            best_fitness = self.population[0].fitness
            worst_fitness = self.population[-1].fitness
            print(best_fitness, worst_fitness)


            self.history.append(episode(i, self.min, self.avg, self.max, self.ra_percentage_common))
            self.step(elite_size, mutation_rate)


    @property
    def ra_percentage_common(self):
        return 0
        return sum(self.hist_similarity) / len(self.hist_similarity)

    @property
    def ra_longest_subseq(self):
        return sum(self.hist_longest_subseq) / len(self.hist_longest_subseq)

    def diverstity_stats(self):
        percentages = []
        longest = []

        for r1 in random.sample(self.population, 1 + len(self.population) // 10):
            r2 = random.choice(self.population)
            percentages.append( self.route_cls.percent_common(r1, r2) )
            longest.append( 0 )



        percentage_common = sum(percentages) / len(percentages)
        avg_longest_subseq = sum(longest) / len(longest)

        self.hist_similarity.append(percentage_common)
        self.hist_longest_subseq.append(avg_longest_subseq)




