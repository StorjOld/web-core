class PromocodeDatabase(object):
    def __init__(self, db):
        self.db = db

    def redeem(self, token, promocode):
        """SELECT * FROM promocodes;"""
        return None # if doesn't exist

        # Do this atomically
        """
            SELECT 1 FROM promocode_uses
            WHERE token = %s AND promocode = %s;
        """

        """
            INSERT INTO promocode_uses (token, promocode)
            VALUES (%s, %s);
        """

        return None # if can't redeem
        return 5    # if success
