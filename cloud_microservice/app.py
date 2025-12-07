from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


def sanitise_input(expression):
    """Sanitise inputs"""

    allowed_chars = set('0123456789+-*/')

    if all(char in allowed_chars for char in expression):
        return expression
    else:
        return ValueError("Invalid characters in input")
    
def evaluate(expression):
    """Evaluate a mathematical expression"""
    if not expression:
        return "0"
    try:
        safe_expression = sanitise_input(expression)
        result = eval(safe_expression)
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except:
        return "Error"

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '')
    result = evaluate(expression)
    return jsonify({"result": result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
