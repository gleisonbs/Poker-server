from itertools import combinations
from deck import Deck
from player import Player
from hand_eval import HandEvaluator

class Table:
    def __init__(self):
        self.max_players = 6
        self.players = []

        self.pot = 0
        self.small_blind_pos = 3
        self.small_blind_size = 5
        self.current_call = 0
        self.players_out = []
        self.options = ['CALL', 'FOLD', 'RAISE']
        self.is_round_in_progress = False
        self.previous_action = ''
        self.cards_drawn = []
        self.hand_evaluator = HandEvaluator()

    def start_round(self):
        self.is_round_in_progress = True
        self.next_to_act = self.small_blind_pos + 2
        if self.next_to_act >= self.max_players:
            self.next_to_act = self.next_to_act - self.max_players
        print('NEXT_TO_ACT', self.next_to_act)
        self.players_to_act = [p for p in range(self.next_to_act+1, 6)] + [p for p in range(0, self.next_to_act)]
        print(self.players_to_act)
        self.deal_hands()
        self.post_blinds()

    def post_blinds(self):
        self.pot += self.players[self.small_blind_pos].post_small_blind(self.small_blind_size)
        self.pot += self.players[self.small_blind_pos+1].post_big_blind(self.small_blind_size*2)
        self.current_call += self.small_blind_size*2

    def deal_hands(self):
        self.deck = Deck()
        for position, player in enumerate(self.players):
            hand = self.deck.draw_cards(2)
            player.hand = hand
            player.position = position
            print(player)

    def player_action(self, action):
        print(action)
        action = action.upper()
        if len(action.split(' ')) == 2:
            value = int(action.split(' ')[1])
            action = action.split(' ')[0]

        current_player_call = self.call_value_for_player()

        if action == 'FOLD':
            self.previous_action = f'Player {self.next_to_act} folded'

            self.players_out.append(self.next_to_act)
        elif action == 'CALL':
            self.previous_action = f'Player {self.next_to_act} called'

            self.pot += self.players[self.next_to_act].call(self.call_value_for_player())
        elif action == 'RAISE':
            if value < self.current_call*2:
                print(f'Raise too low (must be >= {self.current_call*2})')
                return
            self.previous_action = f'Player {self.next_to_act} raised'

            self.pot += self.players[self.next_to_act].raise_bet(value)
            self.current_call = value

            self.update_players_in_hand()

            print('PLAYER TO ACT:', self.players_to_act)
        else:
            print('UNRECOGNIZED ACTION')
            return

        print(self.previous_action)
        self.update_next_to_act()

    def update_positions(self):
        self.small_blind_pos += 1
        if self.small_blind_pos > self.max_players:
            self.small_blind_pos = 0

    def add_player(self, player):
        if not self.is_full():
            self.players.append(Player(player))
            return True
        else:
            return False

    def is_full(self):
        return len(self.players) == self.max_players

    def call_value_for_player(self):
        return self.current_call - self.players[self.next_to_act].current_bettings

    def update_next_to_act(self):
        if self.players_to_act:
            self.next_to_act = self.players_to_act.pop(0)
        else:
            self.next_to_act = None

    def update_players_in_hand(self):
        if self.next_to_act is None:
            self.next_to_act = self.small_blind_pos
            while self.next_to_act in self.players_out:
                self.next_to_act += 1
        self.players_to_act = [p for p in range(self.next_to_act+1, 6)] + [p for p in range(0, self.next_to_act)]
        for po in self.players_out:
            if po in self.players_to_act:
                self.players_to_act.remove(po)

    def decide_winner(self):
        print('\n\nDECIDING WINNER\n')
        print(self.cards_drawn)
        players_in_hand = [p for i, p in enumerate(self.players) if i not in self.players_out]
        best_hands = []
        best_ranking = 999999999
        for p in players_in_hand:
            print(p)
            best_player_hand = []
            for c in combinations(p.hand + self.cards_drawn, 5):
                hand_evaluated = self.hand_evaluator.evaluate(c)
                if not best_player_hand or best_player_hand[0] > hand_evaluated[0]:
                    best_player_hand = hand_evaluated
                    best_ranking = min(best_player_hand[0], best_ranking)
            print(best_player_hand)
            best_hands.append((p, best_player_hand))

        print('\nThe winner is: ', end='')
        for h in best_hands:
            if h[1][0] == best_ranking:
                print(h[0])
                h[0].stack += self.pot

