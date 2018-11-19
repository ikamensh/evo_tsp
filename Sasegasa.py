from GeneticAlgorithm_RAPGA import GeneticAlgorithmRapga


class Sasegasa:

    def __init__(self, cities, n_villages=10, size_per_village=1000, epochs_per_step = 100):
        self.n_villages = n_villages
        self.size_per_village = size_per_village
        self.epochs_per_step = epochs_per_step

        make_random_village = lambda : GeneticAlgorithmRapga.with_random_population(size_per_village, cities, epochs_per_step)
        self.villages = [make_random_village() for _ in range(n_villages) ]

    def redistribute(self):

        self.n_villages -= 1
        total_population = sum([ga.population for ga in self.villages])
        size = len(total_population)

        populations = [total_population[i:i+size]]
        new_villages =