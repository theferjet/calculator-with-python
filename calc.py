import tkinter as tk
import customtkinter as ctk
from PIL import Image

# --- Constants for Theming and Configuration ---
BG_COLOR = "#f4f4f4"
BUTTON_BG = "#f8f8f8"
BUTTON_HOVER = "#e0e0e0"
OPERATOR_BG = "#f8f8f8"
OPERATOR_HOVER = "#e0e0e0"
EQUAL_BG = "#85b7dc"
EQUAL_HOVER = "#4a9ede"
TEXT_COLOR = "#000000"

FONT_MAIN = ("Bodoni", 40, "bold")
FONT_TOTAL = ("Bodoni", 16)
FONT_BUTTON = ("Bodoni", 24, "bold")


class CalculatorApp:
    """A modern, functional calculator application built with customtkinter."""

    def __init__(self):
        # --- Window Setup ---
        self.root = ctk.CTk()
        self.root.title("Calculator")
        self.root.geometry("300x520")
        self.root.resizable(False, False)
        
        # Set window icon (ensure 'logo_calc.ico' is in the same directory)
        try:
            self.root.iconbitmap('logo_calc.ico')
        except tk.TclError:
            print("Icon 'logo_calc.ico' not found. Using default icon.")

        # --- State Variables ---
        self.current_expression = ""
        self.total_expression = ""
        self.error_state = False

        # --- Layout ---
        self.display_frame = self._create_display_frame()
        self.buttons_frame = self._create_buttons_frame()

        self.total_label, self.current_label = self._create_display_labels()

        self._create_buttons()
        self._bind_keys()

        self.root.mainloop()

    def _create_display_frame(self) -> ctk.CTkFrame:
        """Creates and packs the top frame for the display labels."""
        frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR, corner_radius=0)
        frame.pack(fill="both", expand=True)
        return frame

    def _create_buttons_frame(self) -> ctk.CTkFrame:
        """Creates and packs the bottom frame for the calculator buttons."""
        frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR, corner_radius=0)
        frame.pack(fill="both", expand=True)
        # Configure grid weights for responsive button sizing
        for i in range(5):
            frame.rowconfigure(i, weight=1)
            frame.columnconfigure(i, weight=1)
        return frame

    def _create_display_labels(self):
        """Creates the labels for the total and current expressions."""
        total_label = ctk.CTkLabel(self.display_frame, text="", anchor="e", font=FONT_TOTAL, text_color=TEXT_COLOR)
        total_label.pack(fill="x", padx=24, pady=(10, 0))

        current_label = ctk.CTkLabel(self.display_frame, text="0", anchor="e", font=FONT_MAIN, text_color=TEXT_COLOR)
        current_label.pack(fill="x", padx=24, pady=(0, 10))

        return total_label, current_label

    def _create_buttons(self):
        """Creates and places all calculator buttons on the grid."""
        # --- Digit Buttons ---
        digits = {
            '7': (1, 0), '8': (1, 1), '9': (1, 2),
            '4': (2, 0), '5': (2, 1), '6': (2, 2),
            '1': (3, 0), '2': (3, 1), '3': (3, 2),
            '.': (4, 1), '0': (4, 0)
        }
        for digit, pos in digits.items():
            button = ctk.CTkButton(
                self.buttons_frame, text=digit, font=FONT_BUTTON,
                fg_color=BUTTON_BG, hover_color=BUTTON_HOVER, text_color=TEXT_COLOR,
                command=lambda d=digit: self._add_to_expression(d)
            )
            button.grid(row=pos[0], column=pos[1], sticky="nsew", padx=1, pady=1)

        # --- Operator Buttons ---
        operators = {"/": "\u00F7", "*": "\u00D7", "-": "\u2212", "+": "+"}
        for i, (op, symbol) in enumerate(operators.items()):
            button = ctk.CTkButton(
                self.buttons_frame, text=symbol, font=FONT_BUTTON,
                fg_color=OPERATOR_BG, hover_color=OPERATOR_HOVER, text_color=TEXT_COLOR,
                command=lambda o=op: self._append_operator(o)
            )
            button.grid(row=i, column=3, sticky="nsew", padx=1, pady=1)

        # --- Special Buttons ---
        ctk.CTkButton(self.buttons_frame, text="C", font=FONT_BUTTON, command=self._clear,
                      fg_color=OPERATOR_BG, hover_color=OPERATOR_HOVER, text_color=TEXT_COLOR
                      ).grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
                      
        ctk.CTkButton(self.buttons_frame, text="+/-", font=FONT_BUTTON, command=self._negate,
                      fg_color=OPERATOR_BG, hover_color=OPERATOR_HOVER, text_color=TEXT_COLOR
                      ).grid(row=0, column=1, sticky="nsew", padx=1, pady=1)

        ctk.CTkButton(self.buttons_frame, text="%", font=FONT_BUTTON, command=lambda: self._append_operator('%'),
                      fg_color=OPERATOR_BG, hover_color=OPERATOR_HOVER, text_color=TEXT_COLOR
                      ).grid(row=0, column=2, sticky="nsew", padx=1, pady=1)
                      
        ctk.CTkButton(self.buttons_frame, text="\u232B", font=FONT_BUTTON, command=self._backspace,
                      fg_color=OPERATOR_BG, hover_color=OPERATOR_HOVER, text_color=TEXT_COLOR
                      ).grid(row=4, column=2, sticky="nsew", padx=1, pady=1)

        ctk.CTkButton(self.buttons_frame, text="=", font=FONT_BUTTON, command=self._evaluate,
                      fg_color=EQUAL_BG, hover_color=EQUAL_HOVER, text_color=TEXT_COLOR
                      ).grid(row=4, column=3, sticky="nsew", padx=1, pady=1)

    def _bind_keys(self):
        """Binds keyboard keys to calculator functions."""
        self.root.bind("<Return>", lambda event: self._evaluate())
        self.root.bind("<BackSpace>", lambda event: self._backspace())
        self.root.bind("<Escape>", lambda event: self._clear())

        for key in "7894561230.":
            self.root.bind(key, lambda event, d=key: self._add_to_expression(d))
        for key in "/*-+%":
            self.root.bind(key, lambda event, o=key: self._append_operator(o))

    def _update_labels(self):
        """Updates the text and font size of the display labels."""
        # Update total expression label, replacing Python operators with display symbols
        total_text = self.total_expression.replace('/', '\u00F7').replace('*', '\u00D7')
        self.total_label.configure(text=total_text)

        # Update current expression label, handling empty case and font size
        current_text = self.current_expression if self.current_expression else "0"
        
        # Dynamic font size
        font_size = max(16, 40 - len(current_text))
        font = (FONT_MAIN[0], font_size, FONT_MAIN[2])
        self.current_label.configure(text=current_text, font=font)

    def _add_to_expression(self, value):
        """Adds a digit or decimal point to the current expression with validation."""
        if self.error_state:
            return
            
        # Prevent multiple decimal points
        if value == "." and "." in self.current_expression:
            return

        self.current_expression += str(value)
        self._update_labels()

    def _append_operator(self, operator):
        """Appends an operator, moving current expression to total expression."""
        if self.error_state:
            return
        
        # Prevent starting with an operator or adding multiple operators
        if not self.current_expression and not self.total_expression:
            return
        if self.total_expression and self.total_expression[-1] in "/*-+%":
            # Replace last operator instead of adding another one
            self.total_expression = self.total_expression[:-1] + operator
        else:
            self.total_expression += self.current_expression + operator
        
        self.current_expression = ""
        self._update_labels()

    def _clear(self):
        """Clears all expressions and resets the calculator state."""
        self.current_expression = ""
        self.total_expression = ""
        self.error_state = False
        self._update_labels()

    def _evaluate(self):
        """Evaluates the final expression and displays the result."""
        if self.error_state or not self.current_expression:
            return

        full_expression = self.total_expression + self.current_expression
        try:
            # Using eval is simple but can be a security risk in larger apps.
            # For a personal calculator, it's generally safe.
            result = str(eval(full_expression.replace('%', '/100')))
            self.current_expression = result
            self.total_expression = ""
        except Exception:
            self.current_expression = "Error"
            self.error_state = True
        finally:
            self._update_labels()
    
    def _backspace(self):
        """Deletes the last character from the current expression."""
        if self.error_state:
            return
        self.current_expression = self.current_expression[:-1]
        self._update_labels()
        
    def _negate(self):
        """Toggles the sign of the current number."""
        if self.error_state or not self.current_expression:
            return
        if self.current_expression.startswith('-'):
            self.current_expression = self.current_expression[1:]
        else:
            self.current_expression = '-' + self.current_expression
        self._update_labels()


if __name__ == "__main__":
    CalculatorApp()
