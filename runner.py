
from concurrent.futures import ThreadPoolExecutor
from generator import Generator
from cvrp import CVRP
import functools
from statistics import solution_stat, config_stat


class Runner():
    def __init__(self,  iterations=10, cities=None, cities_start=None, cities_stop=None, step=0.1, first_solution_strategy=None, local_search_metaheuristic=None, time_limit=10):
        self.iterations = iterations
        self.cities = cities
        self.cities_start = cities_start
        self.cities_stop = cities_stop
        self.time_limit = time_limit
        self.first_solution_strategy = first_solution_strategy
        self.local_search_metaheuristic = local_search_metaheuristic
        self.step = step
        self.executor = ThreadPoolExecutor()

    def get_solution_stats(self, data):
        solution = CVRP(data, self.first_solution_strategy,
                        self.local_search_metaheuristic, self.time_limit).get_solution()

        return solution_stat(solution) if solution else None

    def get_config_stats(self, generator):
        data = [
            generator.get_data() for i in range(self.iterations)
        ]

        solution_stats = filter(None, list(self.executor.map(
            self.get_solution_stats, data)))
        return config_stat(solution_stats, generator)

    def get_stats(self):
        if self.cities_start and self.cities_stop:
            step = int((self.cities_stop - self.cities_start) * self.step)

            generators = [
                Generator(i, int(i * 0.2), 16, 1, 5) for i in range(self.cities_start, self.cities_stop, step)
            ]
            return list(map(
                self.get_config_stats, generators))

        elif self.cities:
            return [self.get_config_stats(
                Generator(self.cities, int(self.cities * 0.2), 16, 1, 5))]
