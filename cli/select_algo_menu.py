
from .menu import Menu


class SelectAlgoMenu(Menu):
    def get_choices(self):
        return [
            {"name": "GUIDED_LOCAL_SEARCH", "value": "GUIDED_LOCAL_SEARCH"},
            {"name": "TABU_SEARCH", "value": "TABU_SEARCH"},
            {"name": "PATH_CHEAPEST_ARC", "value": "PATH_CHEAPEST_ARC"}
        ]

    def on_action(self, action):
        self.store.sid = action
