class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank}{self.suit}'

