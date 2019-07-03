
from concurrent.futures import ThreadPoolExecutor
from generator import Generator
from cvrpg import CVRPG
from functools import reduce


class Complexity():
    def __init__(self, cities_start, cities_stop, step=0.1):
        self.cities_start = cities_start
        self.cities_stop = cities_stop
        self.step = int((cities_stop - cities_start) * step)
        self.executor = ThreadPoolExecutor()

    def get_complexity_snap(self, cities):
        data = Generator(cities, int(cities * 0.2), 16, 1, 5).get_data()
        solutions = CVRPG(data, 10).get_solutions()
        return {
            algo: {"duration": solution["execution_time"], "cities": cities} for algo, solution in solutions.items()
        }

    def get_complexity(self):
        complexity_snaps = self.executor.map(self.get_complexity_snap, range(
            self.cities_start, self.cities_stop, self.step))

        complexity = {}

        for complexity_snap in complexity_snaps:
            for algo, c in complexity_snap.items():
                if complexity.get(algo) == None:
                    complexity[algo] = []
                complexity[algo].append(c)

        return complexity
