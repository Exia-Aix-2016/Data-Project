from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from PyInquirer import Validator, ValidationError
from halo import Halo
import time
import asyncio
from threading import Thread
from ortools.constraint_solver import routing_enums_pb2
from generator import Generator
from graph import Graph
import json
from chart import Chart
from cvrpg import CVRPG
from complexity import Complexity
from runner import Runner


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


def toFloat(val): return float(val)


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


class Menu():
    spinner = Halo(text='Loading', spinner='dots')
    store = None

    def __init__(self, store, loop=False):
        self.store = store
        self.loop = loop

    def execute(self):
        while True:
            choices = self.get_choices()
            choices.append({
                'name': "Exit",
                'value': "exit"
            })

            answers = prompt({
                'type': 'list',
                'name': 'menu',
                'message': 'What do you want to do?',
                'choices': choices
            })

            if answers["menu"] == "exit":
                return

            self.on_action(answers["menu"])

            if not self.loop:
                break

    def on_action(self, action):
        raise NotImplementedError("Must override on_action")

    def get_choices(self):
        raise NotImplementedError("Must override get_choices")


class DatasetMenu(Menu):
    def get_choices(self):
        choices = [{
            "name": "Generate a dataset",
            "value": "generate"
        }, {
            "name": "Import a dataset",
            "value": "import"
        }]

        if self.store.data:
            choices.append({
                "name": "Export a dataset",
                "value": "export"
            })

        return choices

    def on_action(self, action):
        if action == "generate":
            answers = prompt([
                {
                    'type': 'input',
                    'name': 'cities',
                    'message': 'How many cities do you want ?',
                    'validate': NumberValidator,
                    'filter': toInt,
                },    {
                    'type': 'input',
                    'name': 'trucks',
                    'message': 'How many trucks do you want ?',
                    'validate': NumberValidator,
                    'filter': toInt,
                },    {
                    'type': 'input',
                    'name': 'truck_capacity',
                    'message': 'How much a truck can hold ?',
                    'validate': NumberValidator,
                    'filter': toInt,
                    'default': "15"
                },    {
                    'type': 'input',
                    'name': 'city_demand_min',
                    'message': 'Min city demand ?',
                    'validate': NumberValidator,
                    'filter': toInt,
                    'default': "1"
                },    {
                    'type': 'input',
                    'name': 'city_demand_max',
                    'message': 'Max city demand ?',
                    'validate': NumberValidator,
                    'filter': toInt,
                    'default': "5"
                }
            ])

            with self.spinner:
                self.store.data = Generator(answers["cities"],
                                            answers["trucks"],
                                            answers["truck_capacity"],
                                            answers["city_demand_min"],
                                            answers["city_demand_max"]).get_data()

        elif action == "import" or action == "export":
            filename = prompt([
                {
                    'type': 'input',
                    'name': 'filename',
                    'message': 'What file ?'
                }
            ])["filename"]

            if action == "import":

                with open(filename, 'r') as json_file:
                    self.store.data = json.load(json_file)
            else:
                with open(filename, 'w') as json_file:
                    json.dump(self.store.data, json_file, indent=2)


class SelectAlgoMenu(Menu):
    def get_choices(self):
        return [
            {"name": "GUIDED_LOCAL_SEARCH", "value": "GUIDED_LOCAL_SEARCH"},
            {"name": "TABU_SEARCH", "value": "TABU_SEARCH"},
            {"name": "PATH_CHEAPEST_ARC", "value": "PATH_CHEAPEST_ARC"}
        ]

    def on_action(self, action):
        self.store.sid = action


