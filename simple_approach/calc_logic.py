import logging

logger = logging.getLogger(__name__)

class CalculatorLogic:
    """Handles calculation logic for the calculator"""

    def sanitise_input(self, expression):
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
            logger.warning(f"Invalid characters detected in expression: {expression}")
            raise ValueError("Invalid characters in input")

    def evaluate(self, expression):
        """
        Evaluate a mathematical expression and return the result

        Args:
            expression: The mathematical expression to evaluate

        Returns:
            str: The result as a string, or "Error" if invalid
        """
        logger.debug(f"Evaluating expression: {expression}")

        if not expression:
            logger.debug("Empty expression, returning 0")
            return "0"

        try:
            safe_expression = self.sanitise_input(expression)
            result = eval(safe_expression)
            logger.debug(f"Evaluation result: {result}")

            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            return str(result)
        except Exception as e:
            logger.error(f"Evaluation error: {e}")
            return "Error"
