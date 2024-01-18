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
        return f'Player {self.nickname} ({"Dealer" if self.position == 0 else self.position}) {self.hand} - Stack {self.stack}'
    
    def __repr__(self):
        return f'Player {self.nickname} ({"Dealer" if self.position == 0 else self.position}) {self.hand} - Stack {self.stack}'

    def has_enough_funds(self, amount):
        return self.stack >= amount

    def post_big_blind(self, bb_size):
        self.stack -= bb_size
        self.current_bettings += bb_size
        return bb_size

    def post_small_blind(self, sb_size):
        self.stack -= sb_size
        self.current_bettings += sb_size
        return sb_size

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

    def bet(self, value):
        self.stack -= value
        self.current_bettings += value
        return value

    def raise_bet(self, value):
        value -= self.current_bettings
        self.stack -= value
        self.current_bettings += value
        return value

    def get_action(self, call_amount, current_bet_amount = 0):
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

        while action not in allowed_actions:
            action = input()
        return action.upper()
        
