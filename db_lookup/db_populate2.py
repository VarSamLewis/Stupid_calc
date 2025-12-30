import sqlite3 as sql
import sys
import os

# Add parent directory to path to import from other modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db_lookup.db_setup import db_setup
from simple_approach.calc_logic import CalculatorLogic

def populate():
    db_setup()

    conn = sql.connect("calculator.db")

    cursor = conn.cursor()

    operators = ["+","-","*","/"]

    calc = CalculatorLogic()

    expression_lists = []
    result_list = []

    for op in operators:
        for i in range(1,1001):
            for j in range(1,1001):
                expression = f"{i} {op} {j}"
                result = calc.evaluate(expression)
                cursor.execute("INSERT INTO calc_lookup (expression, result) VALUES (?, ?)", (expression, result))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate()



