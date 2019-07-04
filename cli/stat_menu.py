from PyInquirer import prompt
from .menu import Menu
from .utils import toInt, toFloat, NumberValidator
from .select_algo_menu import SelectAlgoMenu
from chart import Chart
from runner import Runner


ITERATION_QUESTION = {
    'type': 'input',
    'name': 'iterations',
    'message': 'How many iterations do you want ?',
    'validate': NumberValidator,
    'filter': toInt,
}

STEP_QUESTION = {
    'type': 'input',
    'name': 'step',
    'message': 'Step spacing ratio ?',
    'filter': toFloat,
    'default': "0.1"
}

TIME_LIMIT_QUESTION = {
    'type': 'input',
    'name': 'time_limit',
    'message': 'Time limit  ?',
    'validate': NumberValidator,
    'filter': toInt,
    "default": "30"
}


UNIFORMITY_QUESTIONS = [{
    'type': 'input',
    'name': 'cities',
    'message': 'How many cities do you want ?',
    'validate': NumberValidator,
    'filter': toInt,
},
    ITERATION_QUESTION, TIME_LIMIT_QUESTION]

SCATTER_PLOT_QUESTIONS = [{
    'type': 'input',
    'name': 'cities_start',
    'message': 'How many cities to start ?',
    'validate': NumberValidator,
    'filter': toInt,
}, {
    'type': 'input',
    'name': 'cities_stop',
    'message': 'How many cities to stop ?',
    'validate': NumberValidator,
    'filter': toInt,
}, ITERATION_QUESTION, STEP_QUESTION, TIME_LIMIT_QUESTION]


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

    def on_action(self, action):
        self.selectAlgoMenu.execute()
        if action == "SCATTER_PLOT":
            answers = prompt(SCATTER_PLOT_QUESTIONS)
            with self.spinner:
                stats = Runner(iterations=answers["iterations"], cities_start=answers["cities_start"], cities_stop=answers["cities_stop"], step=answers["step"], time_limit=answers["time_limit"], local_search_metaheuristic=self.store.local_search_metaheuristic(
                ), first_solution_strategy=self.store.first_solution_strategy()).get_stats()
            self.chart.showScatterPlot(stats)
        elif action == "UNIFORMITY":
            answers = prompt(UNIFORMITY_QUESTIONS)
            with self.spinner:
                stats = Runner(iterations=answers["iterations"], cities=answers["cities"], time_limit=answers["time_limit"], local_search_metaheuristic=self.store.local_search_metaheuristic(
                ), first_solution_strategy=self.store.first_solution_strategy()).get_stats()
            self.chart.showUniformity(stats[0])
