import game.card
import random

class Deck:
    suits = 'shcd'
    ranks = '23456789TJQKA'

    def __init__(self):
        self.deck = [f'{r}{s}' for s in Deck.suits
                               for r in Deck.ranks]

    def draw_cards(self, quantity):
        return [self.deck.pop() for _ in range(quantity)]

    def shuffle(self):
        random.shuffle(self.deck)