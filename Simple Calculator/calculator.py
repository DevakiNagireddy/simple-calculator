import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Set a modern color scheme
        self.bg_color = "#2b2b2b"
        self.display_bg = "#1e1e1e"
        self.button_bg = "#3c3c3c"
        self.button_fg = "#ffffff"
        self.operator_color = "#ff9500"
        self.special_color = "#a6a6a6"
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize calculator state
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.waiting_for_new_input = False
        self.decimal_used = False
        
        # Create custom font
        self.display_font = font.Font(family="Arial", size=32, weight="bold")
        self.button_font = font.Font(family="Arial", size=18, weight="bold")
        
        self.create_widgets()
        self.bind_keys()
    
    def create_widgets(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg=self.display_bg, height=150)
        display_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Previous calculation display (smaller text)
        self.previous_label = tk.Label(
            display_frame, 
            text="", 
            bg=self.display_bg, 
            fg=self.special_color,
            font=("Arial", 14),
            anchor="e"
        )
        self.previous_label.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        # Main display
        self.display_label = tk.Label(
            display_frame, 
            text=self.current_input, 
            bg=self.display_bg, 
            fg="#ffffff",
            font=self.display_font,
            anchor="e"
        )
        self.display_label.pack(fill=tk.X, padx=20, pady=(5, 20))
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Button layout
        button_layout = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', '.', '=']
        ]
        
        # Create buttons
        self.buttons = {}
        for row_idx, row in enumerate(button_layout):
            button_frame.rowconfigure(row_idx, weight=1)
            for col_idx, button_text in enumerate(row):
                button_frame.columnconfigure(col_idx, weight=1)
                
                # Determine button color
                if button_text in ['/', '×', '-', '+', '=']:
                    bg_color = self.operator_color
                elif button_text in ['C', '⌫', '%', '+/-']:
                    bg_color = self.special_color
                else:
                    bg_color = self.button_bg
                
                # Create button
                button = tk.Button(
                    button_frame,
                    text=button_text,
                    font=self.button_font,
                    bg=bg_color,
                    fg=self.button_fg,
                    activebackground="#505050",
                    activeforeground="#ffffff",
                    borderwidth=0,
                    relief="flat",
                    command=lambda btn=button_text: self.button_click(btn)
                )
                
                button.grid(
                    row=row_idx, 
                    column=col_idx, 
                    padx=5, 
                    pady=5, 
                    sticky="nsew"
                )
                self.buttons[button_text] = button
    
    def bind_keys(self):
        # Bind keyboard keys
        self.root.bind('<Key>', self.key_press)
        
        # Bind specific number keys
        for num in range(10):
            self.root.bind(str(num), lambda event, n=num: self.number_input(str(n)))
        
        # Bind operators
        self.root.bind('+', lambda event: self.operator_input('+'))
        self.root.bind('-', lambda event: self.operator_input('-'))
        self.root.bind('*', lambda event: self.operator_input('×'))
        self.root.bind('/', lambda event: self.operator_input('/'))
        self.root.bind('.', lambda event: self.button_click('.'))
        
        # Bind other keys
        self.root.bind('<Return>', lambda event: self.button_click('='))
        self.root.bind('<Escape>', lambda event: self.button_click('C'))
        self.root.bind('<BackSpace>', lambda event: self.button_click('⌫'))
        self.root.bind('<Delete>', lambda event: self.button_click('C'))
    
    def key_press(self, event):
        # Handle key presses that aren't specifically bound
        char = event.char
        if char in '0123456789':
            self.number_input(char)
    
    def update_display(self):
        # Update the main display
        self.display_label.config(text=self.current_input)
        
        # Update the previous calculation display
        prev_text = ""
        if self.previous_input and self.operator:
            # Format operator symbol for display
            display_operator = self.operator
            if display_operator == '*':
                display_operator = '×'
            prev_text = f"{self.previous_input} {display_operator}"
        
        self.previous_label.config(text=prev_text)
    
    def number_input(self, number):
        if self.waiting_for_new_input:
            self.current_input = number
            self.waiting_for_new_input = False
            self.decimal_used = False
        else:
            if self.current_input == "0":
                self.current_input = number
            else:
                self.current_input += number
        
        self.update_display()
    
    def operator_input(self, op):
        if self.operator and not self.waiting_for_new_input:
            self.calculate_result()
        
        self.previous_input = self.current_input
        self.operator = op
        self.waiting_for_new_input = True
        self.decimal_used = False
        self.update_display()
    
    def button_click(self, button_text):
        if button_text in '0123456789':
            self.number_input(button_text)
        
        elif button_text == '.':
            if not self.decimal_used:
                if self.waiting_for_new_input:
                    self.current_input = "0."
                    self.waiting_for_new_input = False
                elif self.current_input == "0":
                    self.current_input = "0."
                else:
                    self.current_input += "."
                self.decimal_used = True
                self.update_display()
        
        elif button_text in ['+', '-', '×', '/']:
            # Map multiplication symbol
            operator = button_text
            if button_text == '×':
                operator = '*'
            self.operator_input(operator)
        
        elif button_text == '=':
            self.calculate_result()
            self.operator = ""
            self.update_display()
        
        elif button_text == 'C':
            self.current_input = "0"
            self.previous_input = ""
            self.operator = ""
            self.waiting_for_new_input = False
            self.decimal_used = False
            self.update_display()
        
        elif button_text == '⌫':
            if len(self.current_input) > 1:
                # Check if we're removing a decimal point
                if self.current_input[-1] == '.':
                    self.decimal_used = False
                self.current_input = self.current_input[:-1]
            else:
                self.current_input = "0"
            self.update_display()
        
        elif button_text == '%':
            try:
                value = float(self.current_input) / 100
                self.current_input = self.format_number(value)
                self.update_display()
            except:
                self.current_input = "Error"
                self.update_display()
        
        elif button_text == '+/-':
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
    
    def calculate_result(self):
        if not self.operator or not self.previous_input:
            return
        
        try:
            prev = float(self.previous_input)
            current = float(self.current_input)
            result = 0
            
            if self.operator == '+':
                result = prev + current
            elif self.operator == '-':
                result = prev - current
            elif self.operator == '*':
                result = prev * current
            elif self.operator == '/':
                if current == 0:
                    self.current_input = "Error"
                    self.update_display()
                    return
                result = prev / current
            
            self.current_input = self.format_number(result)
            self.previous_input = ""
            self.waiting_for_new_input = True
        except:
            self.current_input = "Error"
        
        self.update_display()
    
    def format_number(self, num):
        # Format number to remove unnecessary decimal places
        if num.is_integer():
            return str(int(num))
        else:
            # Limit to 10 decimal places to avoid long numbers
            result = f"{num:.10f}".rstrip('0').rstrip('.')
            return result

def main():
    root = tk.Tk()
    calculator = Calculator(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()