from GeneticAlgorithm_RAPGA import GeneticAlgorithmRapga
import random
import datetime

class Sasegasa:

    def __init__(self, cities, n_villages=10, size_per_village=1000, epochs_per_step = 100):
        self.n_villages = n_villages
        self.size_per_village = size_per_village
        self.epochs_per_step = epochs_per_step

        make_random_village = lambda : GeneticAlgorithmRapga.with_random_population(size_per_village, cities, epochs_per_step)
        self.villages = [make_random_village() for _ in range(n_villages) ]
        self.uid = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.set_tags()

    def set_tags(self):
        for v in self.villages:
            v.tag = f"SASEGASA/run_{self.uid}_{self.n_villages}"

    def run(self):
        while self.n_villages > 1:
            self.step()
        last_village = self.villages[0]
        last_village.run()
        last_village.document()

        return last_village

    def step(self):
        for ga in self.villages:
            ga.run()
            ga.document()
        pop = []
        for ga in self.villages:
            pop += ga.population
        self.redistribute(pop)
        self.set_tags()

    def redistribute(self, _population):

        population = list(_population)
        self.n_villages -= 1
        random.shuffle(population)

        size = len(population)

        populations = [population[i:i+size] for i in range(self.n_villages)]
        homeless = population[size*self.n_villages:]
        assert len(homeless) < len(populations)
        for i, unit in enumerate(homeless):
            populations[i].append(unit)

        create_village = lambda pop: GeneticAlgorithmRapga(pop,
                                                           maxpop=self.size_per_village,
                                                           planned_epochs=self.epochs_per_step)

        new_villages = [create_village(pop) for pop in populations]
        self.villages = new_villages



