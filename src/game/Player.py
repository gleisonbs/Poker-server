class Player:
    def __init__(self, address):
        self.stack = 1000
        self.hand = []
        self.position = None
        self.current_bettings = 0
        self.address = address
        self.is_big_blind = False
        self.is_small_blind = False

    def __str__(self):
        return f'Player {self.position}: {self.hand}'

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
