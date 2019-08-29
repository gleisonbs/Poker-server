from enum import Enum
from player import Player
import ActionQueue

class BettingRoundName(Enum):
    PRE_FLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3

class BettingRound:
    def __init__(self, betting_round_name, players):
        self.current_round = betting_round_name
        self.players = players
        self.players_to_act = players
        self.cards_drawn = []
        self.pot = 0

        self.small_blind = 10
        self.big_blind = self.small_blind * 2

    def __str__(self):
        return str(self.current_round)

    def post_small_blind(self):
        small_blind_player = self.players_to_act[0]
        if small_blind_player.has_enough_funds(self.small_blind):
            self.pot = small_blind_player.post_big_blind(self.small_blind)
            return True
        return False

    def post_big_blind(self):
        big_blind_player = self.players_to_act[1]
        if big_blind_player.has_enough_funds(self.big_blind):
            self.pot = big_blind_player.post_big_blind(self.big_blind)
            return True
        return False

    def player_should_post_sb(self, player):
        return player == self.players_to_act[0] and self.current_round == BettingRoundName.PRE_FLOP
    
    def player_should_post_bb(self, player):
        return player == self.players_to_act[1] and self.current_round == BettingRoundName.PRE_FLOP

    def start(self):
        while self.players_to_act:
            ActionQueue.add_message_to_player("Your turn", self.players_to_act[0])
            action_from_player = ActionQueue.get_action_from_player()
            
            if not action_from_player:
                continue

            player = action_from_player.player

            if player != self.players_to_act[0]:
                continue

            action, amount = action_from_player.value.split(':')
            action = action.lower()

            if action == "postsb":
                if self.player_should_post_sb(player):
                    self.post_small_blind()
                self.players_to_act.pop(0)
                
            elif action == "postbb":
                if self.player_should_post_bb(player):
                    self.post_big_blind()
                self.players_to_act.pop(0)
                
            elif action == 'fold':
                self.players_to_act.pop(0)

            elif action == 'call':
                pass
            elif action == 'bet':
                pass
            elif action == 'raise':
                pass
