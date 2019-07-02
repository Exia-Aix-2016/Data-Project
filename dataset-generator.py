from random import randrange
from datetime import datetime, time, timedelta
import math
import sys
import json


def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = [[0 for x in range(len(locations))]
                 for y in range(len(locations))]
    for from_counter, from_node in enumerate(locations):
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = (int(
                    math.hypot((from_node[0] - to_node[0]),
                               (from_node[1] - to_node[1]))))
    return distances


def generate_locations(n):
    locations = []
    for i in range(0, n):
        locations.append((
            randrange(0, 1000),
            randrange(0, 1000)
        ))
    return locations


def generate_demands(n, min, max):
    demands = [0]
    for i in range(0, n-1):
        demands.append(
            randrange(min, max)
        )
    return demands


def generate_vehicle_capacities(n, capacity):
    vehicle_capacities = []
    for i in range(0, int(n)):
        vehicle_capacities.append(capacity)
    return vehicle_capacities


def create_data_model():
    """Stores the data for the problem."""

    return data


def main(argv):
    filename = argv[0]
    cities = int(argv[1])
    trucks = int(float(argv[2]) * cities)
    truck_capacity = int(argv[3])
    city_demand_min = int(argv[4])
    city_demand_max = int(argv[5])

    print("Generating dataset with {} cities demanding {} to {} objects delivred by {} trucks of {} objects capacity".format(
        cities, city_demand_min, city_demand_max, trucks, truck_capacity))

    data = {}

    data['locations'] = generate_locations(cities)
    data['distance_matrix'] = compute_euclidean_distance_matrix(data['locations'])
    data['demands'] = generate_demands(
        cities, city_demand_min, city_demand_max)
    data['vehicle_capacities'] = generate_vehicle_capacities(
        trucks, truck_capacity)
    data['num_vehicles'] = len(data['vehicle_capacities'])
    data['depot'] = 0

    with open("datasets/{}.json".format(filename), 'w') as json_file:
        json.dump(data, json_file, indent=2)


if __name__ == "__main__":
    main(sys.argv[1:])
