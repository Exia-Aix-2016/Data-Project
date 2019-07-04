from ortools.constraint_solver import routing_enums_pb2


class Store:
    data = None
    solutions = None
    sid = None
    complexity = None
    stats = None

    def first_solution_strategy(self):
        if self.sid == "PATH_CHEAPEST_ARC":
            return routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    def local_search_metaheuristic(self):
        if self.sid == "GUIDED_LOCAL_SEARCH":
            return routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        elif self.sid == "TABU_SEARCH":
            return routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH
