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
        if not isinstance(name, str):
            raise ValueError('name parameter must be a string')

        if not isinstance(max_players, int):
            raise ValueError('max_players parameter must be an integer')

        if max_players < 2:
            raise ValueError('Number of max players in the table can\'t be less than 2')

        if not name:
            raise ValueError('Table name cannot be empty')

        self.max_players = max_players
        self.name = name
        self.players = []
        # self.current_game = CurrentGame()
        self.pot = 0
        self.small_blind_position = 0
        self.small_blind_size = 5
        self.current_call_size = 0
        self.next_to_act = 0
        self.players_in_round = []
        self.remaining_to_act = []
        # self.players_out = []
        # self.options = ['CALL', 'FOLD', 'RAISE']
        # self.is_round_in_progress = False
        # self.previous_action = ''
        # self.cards_drawn = []
        # self.hand_evaluator = HandEvaluator()
        # self.min_raise_size = self.small_blind_size * 2

    def join(self, player):
        if not self.is_full() and player not in self.players:
            self.players.append(player)
            return True
        return False

    def start(self):
        self.pre_flop_setup()
        # while True:
        self.pre_flop()
        #     self.flop()
        #     self.turn()
        #     self.river()

    def pre_flop_setup(self):
        self.players_in_round = [p for p in self.players]
        self.remaining_to_act = [p for p in self.players]

    def pre_flop(self):
        self.post_blinds()
        self.deal_hands()
        self.betting_round()
        #self.is_round_in_progress = True
        #self.next_to_act = self.small_blind_pos + 2
        # if self.next_to_act >= self.max_players:
        #     self.next_to_act = self.next_to_act - self.max_players
        # print('NEXT_TO_ACT', self.next_to_act)
        # self.players_to_act = [p for p in range(self.next_to_act+1, 6)] + [p for p in range(0, self.next_to_act)]
        # print(self.players_to_act)
        
    def post_blinds(self):
        self.pot += self.players[self.small_blind_position].post_small_blind(self.small_blind_size)
        self.pot += self.players[self.small_blind_position+1].post_big_blind(self.small_blind_size*2)
        self.current_call_size += self.small_blind_size*2

    def deal_hands(self):
        self.deck = Deck()
        for position, player in enumerate(self.players):
            hand = self.deck.draw_cards(2)
            player.hand = hand
            player.position = position

    def remove_player_from_round(self, player):
        self.players_in_round = [p for p in self.players_in_round if p != player]

    # def increase_pot_by(amount):
    #     self.pot += amount

    def get_winner(self):
        print(self.players_in_round,  len(self.players_in_round))
        if len(self.players_in_round) == 1:
            return self.players_in_round[0]

    def update_winnings(self, winner):
        winner.stack += self.pot
        self.pot = 0
        self.remaining_to_act = []

    def betting_round(self):
        winner = None
        while self.remaining_to_act:
            winner = self.get_winner()
            if winner:
                self.update_winnings(winner)
                print("Winner is", winner)
                break

            current_player_acting = self.players_in_round[self.next_to_act]
            action = current_player_acting.get_action()

            print('Players In Round:', self.players_in_round)
            print('Next to Act:', self.next_to_act)
            print('To play:', current_player_acting)
            print('Action:', action)

            if action == 'FOLD':
                print(current_player_acting, 'Folded')
                self.previous_action = f'Player {self.next_to_act} folded'
                self.remove_player_from_round(current_player_acting)
 
            elif action == 'CALL':
                self.previous_action = f'Player {current_player_acting} called'
                value = self.call_value_for_player(current_player_acting)
                current_player_acting.call(value)
                self.pot += value
                self.next_to_act = (self.next_to_act + 1) % len(self.players_in_round)

            elif action == 'RAISE':
                if value < self.min_raise_size:
                    print(f'Raise too low (must be >= {self.current_call_size*2})')
                    return

                self.previous_action = f'Player {self.next_to_act} raised'

                next_to_act.raise_bet(value)
                self.increase_pot_by(value)
                self.current_call_size = value

                self.set_next_player_to_act()

                print('PLAYER TO ACT:', self.players_to_act)
            else:
                print('UNRECOGNIZED ACTION')
                return

            # self.update_next_to_act()
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
