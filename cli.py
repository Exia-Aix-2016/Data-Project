from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from PyInquirer import Validator, ValidationError
from halo import Halo
import time
from generator import generate_data
import asyncio
from threading import Thread
from crvp2 import CVRP
from ortools.constraint_solver import routing_enums_pb2


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


def whenMenu(m):
    return lambda answers: answers['menu'] == m


def toInt(val): return int(val)


class Cli:

    data = None

    solutions = None

    spinner = Halo(text='Loading', spinner='dots')

    def getQuestions(self):

        choices = [{
            'name': 'Generate a dataset',
                    'value': 'generate',
        }]

        if self.data:
            choices.append({
                'name': 'Find a solution',
                'value': 'process',
            })

        if self.solutions:
            choices.append({
                'name': 'Visualize the solution',
                'value': 'visualize',
            })

        choices.append({
            'name': "Exit",
            'value': "exit"
        })

        return [
            {
                'type': 'list',
                'name': 'menu',
                'message': 'What do you want to do?',
                'choices': choices
            },
            {
                'type': 'input',
                'name': 'cities',
                'message': 'How many cities do you want ?',
                'validate': NumberValidator,
                'filter': toInt,
                'when': whenMenu("generate")
            },    {
                'type': 'input',
                'name': 'trucks',
                'message': 'How many trucks do you want ?',
                'validate': NumberValidator,
                'filter': toInt,
                'when': whenMenu("generate")
            },    {
                'type': 'input',
                'name': 'truck_capacity',
                'message': 'How much a truck can hold ?',
                'validate': NumberValidator,
                'filter': toInt,
                'when': whenMenu("generate"),
                'default': "15"
            },    {
                'type': 'input',
                'name': 'city_demand_min',
                'message': 'Min city demand ?',
                'validate': NumberValidator,
                'filter': toInt,
                'when': whenMenu("generate"),
                'default': "1"
            },    {
                'type': 'input',
                'name': 'city_demand_max',
                'message': 'Max city demand ?',
                'validate': NumberValidator,
                'filter': toInt,
                'when': whenMenu("generate"),
                'default': "5"
            },
        ]

    def run(self):
        while True:
            answers = prompt(self.getQuestions())

            if answers["menu"] == "exit":
                break
            elif answers["menu"] == "generate":
                with self.spinner:
                    self.data = generate_data(answers["cities"],
                                              answers["trucks"],
                                              answers["truck_capacity"],
                                              answers["city_demand_min"],
                                              answers["city_demand_max"])
            elif answers["menu"] == "process":
                crvp1 = CVRP(
                    self.data, local_search_metaheuristic=routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH, time_limit=120)
                crvp2 = CVRP(
                    self.data, local_search_metaheuristic=routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH, time_limit=120)
                crvp3 = CVRP(
                    self.data, first_solution_strategy=routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
                crvp1.start()
                crvp2.start()
                crvp3.start()
                with self.spinner:
                    crvp1.join()
                    crvp2.join()
                    crvp3.join()
                self.solutions = [crvp1.solution,
                                  crvp2.solution, crvp3.solution]


if __name__ == "__main__":
    cli = Cli()
    cli.run()
