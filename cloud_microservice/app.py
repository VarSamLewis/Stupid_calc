from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.logging_config import setup_logging

setup_logging(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def sanitise_input(expression):
    """
    Sanitise input expression to prevent code injection

    Args:
        expression: Mathematical expression to sanitise

    Returns:
        str: Sanitised expression

    Raises:
        ValueError: If expression contains invalid characters
    """
    allowed_chars = set('0123456789+-*/. ')
    logger.debug(f"Sanitising input: {expression}")

    if all(char in allowed_chars for char in expression):
        logger.debug("Input validation passed")
        return expression
    else:
        logger.warning(f"Invalid characters detected: {expression}")
        raise ValueError("Invalid characters in input")

def evaluate(expression):
    """
    Evaluate a mathematical expression

    Args:
        expression: Mathematical expression to evaluate

    Returns:
        str: The result as a string, or "Error" if invalid
    """
    logger.debug(f"Evaluating expression: {expression}")

    if not expression:
        logger.debug("Empty expression, returning 0")
        return "0"

    try:
        safe_expression = sanitise_input(expression)
        result = eval(safe_expression)
        logger.debug(f"Evaluation result: {result}")

        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        return "Error"

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Calculate endpoint for mathematical expressions

    Expects JSON with 'expression' field
    Returns JSON with 'result' field
    """
    data = request.get_json()
    expression = data.get('expression', '')
    logger.info(f"Received calculation request: {expression}")

    result = evaluate(expression)
    logger.info(f"Returning result: {result}")

    return jsonify({"result": result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)
