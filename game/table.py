from enum import IntEnum
from itertools import combinations

from game.deck import Deck
from game.player import Player
from game.enums.two_game_positions import TwoGamePositions
from game.hand_evaluator import HandEvaluator
# from round import BettingRound
# from current_game import CurrentGame


class Table:
    def __init__(self, name, max_players):
        # self.cards_drawn = []
        # self.current_game = CurrentGame()
        # self.hand_evaluator = HandEvaluator()
        # self.is_round_in_progress = False
        # self.min_raise_size = self.small_blind_size * 2
        # self.options = ['CALL', 'FOLD', 'RAISE']
        # self.players_out = []
        # self.previous_action = ''
        self.current_call_size = 0
        self.flop_cards = []
        self.turn_cards = []
        self.river_cards = []
        self.max_players = max_players
        self.name = name
        self.next_to_act = 0
        self.players = []
        self.players_in_round = []
        self.pot = 0
        self.previous_action = None
        self.previous_action = None
        self.remaining_to_act = []
        self.small_blind_position = 0
        self.small_blind_size = 5

    def rotate_list(self, list_to_rotate, n_rotations):
        start = len(list_to_rotate) - n_rotations
        return list_to_rotate[start:] + list_to_rotate[:start]

    def join(self, player):
        if not self.is_full() and player not in self.players:
            self.players.append(player)
            return True
        return False

    def start(self):
        positions = [p for p in TwoGamePositions]
        for i in range(self.players):
            player[i].position = positions[i]

        self.pre_flop_setup()
        # while True:
        self.pre_flop()
        self.flop()
        #     self.turn()
        #     self.river()

    def pre_flop_setup(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.previous_action = None
        self.players_in_round = [p for p in self.players]

    def pre_flop(self):
        print('PRE FLOP '.ljust(70, '='))
        self.remaining_to_act = [p for p in self.players_in_round]
        # if is first move on heads up game dealer acts first
        if len(self.players) == 2:
            self.remaining_to_act = self.rotate_list(self.remaining_to_act, 1)

        self.post_blinds()
        self.deal_hands()
        self.betting_round()

    def flop(self):
        print('FLOP '.ljust(70, '='))
        self.remaining_to_act = [p for p in self.players_in_round]
        self.flop_cards = self.deck.draw_cards(3)
        print(self.flop_cards)
        self.betting_round()

    def turn(self):
        print('TURN '.ljust(70, '='))
        self.remaining_to_act = [p for p in self.players_in_round]
        self.turn_cards = self.deck.draw_cards(1)
        self.betting_round()

    def river(self):
        print('RIVER '.ljust(70, '='))
        self.remaining_to_act = [p for p in self.players_in_round]
        self.river_cards = self.deck.draw_cards(1)
        self.betting_round()

    def post_blinds(self):
        small_blind_position = self.small_blind_position
        if len(self.players) == 2:
            small_blind_position = 1
        big_blind_position = (small_blind_position + 1) % len(self.players)

        self.pot += self.players[small_blind_position].post_blind(
            self.small_blind_size)
        self.pot += self.players[big_blind_position].post_blind(
            self.small_blind_size*2)

        self.current_call_size += self.small_blind_size*2

    def deal_hands(self):
        for position, player in enumerate(self.players):
            hand = self.deck.draw_cards(2)
            player.hand = hand
            player.position = position

    def remove_player_from_round(self, player):
        self.players_in_round = [
            p for p in self.players_in_round if p != player]

    def check_has_single_player(self):
        if len(self.players_in_round) == 1:
            return self.players_in_round[0]

    def update_winnings(self, winner):
        winner.stack += self.pot
        self.pot = 0
        self.remaining_to_act = []

    def get_next_to_act(self, previous_action):
        if previous_action is None and len(self.players_in_round) == 2:
            self.next_to_act = 0
            while self.players[self.next_to_act] not in self.players_in_round:
                self.next_to_act = (self.next_to_act +
                                    1) % len(self.players_in_round)
            return self.players_in_round[self.next_to_act]

        if previous_action == 'FOLD':
            ...  # Do nothing
        elif previous_action in ['CALL', 'CHECK']:
            self.next_to_act = (self.next_to_act +
                                1) % len(self.players_in_round)

        return self.players_in_round[self.next_to_act]

    # TODO: split this method into a getter and an updater
    def update_players_to_act(self, previous_action, current_player):
        print('Previous action:', previous_action)
        print('0 remaining_to_act', self.remaining_to_act)
        if previous_action in ['CALL', 'CHECK']:
            self.remaining_to_act = self.rotate_list(self.remaining_to_act, 1)

        print('1 remaining_to_act', self.remaining_to_act)
        if previous_action in ['BET', 'RAISE']:
            self.remaining_to_act = [p for p in self.players_in_round]
            current_player_index = self.remaining_to_act.index(current_player)
            self.remaining_to_act = self.rotate_list(
                self.remaining_to_act, current_player_index)
            self.remaining_to_act.pop(0)

        print('2 remaining_to_act', self.remaining_to_act)

    def betting_round(self):
        print(self.remaining_to_act)
        self.next_to_act = 0
        current_player_acting = None
        previous_action = None
        current_bet_amount = 0
        while self.remaining_to_act:
            print('looping...')

            current_player_acting = self.remaining_to_act.pop(0)

            print('To play:', current_player_acting)
            call_amount = self.call_amount_for_player(current_player_acting)
            print('--------', current_player_acting, call_amount)
            action, amount = current_player_acting.get_action(
                call_amount, current_bet_amount)
            print('Action:', action, '/ Amount:', amount)

            if action == 'FOLD':
                print(current_player_acting, 'Folded')
                self.remove_player_from_round(current_player_acting)

            elif action == 'CHECK':
                ...

            elif action == 'CALL':
                amount = self.call_amount_for_player(current_player_acting)
                print('Amount to call:', amount)
                current_player_acting.call(amount)
                self.pot += amount

            elif action == 'BET':
                current_player_acting.bet(amount)
                self.pot += amount
                self.current_call_size += amount
                current_bet_amount = amount

            elif action == 'RAISE':
                current_player_acting.bet(amount)
                self.pot += amount
                self.current_call_size += amount
                current_bet_amount = amount

            else:
                print('UNRECOGNIZED ACTION')
                return

            previous_action = action
            self.update_players_to_act(previous_action, current_player_acting)

            print('========', previous_action)
            print(self.remaining_to_act)

            print('Pot:', self.pot)

            winner = self.check_has_single_player()
            if winner:
                self.update_winnings(winner)
                print("Winner is", winner)
                break
            print()

        if self.river_cards:
            winner = self.get_winner()
            print("Winner is", winner)
            self.update_winnings(winner)

    def get_winner(self):
        hand_eval = HandEvaluator()
        best_hands = []
        table_cards = self.flop_cards + self.turn_cards + self.river_cards
        for player in self.players_in_round:
            all_cards = player.hand + table_cards
            best_player_hand = hand_eval.get_best_hand(all_cards, 5)
            best_hands.append(best_player_hand + (player,))
        return min(best_hands, key=lambda x: x[0])[2]

    def is_full(self):
        return len(self.players) == self.max_players

    def call_amount_for_player(self, player):
        return self.current_call_size - player.current_bettings

    def update_next_to_act(self):
        player_index = self.players_in_round.index(current_player)
        next_player_index = player_index + 1
        if next_player_index >= len(self.players_in_round):
            next_player_index = 0
        self.next_to_act = next_player_index

    def __str__(self):
        return f'{self.name}: {len(self.players)}/{self.max_players}' \
            f'\nPot: {self.pot}' \
            f'\nFlop: {self.flop_cards}'
