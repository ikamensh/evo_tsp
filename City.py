import numpy as np
import random
from functools import lru_cache

np.random.seed(1)
class City:
    def __init__(self, ndim):
        self.coordinates = np.random.random(size=[ndim])

    @lru_cache(maxsize=int(2**20))
    def distance(self, city):
        return np.linalg.norm(self.coordinates - city.coordinates)

    def __repr__(self):
        return  f"City at {str(self.coordinates)}"



cities = [City(ndim=2) for i in range(60)]