import random
from RouteUnit import RouteUnit
import numpy as np
from typing import List

from collections import deque

class GeneticAlgorithm:

    def __init__(self, popsize, city_list):
        self.population: List[RouteUnit] = []
        for i in range(popsize):
            self.population.append(RouteUnit.createRoute(city_list))
        self.max = None
        self.min = None
        self.avg = None
        self.rank()

        self.hist_similarity = deque(maxlen=25)
        self.hist_longest_subseq = deque(maxlen=25)
        self.diverstity_stats()



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

    def breed(self, n, smoothen_chances = 0) -> List[RouteUnit]:

        parents = self.select_parents(n, smoothen_chances)
        children = []

        for i in range(n):
            child = RouteUnit.crossover(parents[i], parents[len(parents) - i - 1])
            children.append(child)

        return children


    def step(self, eliteSize, mutationRate):

        new_size = len(self.population)
        next_generation = self.population[:eliteSize]
        next_generation += self.breed(new_size-eliteSize)

        for child in next_generation[eliteSize:]:
            child.mutate(mutationRate)

        self.population = next_generation
        self.rank()
        self.diverstity_stats()


    @property
    def ra_percentage_common(self):
        return sum(self.hist_similarity) / len(self.hist_similarity)

    @property
    def ra_longest_subseq(self):
        return sum(self.hist_longest_subseq) / len(self.hist_longest_subseq)

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




