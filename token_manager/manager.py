import database
import units

import generator
import promocodes
import pricing
import ledger

class TokenManager():
    def __init__(self, database_path):
        self.db = database.connect(database_path)

        self.promocodes = promocodes.PromocodeDatabase(self.db)
        self.pricing    = pricing.PriceDatabase(self.db)
        self.ledger     = ledger.Ledger(self.db)

    def generate(self):
        return generator.generate()


    def prices(self):
        return self.pricing.prices()


    def redeem(self, token, promocode):
        amount = self.promocodes.redeem(token, promocode)

        if amount is None:
            return False
        else:
            self.add(token, amount)
            return True


    def balance(self, token):
        return self.ledger.balance(token)

    def consume(self, token, amount):
        return self.ledger.withdraw(token, amount)

    def add(self, token, amount):
        return self.ledger.deposit(token, amount)

    def can_consume(self, token, amount):
        return amount <= self.balance(token)
