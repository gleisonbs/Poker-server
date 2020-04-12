class Account:
    def __init__(self, initial_amount=0):
        if initial_amount < 0:
            raise ValueError('Cannot open an account with a negative balance')

        self._balance = initial_amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError('Cannot withdraw a value lesser or equal to zero')

        if self._balance < amount:
            raise ValueError('Cannot withdraw more than your balance')

        self._balance -= amount
        return amount

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError('Cannot deposit a value lesser or equal to zero')

        self._balance += amount

    def balance(self):
        return self._balance