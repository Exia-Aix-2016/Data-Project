from halo import Halo
from PyInquirer import prompt


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
