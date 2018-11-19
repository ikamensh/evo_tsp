import random
from RouteUnit import RouteUnit
import numpy as np
from typing import List

from collections import deque

class GeneticAlgorithmRapga:

    def __init__(self, popsize, city_list, planned_epochs = 100):
        self.population: List[RouteUnit] = []
        for i in range(popsize):
            self.population.append(RouteUnit.createRoute(city_list))

        self.min_size = 2
        self.max_size = popsize * 2


        self.max = None
        self.min = None
        self.avg = None
        self.rank()

        self.hist_similarity = deque(maxlen=25)
        self.hist_longest_subseq = deque(maxlen=25)
        self.diverstity_stats()

        self.planned_epochs = planned_epochs
        self.epoch = 0

        self.max_tries = 500 # maximum generations for search for successful offsprings - per epoch
        self.min_success_ratio = 0.3
        self.max_success_ratio = 0.8

        self.min_selective_pressure = 0.5
        self.max_selective_pressure = 0.95


        self.tries_history = deque([1],maxlen=25)


    # success ratio is the portion of population which must be filled with successful offspring
    @property
    def success_ratio(self):
        ratio = self.epoch / self.planned_epochs
        return ratio*self.max_success_ratio + (1-ratio)*self.min_success_ratio

    # selective pressure is a coefficient that determines whom of the parents must the child exceed
    #  - the better or the worse
    @property
    def selective_pressure(self):
        ratio = self.epoch / self.planned_epochs
        return ratio * self.max_selective_pressure + (1 - ratio) * self.min_selective_pressure

    # sorts the population, fills min, max, avg
    def rank(self):
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        self.max = self.population[0].distance()
        self.min = self.population[-1].distance()
        self.avg = sum([x.distance() for x in self.population]) / len(self.population)

    # choose individuals to become parents according to their fitnesses (ranked selection)
    def select_parents(self, n, smoothen_chances):
        indexes = np.arange(0, len(self.population), dtype=np.int)
        chances = np.arange(len(self.population), 0, -1, dtype=np.int) + smoothen_chances / (1 - smoothen_chances + 1e-9)
        chances = chances / sum(chances)
        parent_indexes = np.random.choice(indexes, n, True, chances)
        parents = np.array(self.population)[parent_indexes]

        return parents

    def breed_os(self, n, *, mutation_rate, smoothen_chances = 0.8) -> List[RouteUnit]:
        """
        Breed new generation with Offspring selection.

        we try to fill the self.success_ratio proportion of the population with only children who are better when their parents.
        """

        successful = set()

        n_tries = 0

        while len(successful) < self.max_size and n_tries < self.max_tries:
            n_tries += 1
            if n_tries > self.max_tries:
                raise StopIteration

            parents = self.select_parents(n, smoothen_chances)

            for i in range(n):
                parent_1 = parents[i]
                parent_2 = parents[len(parents) - i - 1]
                child = RouteUnit.crossover(parent_1, parent_2)
                child.mutate(mutation_rate)
                if self.offspring_selection(parent_1, parent_2, child, self.selective_pressure):
                    successful.add(child)


        self.tries_history.append(n_tries)

        if len(successful) < self.min_size:
            raise StopIteration

        return list(successful)

    @staticmethod
    def offspring_selection(parent_1: RouteUnit, parent_2: RouteUnit, child: RouteUnit, pressure_coef):
        best_parent_fitness = max(parent_1.fitness, parent_2.fitness)
        worst_parent_fitness = min(parent_1.fitness, parent_2.fitness)

        threshold = best_parent_fitness * pressure_coef + (1-pressure_coef) * worst_parent_fitness

        return child.fitness > threshold




    def step(self, eliteSize, mutationRate):

        elite = self.population[:eliteSize]
        new_generation = self.breed_os(self.max_size, mutation_rate=mutationRate)

        self.population = elite + new_generation
        self.rank()
        self.diverstity_stats()

        self.epoch += 1


    @property
    def ra_percentage_common(self):
        return sum(self.hist_similarity) / len(self.hist_similarity)

    @property
    def ra_longest_subseq(self):
        return sum(self.hist_longest_subseq) / len(self.hist_longest_subseq)

    @property
    def ra_offspr_selection_tries(self):
        return sum(self.tries_history) / len(self.tries_history)

    def diverstity_stats(self):
        percentages = []
        longest = []

        for r1 in random.sample(self.population, 1 + len(self.population) // 10):
            r2 = random.choice(self.population)
            percentages.append( RouteUnit.percent_common(r1, r2) )
            # common_seq = RouteUnit.longest_common_sequence(r1, r2)
            # longest.append( len(common_seq) )
            longest.append( 0 )



        percentage_common = sum(percentages) / len(percentages)
        avg_longest_subseq = sum(longest) / len(longest)

        self.hist_similarity.append(percentage_common)
        self.hist_longest_subseq.append(avg_longest_subseq)




