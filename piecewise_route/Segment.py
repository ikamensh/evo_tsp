from __future__ import annotations
from City import City
from typing import Dict, List
from dataclasses import dataclass, field
import random
import math

@dataclass()
class Segment:
    from_to: Dict[City, City]
    cities: List[City] = field(repr=False)
    dominance: float = field(default_factory= lambda : 1 + random.random())

    # def __post_init__(self):
    #     if len(self.from_to) == 0:
    #         raise Exception("Empty segments are not allowed.")

    @staticmethod
    def from_list( lst : List[City], all_cities : List[City]):
        from_to = {}
        for i, c in enumerate(lst[:-1]):
            from_to[c] = lst[i+1]

        return Segment(from_to, all_cities)

    def cities_not_went(self):
        cities_visited = set( self.from_to.values() )
        cities_not_visited = set(self.cities) - cities_visited
        return cities_not_visited


    def mutate(self, mutation_rate:float):
        throw = random.random()
        n_mutations = math.floor( math.log(throw, mutation_rate) ) # the smaller the throw, the more mutations we make.
        self._mutate(n_mutations)

    def crossover(self, other: Segment):
        from_to = {}

        while len(from_to) == 0:
            from_p1 = list(self.from_to.keys())
            crossover_point1 = random.randint(0, len(from_p1))
            p1 = from_p1[:crossover_point1], from_p1[crossover_point1:]
            p1 = random.choice(p1)


            from_p2 = list(other.from_to.keys())
            crossover_point2 = random.randint(0, len(from_p2))
            p2 = from_p2[:crossover_point2], from_p2[crossover_point2:]
            p2 = random.choice(p2)

            from_to.update({k:self.from_to[k] for k in p1})
            from_to.update({k:other.from_to[k] for k in p2})

        new_dominance = random.choice([self.dominance, other.dominance])

        return Segment(from_to, self.cities, new_dominance)


    def _mutate(self, n_mutations):
        for _ in range(n_mutations):
            mutator = random.choice([self.del_mutation,
                                     self.new_segm_mutation,
                                     self.change_dep_mutation,
                                     self.change_dest_mutation,
                                     self.change_dominance])
            mutator()


    def del_mutation(self):
        if len(self.from_to.keys()) > 1:
            key = random.choice( list(self.from_to.keys() ))
            del self.from_to[key]

    def new_segm_mutation(self):
        c_from = random.choice(self.cities)
        c_to = random.choice(self.cities)
        self.from_to[c_from] = c_to

    def change_dest_mutation(self):
        c_from = random.choice(list(self.from_to.keys()))
        c_to = random.choice(self.cities)
        self.from_to[c_from] = c_to

    def change_dep_mutation(self):
        c_from = random.choice(self.cities)
        c_from_before, c_to = random.choice(list(self.from_to.items()))
        del self.from_to[c_from_before]
        self.from_to[c_from] = c_to

    def change_dominance(self):
        self.dominance += random.random() - 0.5
        if self.dominance < 0:
            self.dominance = 0
        elif self.dominance > 10:
            self.dominance = 10


