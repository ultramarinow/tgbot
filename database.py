import sqlite3
from config import DATABASE_NAME


def create_connection(conn):
    return sqlite3.connect(DATABASE_NAME)

def create_tables(conn):
    with create_connection(conn) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
            tg INTEGER PRIMARY KEY,
            vamp_cd DATETIME,
            ttl_blood_today INTEGER,
            ttl_human INTEGER,
            ttl_hamon INTEGER,
            ttl_tryes INTEGER,
            tryes_lmt INTEGER,
            ttl_blood INTEGER
            )
        """)
        conn.commit()
