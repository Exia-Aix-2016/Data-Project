from .menu import Menu
from .select_algo_menu import SelectAlgoMenu
from chart import Chart
from graph import Graph


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
