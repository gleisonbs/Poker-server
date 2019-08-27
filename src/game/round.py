from enum import Enum
from player import Player

class BettingRound(Enum):
    PRE_FLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3

class Round:
    def __init__(self):
        self.bettingRound = BettingRound.PRE_FLOP
        self.players = []
        self.cards_drawn = []