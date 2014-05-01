class PromocodeDatabase(object):
    def __init__(self, db):
        self.db = db

    def redeem(self, token, promocode):
        cursor = self.db.cursor()

        cursor.execute(
            """SELECT * FROM promocodes WHERE promocode = %s;""",
            [promocode])

        code = cursor.fetchone()

        if code is None:
            return None

        cursor.execute(
            """
                INSERT INTO promocode_uses (token, promocode)
                SELECT %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM promocode_uses
                    WHERE token = %s AND promocode = %s);
            """,
            [token, promocode, token, promocode])

        success = (cursor.rowcount == 1)

        self.db.commit()

        if success:
            return code['bytes']
        else:
            return None
