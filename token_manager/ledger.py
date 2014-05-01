import units

class Ledger(object):
    def __init__(self, db):
        self.db = db

    def balance(self, token):
        """SELECT * FROM balances WHERE TOKEN = %s"""
        return 5 * units.MEGABYTE

    def deposit(self, token, amount):
        """UPDATE balances SET amount = amount + %s WHERE token = %s"""

        """INSERT INTO movements (token, amount) VALUES(%s, %s)"""

        return True

    def withdraw(self, token, amount):
        """UPDATE balances
            SET amount = amount - %s
            WHERE token = %s AND amount >= %s"""

        """INSERT INTO movements (token, amount) VALUES(%s, %s)"""

        return True
