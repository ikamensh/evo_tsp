from __future__ import annotations
from typing import List, Dict
from City import City
import random
from borrowed import longest_common_seq
from solutions.AbstractRoute import AbstractRoute

class RouteUnit(AbstractRoute):
    def __init__(self, route: List[City]):
        self._route = list(route)
        self._distance = None
        self._fitness = 0.0


    @property
    def route(self):
        return self._route

    @staticmethod
    def create_route(cityList: List[City]) -> RouteUnit:
        route = list(cityList)
        random.shuffle(route)
        return RouteUnit(route)

    @property
    def distance(self):
        if self._distance is None:
            self._distance = self.route_distance(self.route)
        return self._distance

    @staticmethod
    def route_distance(route: List[City]):
        pathDistance = 0
        path = route + [route[0]]
        for i in range(0, len(path)-1):
            pathDistance += path[i].distance(path[i+1])
        return pathDistance

    @property
    def fitness(self):
        if self._fitness == 0:
            self._fitness = 1 / float(self.distance + 1)
        return self._fitness

    def crossover(self: RouteUnit, parent2: RouteUnit) -> RouteUnit:
        """
        Create a child which will have a random subsequence from parent1,
        and the rest of the sequence from parent2. The sequence from parent2 will have the
        :param self:
        :param parent2:
        :return:
        """

        routeA = self.route
        routeB = parent2.route

        geneA = random.randint(0, City.n_cities)
        geneB = random.randint(0, City.n_cities)

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        childP1 = routeA[startGene: endGene]
        check = {city.uid for city in childP1}
        childP2 = [item for item in routeB if item.uid not in check]

        child = childP1 + childP2

        return RouteUnit(child)

    def mutate(self, mutationRate):
        self._distance = None
        if random.random() < 0.5:
            self._mutate_2()
        else:
            for swapped in range(len(self.route)):
                if random.random() < mutationRate:
                    swapWith = int(random.random() * len(self.route))

                    city1 = self.route[swapped]
                    city2 = self.route[swapWith]

                    self.route[swapped] = city2
                    self.route[swapWith] = city1

    def _mutate_2(self):
        length = random.randint(2, len(self.route) - 1)
        index = random.randint(0, len(self.route) - length)
        self.route[index:(index + length)] = reversed(self.route[index:(index + length)])


    @staticmethod
    def longest_common_sequence(route1: RouteUnit, route2: RouteUnit):
        r1 = route1.route
        r2 = route2.route

        seqs = longest_common_seq(r1, r2)

        return seqs

    def __eq__(self, other:RouteUnit):
        assert len(self.route) == len(other.route)
        if self.percent_common(self, other) == 1:
            return True
        else:
            return False


    def __hash__(self):
        total = 0
        for i in range(len(self.route)-1):
            city_from = self.route[i]
            city_to = self.route[i+1]
            total += hash( (city_from, city_to) )
        total += hash( (self.route[-1], self.route[0]) )
        return hash(total)


