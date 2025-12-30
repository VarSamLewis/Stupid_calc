import sqlite3 as sql 


def db_setup():
    conn = sql.connect("calculator.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calc_lookup (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT,
            result INTEGER
        );
    """)

    conn.commit()  
    conn.close()

if __name__ == "__main__":
    db_setup()
