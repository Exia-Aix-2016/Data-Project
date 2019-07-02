"""Capacited Vehicles Routing Problem (CVRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from datetime import datetime, time, timedelta
import sys
import json


def print_solution(data, manager, routing, assignment):
    """Prints assignment on console."""
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(
            manager.IndexToNode(index), route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))


def extract_solution(data, manager, routing, assignment):
    """Prints assignment on console."""
    result = {
        "vehicles": [{
            "route": [],
            "distance": 0,
            "load": 0
        } for x in range(data['num_vehicles'])],
        "total_distance": 0,
        "total_load": 0,
        "trucks_fleet": 0,
    }

    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            distance = routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
            load = data['demands'][node_index]
            result["vehicles"][vehicle_id]["route"].append({
                "id": node_index,
                "load": load,
                "distance": distance,
                "location": data["locations"][node_index]
            })
            result["vehicles"][vehicle_id]["distance"] += distance
            result["vehicles"][vehicle_id]["load"] += load
            result["total_distance"] += distance
            result["total_load"] += load

    result["trucks_fleet"] += data['num_vehicles']

    return result


def main(argv):
    """Solve the CVRP problem."""

    # Instantiate the data problem.
    with open("datasets/{}.json".format(argv[0]), 'r') as json_file:
        data = json.load(json_file)

    with open("algorithms.json".format(argv[1]), 'r') as json_file:
        algorithms = json.load(json_file)
        algorithm = [algorithms['algorithms']
                     [int(argv[1])], algorithms['heuristique'][int(argv[1])]]

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.

    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    if algorithm[1] == "True":
        search_parameters.first_solution_strategy = (
            eval("routing_enums_pb2.FirstSolutionStrategy." + algorithm[0]))
    else:
        search_parameters.local_search_metaheuristic = (
            eval("routing_enums_pb2.LocalSearchMetaheuristic." + algorithm[0]))
        search_parameters.time_limit.seconds = 5

    search_parameters.log_search = True

    startTime = datetime.now()
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)
    elapsedTime = datetime.now() - startTime

    # Print solution on console.
    if assignment:
        solution = extract_solution(data, manager, routing, assignment)
        with open("results/{}_{}.json".format(argv[0], algorithm[0]), 'w') as json_file:
            json.dump(solution, json_file, indent=2)

    print(elapsedTime.total_seconds())


if __name__ == "__main__":
    main(sys.argv[1:])
