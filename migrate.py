import settings
import cloudmanager.migrations

import yoyo
import yoyo.connections

if __name__ == '__main__':
    conn, paramstyle = yoyo.connections.connect(settings.DATABASE_PATH)

    migrations = yoyo.read_migrations(conn, paramstyle, cloudmanager.migrations.path())
    migrations.to_apply().apply()

    conn.commit()
