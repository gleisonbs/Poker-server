from unittest import TestCase
from unittest.mock import patch
from game.table import Table

class TableTest(TestCase):
    def test_create_table(self):
        table = Table('test table', 6)

        self.assertEqual(table.name, 'test table')
        self.assertEqual(table.max_players, 6)
        self.assertEqual(len(table.players), 0)