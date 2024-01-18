from enum import IntEnum
# from itertools import combinations
from game.deck import Deck
from game.player import Player

# from round import BettingRound
# from hand_eval import HandEvaluator
# from current_game import CurrentGame

class TwoGamePositions(IntEnum):
    Dealer = 0
    UTG = 1


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
        self.max_players = max_players
        self.name = name
        self.next_to_act = 0
        self.players = []
        self.players_in_round = []
        self.pot = 0
        self.previous_action = None
        self.remaining_to_act = []
        self.small_blind_position = 0
        self.small_blind_size = 5

    def join(self, player):
        if not self.is_full() and player not in self.players:
            self.players.append(player)
            return True
        return False

    def start(self):
        self.pre_flop_setup()
        # while True:
        self.pre_flop()
        self.flop()
        #     self.turn()
        #     self.river()

    def pre_flop_setup(self):
        self.previous_action = None
        self.players_in_round = [p for p in self.players]

    def pre_flop(self):
        print('PRE FLOP')
        self.post_blinds()
        self.deal_hands()
        self.betting_round()

    def flop(self):
        print('FLOP')
        self.betting_round()
        
    def post_blinds(self):
        self.pot += self.players[self.small_blind_position].post_small_blind(self.small_blind_size)
        
        big_blind_position = (self.small_blind_position + 1) % len(self.players)
        self.pot += self.players[big_blind_position].post_big_blind(self.small_blind_size*2)

        self.current_call_size += self.small_blind_size*2

    def deal_hands(self):
        self.deck = Deck()
        for position, player in enumerate(self.players):
            hand = self.deck.draw_cards(2)
            player.hand = hand
            player.position = position

    def remove_player_from_round(self, player):
        self.players_in_round = [p for p in self.players_in_round if p != player]

    def get_winner(self):
        if len(self.players_in_round) == 1:
            return self.players_in_round[0]

    def update_winnings(self, winner):
        winner.stack += self.pot
        self.pot = 0
        self.remaining_to_act = []

    def get_next_to_act(self, previous_action):
        if previous_action is None and len(self.players_in_round) == 2:
            self.next_to_act = (self.next_to_act + 1) % len(self.players_in_round)
            return self.players_in_round[self.next_to_act]

        if previous_action == 'FOLD':
            ... # Do nothing
        elif previous_action in ['CALL', 'CHECK']:
            self.next_to_act = (self.next_to_act + 1) % len(self.players_in_round)

        return self.players_in_round[self.next_to_act]

    def betting_round(self):
        winner = None
        self.remaining_to_act = [p for p in self.players_in_round]
        while self.remaining_to_act:
            winner = self.get_winner()
            if winner:
                self.update_winnings(winner)
                print("Winner is", winner)
                break

            current_player_acting = self.get_next_to_act(self.previous_action)
            print('Players In Round:', self.players_in_round)
            print('To play:', current_player_acting)
            call_amount = self.call_value_for_player(current_player_acting)
            action = current_player_acting.get_action(call_amount)
            print('Action:', action)

            self.remaining_to_act.remove(current_player_acting)
            self.previous_action = action
            if action == 'FOLD':
                print(current_player_acting, 'Folded')
                self.remove_player_from_round(current_player_acting)

            elif action == 'CHECK':
                ...
 
            elif action == 'CALL':
                value = self.call_value_for_player(current_player_acting)
                current_player_acting.call(value)
                self.pot += value

            elif action == 'RAISE':
                if value < self.min_raise_size:
                    print(f'Raise too low (must be >= {self.current_call_size*2})')
                    return

                next_to_act.raise_bet(value)
                self.increase_pot_by(value)
                self.current_call_size = value

                self.set_next_player_to_act()

                print('PLAYER TO ACT:', self.players_to_act)
            else:
                print('UNRECOGNIZED ACTION')
                return

            print('Pot:', self.pot)
            print()


    # def update_positions(self):
    #     self.small_blind_pos += 1
    #     if self.small_blind_pos > self.max_players:
    #         self.small_blind_pos = 0

    def is_full(self):
        return len(self.players) == self.max_players

    def call_value_for_player(self, player):
        return self.current_call_size - player.current_bettings

    def update_next_to_act(self):
        player_index = self.players_in_round.index(current_player)
        next_player_index = player_index + 1
        if next_player_index >= len(self.players_in_round):
            next_player_index = 0
        self.next_to_act = next_player_index

    # def update_players_in_hand(self):
    #     if self.next_to_act is None:
    #         self.next_to_act = self.small_blind_pos
    #         while self.next_to_act in self.players_out:
    #             self.next_to_act += 1
    #     self.players_to_act = [p for p in range(self.next_to_act+1, 6)] + [p for p in range(0, self.next_to_act)]
    #     for po in self.players_out:
    #         if po in self.players_to_act:
    #             self.players_to_act.remove(po)

    # def decide_winner(self):
    #     print('\n\nDECIDING WINNER\n')
    #     print(self.cards_drawn)
    #     players_in_hand = [p for i, p in enumerate(self.players) if i not in self.players_out]
    #     best_hands = []
    #     best_ranking = 999999999
    #     for p in players_in_hand:
    #         print(p)
    #         best_player_hand = []
    #         for c in combinations(p.hand + self.cards_drawn, 5):
    #             hand_evaluated = self.hand_evaluator.evaluate(c)
    #             if not best_player_hand or best_player_hand[0] > hand_evaluated[0]:
    #                 best_player_hand = hand_evaluated
    #                 best_ranking = min(best_player_hand[0], best_ranking)
    #         print(best_player_hand)
    #         best_hands.append((p, best_player_hand))

    #     print('\nThe winner is: ', end='')
    #     for h in best_hands:
    #         if h[1][0] == best_ranking:
    #             print(h[0])
    #             h[0].stack += self.pot

    def __str__(self):
        return f'{self.name}: {len(self.players)}/{self.max_players} - Pot {self.pot}'
