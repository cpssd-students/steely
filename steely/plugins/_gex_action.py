'''Actions and powerups for during gex battles.'''


class BattleAction:

    def __init__(self, cost):
        self.cost = cost

    def is_possible(self, competitor_data):
        return competitor_data['power'] >= self.get_cost()

    def execute(self, competitor_data):
        competitor_data['power'] -= self.get_cost()
        return competitor_data

    def get_cost(self):
        return self.cost


class SwapAction(BattleAction):

    def __init__(self):
        super().__init__(2)

    def is_possible(self, competitor_data):
        if not super().is_possible(competitor_data):
            return False
        return len(competitor_data['deck']) >= 2

    def execute(self, competitor_data):
        competitor_data = super().execute(competitor_data)
        d = competitor_data['deck']
        d[0], d[1] = d[1], d[0]
        competitor_data['deck'] = d
        return competitor_data

actions = {
    'swap': SwapAction(),
}


def get_actions():
    return actions
