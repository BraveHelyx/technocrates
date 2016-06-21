from flask import g
import sqlite3
from contextlib import closing

USER_DB = './tmp/users.db'

def connect_db(db_file):
    g.db = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    return g.db

def close_db():
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# Make connection (if necessary) and get db and
def get_db():
    conn = getattr(g, 'db', None)
    if conn is None:
        # @todo This will fail, as we don't have the config file value here...
        conn = g.db = connect_db(USER_DB)
    conn.row_factory = sqlite3.Row    # Make dict from results
    return conn

def insert_db(query, args=()):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
