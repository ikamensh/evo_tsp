import math
import random
from siman.visualize_sa import plotTSP
import matplotlib.pyplot as plt
from typing import List
from City import City
from RouteUnit import RouteUnit


class SimAnneal:
    def __init__(self, cities: List[City], T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        self.cities = cities
        self.N = len(cities)
        self.T = math.sqrt(self.N) if T == -1 else T
        self.alpha = 0.995 if alpha == -1 else alpha
        self.stopping_temperature = 0.00000001 if stopping_T == -1 else stopping_T
        self.stopping_iter = 100000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1

        self.cur_solution = self.initial_solution()
        self.best_solution = list(self.cur_solution) # make copy

        self.cur_fitness = RouteUnit.route_distance(self.cur_solution)
        self.initial_fitness = self.cur_fitness
        self.best_fitness = self.cur_fitness

        self.fitness_list = [self.cur_fitness]

    def initial_solution(self):
        """
        Greedy algorithm to get an initial solution (closest-neighbour)
        """
        start = random.choice(self.cities)
        solution: List[City] = [start]

        free_list = list(self.cities)
        free_list.remove(start)

        while free_list:
            closest_city = min(free_list, key=lambda x: solution[-1].distance(x))
            free_list.remove(closest_city)
            solution.append(closest_city)

        return solution


    def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current
        Depends on the current temperature and difference between candidate and current
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current
        Accept with probabilty p_accept(..) if candidate is worse
        """
        candidate_fitness = RouteUnit.route_distance(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness = candidate_fitness
            self.cur_solution = candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness = candidate_fitness
                self.best_solution = candidate

        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.cur_fitness = candidate_fitness
                self.cur_solution = candidate

    def anneal(self):
        """
        Execute simulated annealing algorithm
        """
        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:
            candidate = list(self.cur_solution)
            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)
            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
            self.accept(candidate)
            self.T *= self.alpha
            self.iteration += 1

            self.fitness_list.append(self.cur_fitness)

        print('Best fitness obtained: ', self.best_fitness)
        print('Improvement over greedy heuristic: ',
              round((self.initial_fitness - self.best_fitness) / (self.initial_fitness), 4))

    def visualize_routes(self):
        """
        Visualize the TSP route with matplotlib
        """
        plotTSP([self.best_solution])

    def plot_learning(self):
        """
        Plot the fitness through iterations
        """
        plt.plot([i for i in range(len(self.fitness_list))], self.fitness_list)
        plt.ylabel('Fitness')
        plt.xlabel('Iteration')
        plt.show()