from typing import List, Dict
from City import City


def percent_common_route(r1: List[City], r2: List[City]):
    moves_1 = {(r1[i], r1[i + 1]) for i in range(len(r1) - 1)}
    moves_1.add((r1[-1], r1[0]))
    moves_2 = {(r2[i], r2[i + 1]) for i in range(len(r2) - 1)}
    moves_2.add((r2[-1], r2[0]))

    return 2 * len(moves_1.intersection(moves_2)) / (len(moves_1) + len(moves_2))