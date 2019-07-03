from concurrent.futures import ThreadPoolExecutor
from ortools.constraint_solver import routing_enums_pb2
from cvrp import CVRP


class CVRPG:
    def __init__(self, data, time_limit=60):
        self.data = data
        self.time_limit = time_limit
        self.executor = ThreadPoolExecutor()

    def get_solutions(self):
        cvrps = {
            "GUIDED_LOCAL_SEARCH": CVRP(
                self.data, local_search_metaheuristic=routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH, time_limit=self.time_limit),
            "TABU_SEARCH": CVRP(
                self.data, local_search_metaheuristic=routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH, time_limit=self.time_limit),
            "PATH_CHEAPEST_ARC": CVRP(
                self.data, first_solution_strategy=routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        }

        future_solutions = {}
        for key, cvrp in cvrps.items():
            future_solutions[key] = self.executor.submit(cvrp.get_solution)

        solutions = {}
        for key, future_solution in future_solutions.items():
            solutions[key] = future_solution.result()

        return solutions
