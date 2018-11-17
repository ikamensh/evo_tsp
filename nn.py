# naive approach: nearest neighbour
import numpy as np

def nearest_neighbor_route(cities):
    '''returns total distance and route (type:list(City))'''
    visited=[]
    total_dist = 0
    cties = list(cities)
    idx = np.random.randint(0, len(cties))
    c = cties[idx]
    cties.remove(c)
    visited.append(c)
    
    while cties:
        nearest = min(cties, key= lambda x: c.distance(x))
        total_dist += c.distance(nearest)
        c = nearest
        visited.append(c)
        cties.remove(c)
    
    total_dist += visited[-1].distance(visited[0]) 
    
    return total_dist, visited