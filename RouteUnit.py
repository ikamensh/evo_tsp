from __future__ import annotations
from typing import List, Dict
from City import City
import random
from borrowed import longest_common_seq

class RouteUnit:
    def __init__(self, route: List[City]):
        self.route = route
        self._distance = None
        self._fitness = 0.0

    def distance(self):
        if self._distance is None:
            self._distance = self.route_distance(self.route)
        return self._distance

    @staticmethod
    def route_distance(route):
        pathDistance = 0
        for i in range(0, len(route)):
            fromCity = route[i]
            if i + 1 < len(route):
                toCity = route[i + 1]
            else:
                toCity = route[0]
            pathDistance += fromCity.distance(toCity)
        return pathDistance

    @property
    def fitness(self):
        if self._fitness == 0:
            self._fitness = 1 / float(self.distance())
        return self._fitness

    @staticmethod
    def crossover(parent1: RouteUnit, parent2: RouteUnit) -> RouteUnit:
        """
        Create a child which will have a random subsequence from parent1,
        and the rest of the sequence from parent2. The sequence from parent2 will have the
        :param parent1:
        :param parent2:
        :return:
        """

        routeA = parent1.route
        routeB = parent2.route

        geneA = int(random.random() * len(routeA))
        geneB = int(random.random() * len(routeB))

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        childP1 = routeA[startGene: endGene]
        childP2 = [item for item in routeB if item not in childP1]

        child = childP1 + childP2

        return RouteUnit(child)

    def mutate(self, mutationRate):

        # if random.random() < 0.5:
        #     self.mutate_2()
        # else:
            for swapped in range(len(self.route)):
                if random.random() < mutationRate:
                    swapWith = int(random.random() * len(self.route))

                    city1 = self.route[swapped]
                    city2 = self.route[swapWith]

                    self.route[swapped] = city2
                    self.route[swapWith] = city1

    def mutate_2(self):
        length = random.randint(2, len(self.route) - 1)
        index = random.randint(0, len(self.route) - length)
        self.route[index:(index + length)] = reversed(self.route[index:(index + length)])

    @staticmethod
    def createRoute(cityList: List[City]) -> RouteUnit:
        route = list(cityList)
        random.shuffle(route)
        return RouteUnit(route)


    # stats methods
    @staticmethod
    def percent_common(route1: RouteUnit, route2: RouteUnit):
        r1 = route1.route
        r2 = route2.route

        assert len(r1) == len(r2)

        moves_1 = { (r1[i], r1[i+1]) for i in range(len(r1)-1)}
        moves_1.add( (r1[-1], r1[0]) )
        moves_2 = { (r2[i], r2[i+1]) for i in range(len(r2)-1)}
        moves_2.add((r2[-1], r2[0]))

        return len( moves_1.intersection(moves_2) ) / len(moves_1)

    @staticmethod
    def longest_common_sequence(route1: RouteUnit, route2: RouteUnit):
        r1 = route1.route
        r2 = route2.route

        seqs = longest_common_seq(r1, r2)

        return seqs



