import random

class RouteRLAgent:
    def __init__(self):
        self.q_table = {}

    def select_optimal_mode(self, state_dict):
        # actions: [fastest_road, cheapest_road, air, sea, rail, multimodal]
        actions = ['fastest_road', 'cheapest_road', 'air', 'sea', 'rail', 'multimodal']
        best_act = random.choice(actions)
        return best_act, 0.90
