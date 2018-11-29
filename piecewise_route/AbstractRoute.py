from __future__ import annotations
from typing import List
from City import City
import abc

class AbstractRoute:

    @property
    @abc.abstractmethod
    def fitness(self) -> float:
        pass

    @abc.abstractmethod
    def crossover(self, other: AbstractRoute) -> AbstractRoute:
        pass

    @abc.abstractmethod
    def mutate(self, mutation_rate: float) -> None:
        pass

    @staticmethod
    @abc.abstractmethod
    def create_route(cityList: List[City]) -> AbstractRoute:
        pass



