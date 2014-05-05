import token_manager.database

class Authentication(object):
    def __init__(self, database_path):
        self.db = token_manager.database.connect(database_path)

    def valid_api_key(self, api_key):
        cursor = self.db.cursor()
        cursor.execute(
            """SELECT * FROM api_keys WHERE key = %s""",
            [api_key])

        return (cursor.rowcount == 1)
