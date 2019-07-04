from PyInquirer import prompt
from .menu import Menu
from .utils import NumberValidator, toInt
from generator import Generator
import json


class FileMenu(Menu):
    def __init__(self, store, property, property_name):
        Menu.__init__(self, store)
        self.property = property
        self.property_name = property_name

    def get_choices(self):
        choices = [{
            "name": "Generate {}".format(self.property_name),
            "value": "generate"
        }, {
            "name": "Import {}".format(self.property_name),
            "value": "import"
        }]

        if getattr(self.store, self.property):
            choices.append({
                "name": "Export {}".format(self.property_name),
                "value": "export"
            })

        return choices

    def on_action(self, action):
        if action == "generate":
            self.on_generate()
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
                    setattr(self.store, self.property, json.load(json_file))
            else:
                with open(filename, 'w') as json_file:
                    json.dump(getattr(self.store, self.property),
                              json_file, indent=2)

    def on_generate(self):
        raise NotImplementedError("on_generate must be implemented")
