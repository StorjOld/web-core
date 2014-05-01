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
        return [
            Price(5, 100 * units.GIGABYTE),
            Price(50,  1 * units.TERABYTE)
        ]
