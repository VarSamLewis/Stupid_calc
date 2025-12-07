import tkinter as tk
import os
import sys
from dotenv import load_dotenv
import logging
import requests
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from simple_approach.calc_logic import CalculatorLogic
from AI_Slop.LLM import Calclogic
from rand_guess.calc_logic import RandCalcLogic
from utils.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

load_dotenv()
GEMINI_API = os.getenv("GEMINI_API")
MODEL_ID = "gemini-2.5-flash"
RAILWAY_URL = os.getenv("RAILWAY_URL")
logger.debug(f"Loaded RAILWAY_URL: {RAILWAY_URL}")
logger.debug(f"Loaded MODEL_ID: {MODEL_ID}")


class Calculator:
    """Calculator UI using Tkinter with multiple calculation backends"""

    def __init__(self, root):
        """
        Initialize the calculator UI

        Args:
            root: Tkinter root window
        """
        logger.debug("Initializing Calculator")
        self.root = root
        self.root.title("Calculator")
        self.calc_logic = CalculatorLogic()
        self.llm_calc_logic = Calclogic(GEMINI_API, MODEL_ID)
        self.rand_calc_logic = RandCalcLogic()
        logger.debug("Calculation backends initialized")

        self.display = tk.Entry(root, width=20, font=('Arial', 20), justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]

        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.on_button_click(x)
            tk.Button(root, text=button, width=5, height=2, font=('Arial', 14),
                     command=cmd).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

        logger.info("Calculator initialized successfully")

    def get_output(self, expression, method=1):
        """
        Get calculation output using specified method

        Args:
            expression: Mathematical expression to evaluate
            method: Calculation method (1=local, 2=cloud, 3=LLM)

        Returns:
            str: Calculation result or "ERROR"
        """
        logger.debug(f"Getting output using method {method}")

        if method == 1:
            logger.debug("Using local calculation logic")
            try:
                output = self.calc_logic.evaluate(expression)
                logger.info(f"Local calculation result: {output}")
            except Exception as e:
                logger.error(f"Error calling local logic: {e}")
                output = "ERROR"
            return output

        elif method == 2:
            logger.debug("Using cloud microservice")
            try:
                logger.debug(f"Sending request to {RAILWAY_URL}/calculate")
                response = requests.post(f"{RAILWAY_URL}/calculate",
                                     json={"expression": expression})
                logger.debug(f"Response status code: {response.status_code}")
                result = response.json()["result"]
                logger.info(f"Cloud result: {result}")
            except Exception as e:
                logger.error(f"Error calling cloud microservice: {e}")
                result = "ERROR"
            return result

        elif method == 3:
            logger.debug("Using LLM calculation")
            try:
                output = self.llm_calc_logic.genresponse(expression)
                logger.info(f"LLM calculation result: {output}")
            except Exception as e:
                logger.error(f"Error calling LLM: {e}")
                output = "ERROR"
            return output
        elif method == 4:
            logger.debug("Using random calculation")
            try:
                output, counter = self.rand_calc_logic.calculate(expression)
                logger.info(f"Random calculation result: {output}, Guess count: {counter}")
            except Exception as e:
                logger.error(f"Error generatring random guess: {e}")
                output = "ERROR"
            return output
        else: 
            raise  ValueError("No method was called")

    def on_button_click(self, button):
        """
        Handle button click events

        Args:
            button: The button value that was clicked
        """
        logger.debug(f"Button clicked: {button}")

        if button == 'C':
            logger.debug("Clear button pressed")
            self.clear_display()

        elif button == '=':
            current = self.display.get()
            logger.info(f"Evaluating expression: {current}")

            start = time.time()
            result = self.get_output(current, method=4)
            elapsed = time.time() - start

            logger.info(f"Time taken for calculation: {elapsed:.4f}s")
            logger.info(f"Final result: {result}")
            self.update_display(result)

        else:
            logger.debug(f"Appending '{button}' to display")
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, current + button)

    def update_display(self, value):
        """
        Update the display with a value

        Args:
            value: Value to display
        """
        logger.debug(f"Updating display with: {value}")
        self.display.delete(0, tk.END)
        self.display.insert(0, str(value))

    def clear_display(self):
        """Clear the calculator display"""
        logger.debug("Display cleared")
        self.display.delete(0, tk.END)

    def get_display(self):
        """
        Get current display value

        Returns:
            str: Current display contents
        """
        return self.display.get()


if __name__ == "__main__":
    logger.info("Starting Calculator application")
    root = tk.Tk()
    calc = Calculator(root)
    logger.info("Entering main event loop")
    root.mainloop()
