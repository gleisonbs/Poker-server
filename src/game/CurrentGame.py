from BettingRound import BettingRound, BettingRoundName

class CurrentGame:
    def __init__(self, players):
        self.rounds = []
        self.players = players
        self.pot = 0
    
    def finish_round(self):
        return self.rounds.pop(0)

    def add_to_pot(self, amount):
        self.pot = amount

    def remove_player(self, player):
        self.players.remove(player)

