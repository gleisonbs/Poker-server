from unittest import TestCase
from unittest.mock import patch

from game.table import Table
from game.player import Player


class GameTest(TestCase):
    def setUp(self):
        ...

    @patch('builtins.input', side_effect=['fold'])
    def test_headsup_dealer_folds_preflop(self, mock_input):
        player_dealer = Player(None, "dealer")
        player_big_blind = Player(None, "big_blind")

        table = Table("Main table", 2)
        table.join(player_big_blind)
        table.join(player_dealer)

        table.pre_flop_setup()
        table.pre_flop()

        self.assertEqual(player_dealer.stack, 995)
        self.assertEqual(player_big_blind.stack, 1005)

    @patch('builtins.input', side_effect=['call', 'fold'])
    def test_headsup_big_blind_folds_preflop(self, mock_input):
        player_dealer = Player(None, "dealer")
        player_big_blind = Player(None, "big_blind")

        table = Table("Main table", 2)
        table.join(player_big_blind)
        table.join(player_dealer)

        table.pre_flop_setup()
        table.pre_flop()

        self.assertEqual(player_dealer.stack, 1010)
        self.assertEqual(player_big_blind.stack, 990)

    @patch('builtins.input', side_effect=['call', 'check', 'fold'])
    def test_headsup_big_blind_folds_postflop(self, mock_input):
        player_dealer = Player(None, "dealer")
        player_big_blind = Player(None, "big_blind")

        table = Table("Main table", 2)
        table.join(player_big_blind)
        table.join(player_dealer)

        table.pre_flop_setup()
        table.pre_flop()
        table.flop()

        self.assertEqual(player_dealer.stack, 1010)
        self.assertEqual(player_big_blind.stack, 990)

    @patch('builtins.input', side_effect=['call', 'check', 'check', 'fold'])
    def test_headsup_dealer_folds_postflop(self, mock_input):
        player_dealer = Player(None, "dealer")
        player_big_blind = Player(None, "big_blind")

        table = Table("Main table", 2)
        table.join(player_big_blind)
        table.join(player_dealer)

        table.pre_flop_setup()
        table.pre_flop()
        table.flop()

        self.assertEqual(player_dealer.stack, 990)
        self.assertEqual(player_big_blind.stack, 1010)

    @patch('builtins.input', side_effect=['call', 'check', 'check', 'bet 100', 'fold'])
    def test_headsup_big_blind_folds_postflop_after_bet(self, mock_input):
        player_big_blind = Player(None, "big_blind")
        player_dealer = Player(None, "dealer")

        table = Table("Main table", 2)
        table.join(player_big_blind)
        table.join(player_dealer)

        table.pre_flop_setup()
        table.pre_flop()
        table.flop()

        self.assertEqual(player_big_blind.stack, 990)
        self.assertEqual(player_dealer.stack, 1010)

    @patch('builtins.input', side_effect=['call', 'check', 'bet 100', 'fold'])
    def test_headsup_dealer_folds_postflop_after_bet(self, mock_input):
        player_big_blind = Player(None, "big_blind")
        player_dealer = Player(None, "dealer")

        table = Table("Main table", 2)
        table.join(player_big_blind)
        table.join(player_dealer)

        table.pre_flop_setup()
        table.pre_flop()
        table.flop()

        self.assertEqual(player_big_blind.stack, 1010)
        self.assertEqual(player_dealer.stack, 990)

    @patch('builtins.input', side_effect=['call', 'check', 'bet 100', 'raise 250', 'fold'])
    def test_headsup_big_blind_folds_postflop_after_raise(self, mock_input):
        player_big_blind = Player(None, "big_blind")
        player_dealer = Player(None, "dealer")

        table = Table("Main table", 2)
        table.join(player_big_blind)
        table.join(player_dealer)

        table.pre_flop_setup()
        table.pre_flop()
        table.flop()

        self.assertEqual(player_big_blind.stack, 890)
        self.assertEqual(player_dealer.stack, 1110)

    @patch('builtins.input', side_effect=['call', 'check', 'bet 100', 'raise 250', 'raise 750', 'fold'])
    def test_headsup_dealer_folds_postflop_after_reraise(self, mock_input):
        player_big_blind = Player(None, "big_blind")
        player_dealer = Player(None, "dealer")

        table = Table("Main table", 2)
        table.join(player_big_blind)
        table.join(player_dealer)

        table.pre_flop_setup()
        table.pre_flop()
        table.flop()

        self.assertEqual(player_big_blind.stack, 1260)
        self.assertEqual(player_dealer.stack, 740)

    @patch('builtins.input', side_effect=['call', 'check', 'check', 'check', 'check', 'fold'])
    def test_headsup_dealer_folds_after_turn(self, mock_input):
        player_big_blind = Player(None, "big_blind")
        player_dealer = Player(None, "dealer")

        table = Table("Main table", 2)
        table.join(player_big_blind)
        table.join(player_dealer)

        table.pre_flop_setup()
        table.pre_flop()
        table.flop()
        table.turn()

        print(table.flop_cards)
        print(table.turn_cards)

        self.assertEqual(player_big_blind.stack, 1010)
        self.assertEqual(player_dealer.stack, 990)

    @patch('builtins.input', side_effect=['call', 'check', 'check', 'check', 'fold'])
    def test_headsup_big_blind_folds_after_turn(self, mock_input):
        player_big_blind = Player(None, "big_blind")
        player_dealer = Player(None, "dealer")

        table = Table("Main table", 2)
        table.join(player_big_blind)
        table.join(player_dealer)

        table.pre_flop_setup()
        table.pre_flop()
        table.flop()
        table.turn()

        print(table.flop_cards)
        print(table.turn_cards)
        print(table.river_cards)

        self.assertEqual(player_big_blind.stack, 990)
        self.assertEqual(player_dealer.stack, 1010)

    @patch('builtins.input', side_effect=['call', 'check', 'check', 'check', 'check', 'check', 'check', 'check'])
    def test_headsup_winner_after_river(self, mock_input):
        player_big_blind = Player(None, "big_blind")
        player_dealer = Player(None, "dealer")

        table = Table("Main table", 2)
        table.join(player_big_blind)
        table.join(player_dealer)

        table.pre_flop_setup()
        table.pre_flop()
        table.flop()
        table.turn()
        table.river()

        if player_big_blind.stack == 990:
            self.assertEqual(player_dealer.stack, 1010)
        elif player_big_blind.stack == 1010:
            self.assertEqual(player_dealer.stack, 990)

        if player_dealer.stack == 1010:
            self.assertEqual(player_big_blind.stack, 990)
        elif player_dealer.stack == 990:
            self.assertEqual(player_big_blind.stack, 1010)

    def tearDown(self):
        ...
