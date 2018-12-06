import random
from solutions.AbstractRoute import AbstractRoute
import numpy as np
from typing import List, ClassVar

from collections import deque

from collections import namedtuple
episode = namedtuple("episode", "generation min avg max similarity")

from ga_utils.ploting import plot_many, my_plot, problem_tag, plot_histogram
from ga_utils.draw_route import plot_route
from ga_utils import stats
import os

class GeneticAlgorithm:

    def __init__(self, popsize, city_list, route_cls: ClassVar ):
        assert issubclass(route_cls, AbstractRoute)
        self.route_cls = route_cls
        self.city_list = city_list
        self.population: List[AbstractRoute] = []
        for i in range(popsize):
            self.population.append(route_cls.create_route(city_list))

        self.champions = []

        self.history = []
        self.max = None
        self.min = None
        self.avg = None
        self.rank()

        self.hist_similarity = deque(maxlen=25)
        self.diverstity_stats()

        self.tag = "standard " + str(random.randint(1000,10000))



    def rank(self):
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        self.max = self.population[0].distance
        self.min = self.population[-1].distance
        self.avg = sum([x.distance for x in self.population]) / len(self.population)

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
            if i % 100 == 0:
                print("generation", i)
                print(i, self.min, self.avg, self.max, self.population[0].fitness, self.ra_percentage_common)
                self.champions.append(self.population[0])
                print(" ")

                other_stats = self.route_cls.compute_stats(self.population)
                for name, values in other_stats.items():
                    folder = f"plots/{problem_tag(self.city_list)}" \
                        f"/{self.tag}/{len(self.population)}_{elite_size}_{mutation_rate}"
                    plot_histogram(values, name + f"_{i}", folder)

            # best_not_visited = self.population[0].cities_not_visited()
            # worst_not_visited = self.population[-1].cities_not_visited()
            # print(best_not_visited, worst_not_visited)
            #
            # best_fitness = self.population[0].fitness
            # worst_fitness = self.population[-1].fitness
            # print(best_fitness, worst_fitness)


            self.history.append(episode(i, self.min, self.avg, self.max, self.ra_percentage_common))
            self.step(elite_size, mutation_rate)


    @property
    def ra_percentage_common(self):
        return sum(self.hist_similarity) / len(self.hist_similarity)

    def diverstity_stats(self):
        percentages = []

        for r1 in random.sample(self.population, 1 + len(self.population) // 10):
            r2 = random.choice(self.population)
            percentages.append( stats.percent_common_route(r1.route, r2.route) )

        percentage_common = sum(percentages) / len(percentages)

        self.hist_similarity.append(percentage_common)


    def document(self, epochs, elite_size, mutation_rate):
        history = self.history

        folder = f"plots/{problem_tag(self.city_list)}" \
                 f"/{self.tag}/{len(self.population)}_{elite_size}_{mutation_rate} --- {self.max:.3f}"

        print(folder, epochs)


        avg = [e.avg for e in history]
        maxi = [e.max for e in history]
        plot_many("Distance", folder, avg, maxi)

        my_plot([e.similarity for e in history], "similarity", folder)
        # my_plot([e.sel_pressure for e in history], "Selective Pressure", folder)
        # my_plot([e.popsize for e in history], "Population Size", folder)

        plot_route([self.population[0]], save_to= ( folder, "best_route.png") )




