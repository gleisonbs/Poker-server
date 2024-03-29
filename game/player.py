from game.enums.two_game_positions import TwoGamePositions


class Player:
    def __init__(self, connection, nickname=''):
        self.connection = connection
        self.nickname = nickname
        self.stack = 1000
        self.hand = []
        self.position = None
        self.current_bettings = 0
        self.is_big_blind = False
        self.is_small_blind = False

    def __str__(self):
        return f'Player ({TwoGamePositions(self.position).name}) {self.hand} - Stack {self.stack}'

    def __repr__(self):
        return f'Player ({TwoGamePositions(self.position).name}) {self.hand} - Stack {self.stack}'

    def has_enough_funds(self, amount):
        return self.stack >= amount

    def post_blind(self, blind_size):
        self.stack -= blind_size
        self.current_bettings += blind_size
        return blind_size

#    def fold(self):
#        pass
#
#    def check(self):
#        pass
#
    def call(self, value):
        self.stack -= value
        self.current_bettings += value
        return value

    def bet(self, amount):
        self.stack -= amount
        self.current_bettings += amount
        return amount

    def raise_bet(self, amount):
        self.stack -= amount
        self.current_bettings += amount
        return amount

    def get_action(self, call_amount, current_bet_amount):
        action = None
        allowed_actions = ['fold']
        if call_amount > 0:
            allowed_actions.append('call')
        else:
            allowed_actions.append('check')

        if self.stack > 0:
            if current_bet_amount:
                allowed_actions.append('raise')
            else:
                allowed_actions.append('bet')

        print('allowed_actions', call_amount, allowed_actions)
        while action not in allowed_actions:
            action_and_amount = input()
            print('action_and_amount', action_and_amount)
            action_and_amount = action_and_amount.split(' ')
            if len(action_and_amount) > 1:
                action, amount = action_and_amount
                amount = float(amount)
            else:
                action = action_and_amount[0]
                amount = 0
        return action.upper(), amount
