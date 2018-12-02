from __future__ import annotations
from piecewise_route.Segment import Segment
from piecewise_route.AbstractRoute import AbstractRoute
from City import City
from RouteUnit import RouteUnit
from typing import List
import random
import math

N_SEGMENTS_REGULARIZATION = 1e-4
SEG_LENGTH_REGULARIZATION = 1e-7

import copy

class PiecewiseRoute(AbstractRoute):

    def __init__(self, segments: List[Segment], all_cities: List[City]):
        if len(segments) == 0:
            raise Exception("Empty routes are not allowed.")
        new_segments = []
        if segments:
            for seg in segments:
                new_segments.append(Segment(dict(seg.from_to), all_cities))
        self.segments = new_segments

        self.all_cities = all_cities
        self._fitness = None
        self.n_segments_reg_threshold = min( int( 4 * math.sqrt(len(all_cities)) ), len(all_cities) // 2)
        self.n_transitions_reg_threshold = len(all_cities) * 10


    @staticmethod
    def create_route(_city_list: List[City]) -> PiecewiseRoute:

        city_list = list(_city_list)
        random.shuffle(city_list)
        city_list.append(city_list[0])
        n_segments_max = min( int( 2 * math.sqrt(len(city_list)) ), len(city_list) // 2)
        n_segments = random.randint(2, n_segments_max)
        cities_per_segment = len(city_list) / n_segments
        segments = []

        start = 0
        for i in range(n_segments-1):
            end = int( start + cities_per_segment - 1 + random.randint(0,2) )
            new_segment = Segment.from_list(city_list[start:end+1], _city_list)
            segments.append(new_segment)

            start = end
            if start >= len(city_list) - 1:
                break

        if start < len(city_list) - 1:
            segments.append( Segment.from_list(city_list[start:], _city_list) )

        return PiecewiseRoute(segments, _city_list)


    def to_route(self) -> List[City]:
        if len(self.segments) == 0:
            return []

        seq = {}
        sorted_segments = sorted(self.segments, key= lambda x: x.dominance)
        for segment in sorted_segments:
            seq.update(segment.from_to)
            for k, v in segment.from_to.items():
                if (v, k) in seq.items():
                    del seq[v]


        first = list(seq.keys())[0]
        route = [first]

        not_visited = set(self.all_cities)
        not_visited.remove(first)

        for _ in range(len(self.all_cities)-1):
            try:
                next_city = seq[route[-1]]
                if next_city not in not_visited:
                    next_city = random.sample(not_visited, 1)[0]
                route.append(next_city)
                not_visited.remove(next_city)
            except KeyError:
                next_city = random.sample(not_visited, 1)[0]
                route.append(next_city)
                not_visited.remove(next_city)

        if route[0] == route[-1]:
            route.pop()

        return route

    def distance(self):
        route_unit = RouteUnit(self.to_route())
        return route_unit.distance()

    def cities_not_visited(self):
        route_unit = RouteUnit(self.to_route())
        return len( set(self.all_cities) - set(route_unit.route) )


    @property
    def fitness(self):
        if self._fitness is None:
            route_unit = RouteUnit(self.to_route())

            too_many_segments = max(0, len(self.segments) - self.n_segments_reg_threshold)
            penalty_n_routes = N_SEGMENTS_REGULARIZATION * too_many_segments

            too_many_steps = max(0, sum([len(seg.from_to) for seg in self.segments]) - self.n_transitions_reg_threshold)
            penalty_segments_len = SEG_LENGTH_REGULARIZATION * too_many_steps

            self._fitness = route_unit.fitness - self.cities_not_visited() - penalty_n_routes - penalty_segments_len

        return self._fitness


    def mutate(self, mutation_rate: float):
        for mutating_segment in self.segments:
            mutating_segment.mutate(mutation_rate)
        self._fitness = None

    def _exchange_crossover(self, other: PiecewiseRoute) -> PiecewiseRoute:

        start, end = [], []

        while len(start) + len(end) == 0:
            crossover_point1 = random.randint(0, len(self.segments))
            p1_start, p1_end = self.segments[:crossover_point1], self.segments[crossover_point1:]

            crossover_point2 = random.randint(0, len(other.segments))
            p2_start, p2_end = other.segments[:crossover_point2], other.segments[crossover_point2:]

            start, end = random.choice( [(p1_start, p2_end), (p2_start, p1_end)] )


        new_route = PiecewiseRoute(start + end, self.all_cities)
        return new_route

    def _segments_crossover(self, other: PiecewiseRoute) -> PiecewiseRoute:

        p_crossover = 1 / len(self.segments)
        new_segments = []
        for seg in self.segments:
            if random.random() > p_crossover:
                seg2 = random.choice(other.segments)
                new_segments.append(seg.crossover(seg2))
            else:
                new_segments.append(seg)    # Imbalance: most pieces come from parent1

        return PiecewiseRoute(new_segments, self.all_cities)


    def crossover(self, other: PiecewiseRoute) -> PiecewiseRoute:
        if random.random() > 0.5:
            return self._segments_crossover(other)
        else:
            return self._exchange_crossover(other)





