import random
from RouteUnit import RouteUnit
from City import City
import numpy as np
from typing import List
import os
from utils.plotting import plot_many, my_plot
from utils.draw_route import plot_route

from collections import deque

from collections import namedtuple
episode = namedtuple("episode", "generation min avg max similarity longest_common sel_pressure popsize")

class GeneticAlgorithmRapga:

    def __init__(self, initial_population: List[RouteUnit],*, maxpop, planned_epochs = 100, elite_size = None, mutation_rate = None):

        self.cities = len(initial_population[0].route)

        self.population = initial_population
        self.min_size = 5
        self.max_size = maxpop

        self.elite_size = elite_size or 1
        self.mutation_rate = mutation_rate or 1 / self.cities

        self.tag = "no_tag"


        self.max = None
        self.min = None
        self.avg = None
        self.rank()

        self.hist_similarity = deque(maxlen=25)
        self.hist_longest_subseq = deque(maxlen=25)
        self.diverstity_stats()

        self.planned_epochs = planned_epochs
        self.epoch = 0

        self.max_tries = int(2000 * (self.min_size / self.max_size)) # maximum generations for search for successful offsprings - per epoch
        # self.min_success_ratio = 0.3
        # self.max_success_ratio = 0.8

        self.min_selective_pressure = 0.5
        self.max_selective_pressure = 0.95


        self.tries_history = deque([1],maxlen=25)

        self.history = []

    @staticmethod
    def with_random_population(popsize: int, city_list: List[City], planned_epochs: int,
                               elite_size: int = None, mutation_rate: float = None):
        population = []
        for i in range(popsize):
            population.append(RouteUnit.createRoute(city_list))
        return GeneticAlgorithmRapga(population, maxpop=len(population), planned_epochs=planned_epochs,
                                     elite_size=elite_size, mutation_rate=mutation_rate)


    # success ratio is the portion of population which must be filled with successful offspring
    # @property
    # def success_ratio(self):
    #     ratio = self.epoch / self.planned_epochs
    #     return ratio*self.max_success_ratio + (1-ratio)*self.min_success_ratio


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
        chances = np.arange(len(self.population), 0, -1, dtype=np.int) + len(self.population) * smoothen_chances / (1 - smoothen_chances + 1e-9)
        chances = chances / sum(chances)
        parent_indexes = np.random.choice(indexes, n, True, chances)
        parents = np.array(self.population)[parent_indexes]

        return parents

    def breed_os(self, n, *, elite, mutation_rate, smoothen_chances = 0.5) -> List[RouteUnit]:
        """
        Breed new generation with Offspring selection.

        we try to fill the self.success_ratio proportion of the population with only children who are better when their parents.
        """

        successful = set(elite)

        n_tries = 0

        while len(successful) < self.max_size and n_tries < self.max_tries:
            n_tries += 1
            if n_tries > self.max_tries:
                break

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
        new_generation = self.breed_os(self.max_size, elite=elite, mutation_rate=mutationRate)

        self.population = new_generation
        self.rank()
        self.diverstity_stats()

        self.epoch += 1


    def run(self):

        try:
            for i in range(self.planned_epochs):
                if i % 30 == 0:
                    print("generation", i)
                    print(i, self.min, self.avg, self.max, self.ra_percentage_common, len(self.population))
                self.history.append(episode(i, self.min, self.avg, self.max, self.ra_percentage_common, self.ra_longest_subseq,
                                            self.ra_offspr_selection_tries, len(self.population)))
                self.step(self.elite_size, self.mutation_rate)
        except StopIteration:
            print("Terminated due to maximum selective pressure")



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

    def document(self):
        history = self.history

        folder = f"plots/cities_{self.cities}_dim{len(self.population[0].route[0].coordinates)}" \
                 f"/{self.tag}/{self.max_size}_{self.elite_size}_{self.mutation_rate} --- {self.max:.3f}"
        print(folder, self.epoch)
        try:
            os.makedirs(folder)
        except:
            pass

        avg = [e.avg for e in history]
        maxi = [e.max for e in history]
        plot_many("Distance", folder, avg, maxi)

        my_plot([e.similarity for e in history], "similarity", folder)
        my_plot([e.sel_pressure for e in history], "Selective Pressure", folder)
        my_plot([e.popsize for e in history], "Population Size", folder)

        plot_route([self.population[0].route], save_to=os.path.join(folder, "best_route.png"))




