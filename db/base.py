import sqlite3

def get_db(db):
    con = sqlite3.connect(db)
    return con

cursor = get_db("user.db")

db = cursor.execute("""
                CREATE TABLE IF NOT EXISTS run_db (user_id INTEGER, date TEXT, distance INTEGER, id INTEGER PRIMARY KEY AUTOINCREMENT)
               """
               )