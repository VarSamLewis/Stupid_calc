import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from simple_approach.calc_logic import CalculatorLogic



class Calculator:
    def __init__(self, root):
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

    def on_button_click(self, button):
        """Handle button clicks"""
        if button == 'C':
            self.clear_display()
        elif button == '=':
            current = self.display.get()
            result = self.calc_logic.evaluate(current)
            self.update_display(result)
        else:
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, current + button)

    def update_display(self, value):
        """Update the display with a value"""
        self.display.delete(0, tk.END)
        self.display.insert(0, str(value))

    def clear_display(self):
        """Clear the display"""
        self.display.delete(0, tk.END)

    def get_display(self):
        """Get current display value"""
        return self.display.get()


if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
