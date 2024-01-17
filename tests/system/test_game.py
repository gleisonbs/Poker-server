from unittest import TestCase
from unittest.mock import patch

from game.table import Table
from game.player import Player

class GameTest(TestCase):
    def setUp(self):
        ...
    @patch('builtins.input', side_effect=['fold'])
    def test_headsup_dealer_folds_preflop(self, mock_input):
        player1 = Player(None, "dealer")
        player2 = Player(None, "utg")

        table = Table("Main table", 2)
        table.join(player1)
        table.join(player2)

        table.pre_flop_setup()
        table.pre_flop()

        self.assertEqual(player1.stack, 995)
        self.assertEqual(player2.stack, 1005)

    @patch('builtins.input', side_effect=['call', 'fold'])
    def test_headsup_utg_folds_preflop(self, mock_input):
        player1 = Player(None, "dealer")
        player2 = Player(None, "utg")

        table = Table("Main table", 2)
        table.join(player1)
        table.join(player2)

        table.pre_flop_setup()
        table.pre_flop()

        self.assertEqual(player1.stack, 1010)
        self.assertEqual(player2.stack, 990)

    def tearDown(self):
        ...
