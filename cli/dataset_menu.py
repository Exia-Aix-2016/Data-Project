from PyInquirer import prompt
from .menu import Menu
from .utils import NumberValidator, toInt
from generator import Generator
import json
from .file_menu import FileMenu


class DatasetMenu(FileMenu):
    def __init__(self, store):
        FileMenu.__init__(self, store, "data", "a dataset")

    def on_generate(self):
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
