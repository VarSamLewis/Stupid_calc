class CalculatorLogic:
    """Handles calculation logic for the calculator"""

    def evaluate(self, expression):
        """
        Evaluate a mathematical expression and return the result
        Args:
            expression (str): The mathematical expression to evaluate
        Returns:
            str: The result as a string, or "Error" if invalid
        """
        if not expression:
            return "0"

        try:
            result = eval(expression)
            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            return str(result)
        except:
            return "Error"
