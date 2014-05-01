import units

class Ledger(object):
    def __init__(self, db):
        self.db = db

    def balance(self, token):
        cursor = self.db.cursor()
        cursor.execute("""SELECT * FROM balances WHERE TOKEN = %s""", [token])

        row = cursor.fetchone()

        return 0 if row is None else row['amount']

    def deposit(self, token, amount):
        cursor = self.db.cursor()

        cursor.execute(
            """INSERT INTO balances (token, amount)
                SELECT %s, 0
                WHERE NOT EXISTS (SELECT 1 FROM balances WHERE token = %s)""",
                [token, token])

        cursor.execute(
            """UPDATE balances SET amount = amount + %s WHERE token = %s""",
            [amount, token])

        cursor.execute(
            """INSERT INTO movements (token, amount) VALUES(%s, %s)""",
            [token, amount])

        self.db.commit()

        return True

    def withdraw(self, token, amount):
        """Remove the given amount from the token's balance."""

        cursor = self.db.cursor()

        cursor.execute("""
            UPDATE balances
            SET amount = amount - %s
            WHERE token = %s AND amount >= %s""",
            [amount, token, amount])

        success = (cursor.rowcount == 1)

        if success:
            cursor.execute(
                """INSERT INTO movements (token, amount) VALUES(%s, %s)""",
                [token, -amount])

        self.db.commit()
        return success
