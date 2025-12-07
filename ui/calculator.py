import tkinter as tk
import os
import sys
from dotenv import load_dotenv
import logging
import requests
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from simple_approach.calc_logic import CalculatorLogic

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

RAILWAY_URL=os.getenv("RAILWAY_URL")
logger.debug(f"Loaded RAILWAY_URL: {RAILWAY_URL}")


class Calculator:
    def __init__(self, root):
        logger.debug("Initializing Calculator")
        self.root = root
        self.root.title("Calculator")
        self.calc_logic = CalculatorLogic()

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

    def on_button_click(self, button):
        """Handle button clicks"""
        logger.debug(f"Button clicked: {button}")
        if button == 'C':
            logger.debug("Clearing display")
            self.clear_display()
        elif button == '=':
            current = self.display.get()
            logger.info(f"Evaluating expression: {current}")

            start = time.time()
            # Simple approach
            #result = self.calc_logic.evaluate(current)
        
            # cloud microservice
            try:
                logger.debug(f"Sending request to {RAILWAY_URL}/calculate")
                response = requests.post(f"{RAILWAY_URL}/calculate",
                                     json={"expression": current})
                logger.debug(f"Response status code: {response.status_code}")
                result = response.json()["result"]
                logger.info(f"Cloud result: {result}")
            except Exception as e:
                logger.error(f"Error calling cloud microservice: {e}")
                result = "ERROR"

            logger.info(f"Time taken for calculation: {time.time() - start}")
            logger.info(f"Request value: {result}")
            self.update_display(result)
        else:
            logger.debug(f"Appending '{button}' to display")
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, current + button)

    def update_display(self, value):
        """Update the display with a value"""
        logger.debug(f"Updating display with: {value}")
        self.display.delete(0, tk.END)
        self.display.insert(0, str(value))

    def clear_display(self):
        """Clear the display"""
        logger.debug("Display cleared")
        self.display.delete(0, tk.END)

    def get_display(self):
        """Get current display value"""
        return self.display.get()


if __name__ == "__main__":
    logger.info("Starting Calculator application")
    root = tk.Tk()
    calc = Calculator(root)
    logger.info("Entering main event loop")
    root.mainloop()
