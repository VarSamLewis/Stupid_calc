import sqlite3 as sql

from db_lookup.db_setup import db_setup
from simple_approach.calc_logic import CalculatorLogic

def lookup(expression):
    
    db_setup()

    conn = sql.connect("calculator.db")
    cursor = conn.cursor()

    result = cursor.execute("SELECT result FROM calc_lookup WHERE expression = ? LIMIT 1", (expression,))
    row = result.fetchone()

    if row:
        
        conn.close()
        return row[0]
    else:
        calc = CalculatorLogic()
        result = calc.evaluate(expression)  

        cursor.execute("INSERT INTO calc_lookup (expression, result) VALUES (?, ?)", (expression, result))
        conn.commit()
        conn.close()
        return result

if __name__ == "__main__":
    lookup()



