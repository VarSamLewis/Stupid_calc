class CalculatorLogic:
    """Handles calculation logic for the calculator"""


    

    def sanitise_input(self, expression):
        """Sanitise inputs"""

        allowed_chars = set('0123456789+-*/')

        if all(char in allowed_chars for char in expression):
            return expression
        else: 
            return ValueError("Invalid characters in input")

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
            safe_expression = self.sanitise_input(expression)
            result = eval(safe_expression)
            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            return str(result)
        except:
            return "Error"
