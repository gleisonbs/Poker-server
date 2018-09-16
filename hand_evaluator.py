__author__ = 'cafeina'

from itertools import combinations

class HandEvaluator:
    def __init__(self):
        self.hands_table = HandEvaluator.__HandsTable()

    def evaluate(self, hand):
        prime_hand = 1
        suit = hand[0][1]
        if hand[1][1] == suit and hand[2][1] == suit and hand[3][1] == suit and hand[4][1] == suit:
            prime_hand *= self.hands_table.prime_flush

        for card in hand:
            prime_hand *= self.hands_table.prime_cards[card[0]]

        hand_info = self.hands_table.all_hands[prime_hand]
        return hand_info

    class __HandsTable:
        def __init__(self):
            self.cards = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
            self.prime_cards = {"2": 2, "3": 3, "4": 5, "5": 7, "6": 11, "7": 13, "8": 17, "9": 19, "T": 23, "J": 29,
                                "Q": 31, "K": 37, "A": 41}
            self.prime_flush = 43
            self.all_hands = {}
            self.generate()

        def generate(self):
            self.straight(is_straight_flush=True)
            self.four_of_a_kind()
            self.full_house()
            self.high_card(is_flush=True)
            self.straight()
            self.three_of_a_kind()
            self.two_pairs()
            self.one_pair()
            self.high_card()

        def straight(self, is_straight_flush=False):
            counter = 10
            start = -1
            while counter:
                for c1 in self.cards[start::-1]:
                    for c2 in self.cards[start - 1::-1]:
                        for c3 in self.cards[start - 2::-1]:
                            for c4 in self.cards[start - 3::-1]:
                                for c5 in self.cards[start - 4::-1]:
                                    hand = c1 + c2 + c3 + c4 + c5
                                    if is_straight_flush:
                                        hand += "F"
                                    self.add_hands_to_table(hand)
                                    break
                                break
                            break
                        break
                    break
                start -= 1
                counter -= 1

        def four_of_a_kind(self):
            for c1 in self.cards[:0:-1]:
                for c2 in self.cards[:0:-1]:
                    if c1 == c2:
                        continue
                    hand = (c1 * 4) + c2
                    self.add_hands_to_table(hand)

        def full_house(self):
            for c1 in self.cards[:0:-1]:
                for c2 in self.cards[:0:-1]:
                    if c1 == c2:
                        continue
                    hand = (c1 * 3) + (c2 * 2)
                    self.add_hands_to_table(hand)

        def high_card(self, is_flush=False):
            for tuple_hand in list(combinations(self.cards[:0:-1], 5)):
                hand = ''.join([card for card in tuple_hand])
                if is_flush:
                    hand += "F"
                self.add_hands_to_table(hand)


        def three_of_a_kind(self):
            for c1 in self.cards[:0:-1]:
                for c2 in self.cards[:0:-1]:
                    for c3 in self.cards[:0:-1]:
                        if c2 == c3 or c1 == c2 or c1 == c3:
                            continue
                        hand = (c1 * 3) + c2 + c3
                        self.add_hands_to_table(hand)

        def two_pairs(self):
            for c1 in self.cards[:0:-1]:
                for c2 in self.cards[:0:-1]:
                    for c3 in self.cards[:0:-1]:
                        if c2 == c3 or c1 == c2 or c1 == c3:
                            continue
                        hand = (c1 * 2) + (c2 * 2) + c3
                        self.add_hands_to_table(hand)

        def one_pair(self):
            for c1 in self.cards[:0:-1]:
                for c2 in self.cards[:0:-1]:
                    for c3 in self.cards[:0:-1]:
                        for c4 in self.cards[:0:-1]:
                            if c1 == c2 or c1 == c3 or c1 == c4 or c2 == c3 or c2 == c4 or c3 == c4:
                                continue
                            hand = (c1 * 2) + c2 + c3 + c4
                            self.add_hands_to_table(hand)

        def convert_to_primes(self, hand):
            prime_hand = 1
            if hand[-1] == "F":
                prime_hand *= self.prime_flush
                hand = hand[:-1]
            for card in hand:
                prime_hand *= self.prime_cards[card]
            return prime_hand

        def add_hands_to_table(self, hand):
            prime_hand = self.convert_to_primes(hand)
            if prime_hand in self.all_hands:
                return
            self.all_hands[prime_hand] = (len(self.all_hands), hand)


if __name__ == "__main__":
    hand_eval = HandEvaluator()
    print(hand_eval.evaluate(("As", "Ks", "Qs", "Js", "Ts")))  # Royal Flush
    print(hand_eval.evaluate(("Ks", "Qs", "Js", "Ts", "9s")))  # Royal Flush
    print(hand_eval.evaluate(("Ks", "As", "Ts", "Js", "Qs")))  # Royal Flush
