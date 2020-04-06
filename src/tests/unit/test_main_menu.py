from unittest import TestCase
from unittest.mock import patch
from game.main_menu import MainMenu

class MainMenuTest(TestCase):
    def test_initial_message(self):
        self.assertEqual(MainMenu.get(), """
         /$$$$$$$           /$$                          
        | $$__  $$         | $$                          
        | $$  \ $$ /$$$$$$ | $$   /$$  /$$$$$$   /$$$$$$ 
        | $$$$$$$//$$__  $$| $$  /$$/ /$$__  $$ /$$__  $$
        | $$____/| $$  \ $$| $$$$$$/ | $$$$$$$$| $$  \__/
        | $$     | $$  | $$| $$_  $$ | $$_____/| $$      
        | $$     |  $$$$$$/| $$ \  $$|  $$$$$$$| $$      
        |__/      \______/ |__/  \__/ \_______/|__/      
        

        1. Join table
        2. Create table
        3. List tables

        : """)

    def test_choose_option(self):
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print') as mocked_print:
                MainMenu.choose_option()
                mocked_print.assert_called()
                mocked_print.assert_called_with('You chose 1')