import random as rand
import logging
import math

logger = logging.getLogger(__name__)

class RandCalcLogic():
    
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

    def extract_numbers(expression):
        """Extract all numbers from expression"""
        numbers = re.findall(r'\d+\.?\d*', expression)
        return [float(num) if '.' in num else int(num) for num in numbers]

    def calculate(self, expression):
        safe_expression = self.sanitise_input(expression)
        result = eval(safe_expression)
    
        #lower_bound = -9223372036854775807
        #upper_bound = 9223372036854775807
        lower_bound = -100000000 
        upper_bound = 100000000
        guess = rand.randint(lower_bound, upper_bound)
        counter = 0
    
        while guess != result:
            counter += 1
            diff = result - guess

            loss = min(abs(diff), 1e10)  # Cap the loss
            adjustment = int(loss * math.log(loss + 1))  # Logarithmic scaling

            if diff > 0:  #
                lower_bound = guess + 1
                upper_bound = min(guess + adjustment, upper_bound)
            else:  
                upper_bound = guess - 1
                lower_bound = max(guess - adjustment, lower_bound)
        
            if lower_bound > upper_bound:
                lower_bound, upper_bound = upper_bound, lower_bound
        
                
            guess = rand.randint(lower_bound, upper_bound)

            logger.debug(f"Count: {counter}")
            logger.debug(f"Lower Bound: {lower_bound}")
            logger.debug(f"Upper Bound: {upper_bound}")
            logger.debug(f"Guess: {guess}")
        return guess,  counter
