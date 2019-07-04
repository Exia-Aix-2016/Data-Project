from PyInquirer import prompt
from .menu import Menu
from .utils import NumberValidator, toInt
from generator import Generator
import json
from .file_menu import FileMenu
from cvrpg import CVRPG


class SolutionMenu(FileMenu):
    def __init__(self, store):
        FileMenu.__init__(self, store, "solutions", "solutions")

    def on_generate(self):
        answers = prompt([{
            "type": "input",
            "message": "Which time limit ?",
            "name": "time_limit",
            "default": "10",
            "filter": toInt
        }])
        with self.spinner:
            self.store.solutions = CVRPG(
                self.store.data, answers["time_limit"]).get_solutions()
