import math
import numpy as np
from langchain.tools import Tool

def create_calculator_tool():
    def calculate(expression):
        """Perform mathematical calculations"""
        try:
            # Safe evaluation with limited functions
            allowed_names = {
                k: v for k, v in math.__dict__.items() 
                if not k.startswith("__")
            }
            allowed_names.update({
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sum': sum, 'len': len, 'pow': pow,
                'np': np  # Allow numpy functions
            })
            
            # Remove potentially dangerous functions
            dangerous = ['eval', 'exec', 'compile', '__import__']
            for name in dangerous:
                allowed_names.pop(name, None)
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"Calculation result: {expression} = {result}"
            
        except Exception as e:
            return f"Error in calculation: {str(e)}"
    
    return Tool(
        name="Calculator",
        description="Perform mathematical calculations. Supports basic math, trigonometry, and numpy functions. Example: 'sqrt(16) + 2*3'",
        func=calculate
    ) 