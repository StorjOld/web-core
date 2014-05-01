import sqlite3
import psycopg2
import psycopg2.extras

def connect(*args, **kwargs):
    return connect_psycopg2(*args, **kwargs)

def connect_sqlite3(*args, **kwargs):
    db = sqlite3.connect(*args, **kwargs)

    db.row_factory = sqlite3.Row

    return db

def connect_psycopg2(*args, **kwargs):
    db = psycopg2.connect(*args, **kwargs)

    db.cursor_factory = psycopg2.extras.DictCursor

    return db