class VisualizationMenu(Menu):

    def __init__(self, store):
        Menu.__init__(self, store)
        self.selectAlgoMenu = SelectAlgoMenu(store)
        self.chart = Chart(store)

    def get_choices(self):
        choices = []
        if self.store.solutions:
            choices.append({
                'name': 'Graph',
                'value': 'GRAPH'
            })
            choices.append({
                'name': 'Graph without depot',
                'value': 'GRAPH_NO_DEPOT'
            })
            choices.append({
                'name': 'Quality chart',
                'value': 'QUALITY_CHART'
            })

        if self.store.complexity:
            choices.append({
                'name': 'Complexity chart',
                'value': 'COMPLEXITY_CHART'
            })

        return choices

    def on_action(self, action):
        if action == "GRAPH" or action == "GRAPH_NO_DEPOT":
            self.selectAlgoMenu.execute()
            graph = Graph(
                self.store.solutions[self.store.sid], showDepotEdges=(action == "GRAPH"))
            graph.show()
        elif action == "QUALITY_CHART":
            self.chart.showQuality()
        elif action == "COMPLEXITY_CHART":
            self.chart.showComplexity()


class StatMenu(Menu):
    def __init__(self, store):
        Menu.__init__(self, store)
        self.selectAlgoMenu = SelectAlgoMenu(store)
        self.chart = Chart(store)

    def get_choices(self):
        return [
            {
                'name': 'Show scatter plot',
                'value': 'SCATTER_PLOT'
            },
            {
                'name': 'Show uniformity',
                'value': 'UNIFORMITY'
            }
        ]

        # choices = [{
        #     'name': 'Generate stats',
        #     'value': 'GENERATE'
        # }]

        # if self.store.stats:
        #     choices.append({
        #         'name': 'Show scatter plot',
        #         'value': 'SCATTER_PLOT'
        #     })

    def on_action(self, action):
        if action == "SCATTER_PLOT":
            self.selectAlgoMenu.execute()
            with self.spinner:
                stats = Runner(iterations=3, cities_start=10, cities_stop=200, local_search_metaheuristic=self.store.local_search_metaheuristic(
                ), first_solution_strategy=self.store.first_solution_strategy()).get_stats()
            self.chart.showScatterPlot(stats)
        elif action == "UNIFORMITY":
            self.selectAlgoMenu.execute()
            with self.spinner:
                stats = Runner(cities=500, local_search_metaheuristic=self.store.local_search_metaheuristic(
                ), first_solution_strategy=self.store.first_solution_strategy()).get_stats()
            self.chart.showUniformity(stats[0])


class MainMenu(Menu):

    def __init__(self, store):
        Menu.__init__(self, store, loop=True)
        self.datasetMenu = DatasetMenu(store)
        self.visualizationMenu = VisualizationMenu(store)
        self.statMenu = StatMenu(store)

    def get_choices(self):
        choices = [{
            'name': 'Manage dataset',
            'value': 'dataset',
        }]

        if self.store.data:
            choices.append({
                'name': 'Find a solution',
                'value': 'process',
            })

        choices.append({
            'name': 'Find a complexity',
            'value': 'complexity',
        })

        if self.store.solutions or self.store.complexity:
            choices.append({
                'name': 'Visualize the solution',
                'value': 'visualize',
            })

        choices.append({
            'name': 'Stats',
            'value': 'stats',
        })

        return choices

    def on_action(self, action):
        if action == "dataset":
            self.datasetMenu.execute()
        if action == "process":
            with self.spinner:
                self.store.solutions = CVRPG(
                    self.store.data, 5).get_solutions()
        if action == "visualize":
            self.visualizationMenu.execute()
        if action == "complexity":
            answers = prompt([
                {
                    "type": "input",
                    "message": "How many cities do you want from ?",
                    "name": "city_start",
                    "filter": toInt
                }, {
                    "type": "input",
                    "message": "How many cities do you want to ?",
                    "name": "city_stop",
                    "filter": toInt
                }, {
                    "type": "input",
                    "message": "Which step ratio ?",
                    "name": "step",
                    "default": "0.1",
                    "filter": toFloat
                }, {
                    "type": "input",
                    "message": "Which time limit ?",
                    "name": "time_limit",
                    "default": "60",
                    "filter": toInt
                }
            ])
            with self.spinner:
                self.store.complexity = Complexity(
                    answers["city_start"], answers["city_stop"], answers["step"], answers["time_limit"]).get_complexity()
        elif action == "stats":
            self.statMenu.execute()


if __name__ == "__main__":
    store = Store()
    mainMenu = MainMenu(store)
    mainMenu.execute()
