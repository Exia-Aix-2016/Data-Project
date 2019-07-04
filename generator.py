import time
from random import randrange
from datetime import datetime, time, timedelta
import math
import sys
import json
from ortools.constraint_solver import routing_enums_pb2


class Generator:
    def __init__(self, cities, trucks, truck_capacity, city_demand_min, city_demand_max):
        self.cities = cities
        self.trucks = trucks
        self.truck_capacity = truck_capacity
        self.city_demand_min = city_demand_min
        self.city_demand_max = city_demand_max

    def get_data(self):
        data = {}

        data['locations'] = []
        for i in range(self.cities):
            data['locations'].append((
                randrange(0, 1000),
                randrange(0, 1000)
            ))

        data['distance_matrix'] = [[0 for x in range(self.cities)]
                                   for y in range(self.cities)]
        for from_counter, from_node in enumerate(data['locations']):
            for to_counter, to_node in enumerate(data['locations']):
                if from_counter == to_counter:
                    data['distance_matrix'][from_counter][to_counter] = 0
                else:
                    data['distance_matrix'][from_counter][to_counter] = (int(
                        math.hypot((from_node[0] - to_node[0]),
                                   (from_node[1] - to_node[1]))))

        data['demands'] = [0]
        for i in range(self.cities-1):
            data['demands'].append(
                randrange(self.city_demand_min, self.city_demand_max)
            )

        data['vehicle_capacities'] = []
        for i in range(self.trucks):
            data['vehicle_capacities'].append(self.truck_capacity)

        data['num_vehicles'] = self.trucks
        data['depot'] = 0

        return data
