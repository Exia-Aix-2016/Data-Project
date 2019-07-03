import time
from random import randrange
from datetime import datetime, time, timedelta
import math
import sys
import json
from ortools.constraint_solver import routing_enums_pb2
from threading import Thread


class Generator(Thread):
    data = None

    def __init__(self, cities, trucks, truck_capacity, city_demand_min, city_demand_max):
        Thread.__init__(self)
        self.cities = cities
        self.trucks = trucks
        self.truck_capacity = truck_capacity
        self.city_demand_min = city_demand_min
        self.city_demand_max = city_demand_max

    def run(self):
        self.data = {}

        self.data['locations'] = []
        for i in range(self.cities):
            self.data['locations'].append((
                randrange(0, 1000),
                randrange(0, 1000)
            ))

        self.data['distance_matrix'] = [[0 for x in range(self.cities)]
                                        for y in range(self.cities)]
        for from_counter, from_node in enumerate(self.data['locations']):
            for to_counter, to_node in enumerate(self.data['locations']):
                if from_counter == to_counter:
                    self.data['distance_matrix'][from_counter][to_counter] = 0
                else:
                    self.data['distance_matrix'][from_counter][to_counter] = (int(
                        math.hypot((from_node[0] - to_node[0]),
                                   (from_node[1] - to_node[1]))))

        self.data['demands'] = [0]
        for i in range(self.cities-1):
            self.data['demands'].append(
                randrange(self.city_demand_min, self.city_demand_max)
            )

        self.data['vehicle_capacities'] = []
        for i in range(self.trucks):
            self.data['vehicle_capacities'].append(self.truck_capacity)

        self.data['num_vehicles'] = self.trucks
        self.data['depot'] = 0
