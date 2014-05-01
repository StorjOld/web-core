import units

class Price(object):
    def __init__(self, amount, cost):
        self.amount = amount
        self.cost   = cost

class PriceDatabase(object):
    def __init__(self, db):
        self.db = db

    def prices(self):
        """SELECT * FROM prices;"""

        cursor = self.db.cursor()
        cursor.execute("""SELECT * FROM prices;""")

        rows = []
        while True:
            row = cursor.fetchone()
            if row is None:
                break

            rows.append(self.convert(row))

        return rows

    def convert(self, row):
        return Price(row['bytes'], row['amount'])
