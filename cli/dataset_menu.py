from PyInquirer import prompt
from .menu import Menu
from .utils import NumberValidator, toInt
from generator import Generator
import json


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
