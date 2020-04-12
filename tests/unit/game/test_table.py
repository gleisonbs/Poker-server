from unittest import TestCase
from unittest.mock import patch
from game.table import Table


class TableTest(TestCase):
    def test_create(self):
        table = Table('test table', 6)

        self.assertEqual(table.name, 'test table')
        self.assertEqual(table.max_players, 6)
        self.assertEqual(len(table.players), 0)

    def test_create_empty_name(self):
        self.assertRaises(ValueError, Table, '', 2)

    def test_create_zero_players(self):
        self.assertRaises(ValueError, Table, 'test table', 0)

    def test_create_one_player(self):
        self.assertRaises(ValueError, Table, 'test table', 1)

    def test_create_negative_players(self):
        self.assertRaises(ValueError, Table, 'test table', -10)
