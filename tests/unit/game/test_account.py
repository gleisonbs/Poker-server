from unittest import TestCase
from game.account import Account

class AccountTest(TestCase):
    def test_creation_zero_balance(self):
        account = Account()
        self.assertEqual(account.balance(), 0)
    
    def test_creation_positive_balance(self):
        account = Account(1000)
        self.assertEqual(account.balance(), 1000)

    def test_creation_negative_balance(self):
        self.assertRaises(ValueError, Account, -1000)

    def test_deposit_positive_amount(self):
        account = Account()
        account.deposit(1000)
        self.assertEqual(account.balance(), 1000)

    def test_deposit_negative_amount(self):
        account = Account()
        self.assertEqual(account.balance(), 0)
        self.assertRaises(ValueError, account.deposit, -1000)

    def test_deposit_zero_amount(self):
        account = Account()
        self.assertEqual(account.balance(), 0)
        self.assertRaises(ValueError, account.deposit, 0)
    
    def test_withdraw_postive_amount(self):
        account = Account(1000)
        account.withdraw(600)
        self.assertEqual(account.balance(), 400)

    def test_withdraw_negative_amount(self):
        account = Account()
        self.assertEqual(account.balance(), 0)
        self.assertRaises(ValueError, account.withdraw, -1000)

    def test_withdraw_zero_amount(self):
        account = Account()
        self.assertEqual(account.balance(), 0)
        self.assertRaises(ValueError, account.withdraw, 0)

    def test_withdraw_over_balance(self):
        account = Account()
        self.assertEqual(account.balance(), 0)
        self.assertRaises(ValueError, account.withdraw, 1000)
