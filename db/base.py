import sqlite3

def get_db(db):
    con = sqlite3.connect(db)
    return con

def init_db():
    conn = get_db("user.db")
    # cursor = get_db("user.db")

    conn.execute("""
                    CREATE TABLE IF NOT EXISTS run_db (user_id INTEGER, date TEXT, distance INTEGER, id INTEGER PRIMARY KEY AUTOINCREMENT)
                """
                )
    conn.close()
init_db()