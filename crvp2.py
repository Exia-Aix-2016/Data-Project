"""Capacited Vehicles Routing Problem (CVRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from datetime import datetime, time, timedelta
import sys
import json
from threading import Thread


class CVRP(Thread):
    solution = None

    def __init__(self, data, first_solution_strategy=None, local_search_metaheuristic=None, time_limit=None):
        Thread.__init__(self)
        self.data = data
        self.first_solution_strategy = first_solution_strategy
        self.local_search_metaheuristic = local_search_metaheuristic
        self.time_limit = time_limit

    def run(self):
        # Create the routing index manager.
        self.manager = pywrapcp.RoutingIndexManager(
            len(self.data['distance_matrix']), self.data['num_vehicles'], self.data['depot'])

        # Create Routing Model.
        self.routing = pywrapcp.RoutingModel(self.manager)

        # Create and register a transit callback.
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = self.manager.IndexToNode(from_index)
            to_node = self.manager.IndexToNode(to_index)
            return self.data['distance_matrix'][from_node][to_node]

        transit_callback_index = self.routing.RegisterTransitCallback(
            distance_callback)

        # Define cost of each arc.
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Capacity constraint.
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = self.manager.IndexToNode(from_index)
            return self.data['demands'][from_node]

        demand_callback_index = self.routing.RegisterUnaryTransitCallback(
            demand_callback)

        self.routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            self.data['vehicle_capacities'],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')

        self.search_parameters = pywrapcp.DefaultRoutingSearchParameters()

        if self.first_solution_strategy:
            self.search_parameters.first_solution_strategy = self.first_solution_strategy

        if self.local_search_metaheuristic:
            self.search_parameters.local_search_metaheuristic = self.local_search_metaheuristic

        if self.time_limit:
            self.search_parameters.time_limit.seconds = self.time_limit

        self.search_parameters.log_search = True

        startTime = datetime.now()

        # Solve the problem.
        assignment = self.routing.SolveWithParameters(self.search_parameters)

        elapsedTime = datetime.now() - startTime

        # Parse the solution.
        if assignment:
            self.solution = self.parse_solution(assignment)

        print(elapsedTime.total_seconds())

    def parse_solution(self, assignment):
        result = {
            "vehicles": [{
                "route": [],
                "distance": 0,
                "load": 0
            } for x in range(self.data['num_vehicles'])],
            "total_distance": 0,
            "total_load": 0,
            "trucks_fleet": 0,
        }

        for vehicle_id in range(self.data['num_vehicles']):
            index = self.routing.Start(vehicle_id)
            while not self.routing.IsEnd(index):
                node_index = self.manager.IndexToNode(index)
                previous_index = index
                index = assignment.Value(self.routing.NextVar(index))
                distance = self.routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)
                load = self.data['demands'][node_index]
                result["vehicles"][vehicle_id]["route"].append({
                    "id": node_index,
                    "load": load,
                    "distance": distance,
                    "location": self.data["locations"][node_index]
                })
                result["vehicles"][vehicle_id]["distance"] += distance
                result["vehicles"][vehicle_id]["load"] += load
                result["total_distance"] += distance
                result["total_load"] += load

        result["trucks_fleet"] += self.data['num_vehicles']

        return result
