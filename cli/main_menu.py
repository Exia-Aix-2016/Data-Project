from PyInquirer import prompt
from .menu import Menu
from .utils import toInt, toFloat
from .dataset_menu import DatasetMenu
from .visualization_menu import VisualizationMenu
from .stat_menu import StatMenu
from .solution_menu import SolutionMenu
from cvrpg import CVRPG
from complexity import Complexity


class MainMenu(Menu):

    def __init__(self, store):
        Menu.__init__(self, store, loop=True)
        self.datasetMenu = DatasetMenu(store)
        self.solutionMenu = SolutionMenu(store)
        self.visualizationMenu = VisualizationMenu(store)
        self.statMenu = StatMenu(store)

    def get_choices(self):
        choices = [{
            'name': 'Manage dataset',
            'value': 'dataset',
        }, {
            'name': 'Manage solutions',
            'value': 'solutions',
        }]

        # if self.store.data:
        #     choices.append({
        #         'name': 'Find a solution',
        #         'value': 'process',
        #     })

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
        elif action == "solutions":
            self.solutionMenu.execute()
        elif action == "visualize":
            self.visualizationMenu.execute()
        elif action == "complexity":
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
