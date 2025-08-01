#!/usr/bin/env python3
"""
Offline Calculator Tool - Works without API calls
"""

import math
import re
import numpy as np

class OfflineCalculator:
    def __init__(self):
        self.allowed_names = {
            k: v for k, v in math.__dict__.items() 
            if not k.startswith("__")
        }
        self.allowed_names.update({
            'abs': abs, 'round': round, 'min': min, 'max': max,
            'sum': sum, 'len': len, 'pow': pow,
            'np': np  # Allow numpy functions
        })
        
        # Remove potentially dangerous functions
        dangerous = ['eval', 'exec', 'compile', '__import__']
        for name in dangerous:
            self.allowed_names.pop(name, None)
    
    def calculate(self, expression):
        """Perform mathematical calculations safely"""
        try:
            # Clean the expression
            expression = expression.strip()
            
            # Remove any non-mathematical characters
            expression = re.sub(r'[^0-9+\-*/()., \t\n\r\f\v]', '', expression)
            
            result = eval(expression, {"__builtins__": {}}, self.allowed_names)
            return f"Calculation result: {expression} = {result}"
            
        except Exception as e:
            return f"Error in calculation: {str(e)}"
    
    def extract_calculation(self, text):
        """Extract mathematical expressions from text"""
        # Look for common calculation patterns
        patterns = [
            r'calculate\s+([^.!?]+)',
            r'compute\s+([^.!?]+)',
            r'what\s+is\s+([^.!?]+)',
            r'([0-9+\-*/()., \t\n\r\f\v]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Clean the match
                clean_match = re.sub(r'[^0-9+\-*/()., \t\n\r\f\v]', '', match)
                if clean_match and len(clean_match) > 2:
                    return clean_match
        
        return None

def main():
    """Test the offline calculator"""
    calc = OfflineCalculator()
    
    print("🧮 Offline Calculator Tool")
    print("=" * 40)
    
    test_expressions = [
        "2 + 2",
        "sqrt(16)",
        "sin(pi/2)",
        "2 * 3 + 4",
        "pow(2, 3)",
        "np.mean([1, 2, 3, 4, 5])"
    ]
    
    for expr in test_expressions:
        result = calc.calculate(expr)
        print(f"{expr} → {result}")
    
    print("\n💡 You can use this tool when API is unavailable!")
    print("Example: python offline_calculator.py")

if __name__ == "__main__":
    main() 