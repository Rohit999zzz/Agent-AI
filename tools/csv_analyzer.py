import pandas as pd
import numpy as np
from langchain.tools import Tool

def create_csv_analyzer_tool():
    def analyze_csv(file_path_and_operation):
        """Analyze CSV files with specific operations"""
        try:
            parts = file_path_and_operation.split("|")
            if len(parts) != 2:
                return "Please provide format: 'file_path|operation' where operation is like 'sum column_name' or 'average column_name'"
            
            file_path, operation = parts[0].strip(), parts[1].strip()
            
            df = pd.read_csv(file_path)
            
            op_parts = operation.split()
            if len(op_parts) < 2:
                return "Operation should be like 'sum column_name' or 'average column_name'"
            
            action, column = op_parts[0], " ".join(op_parts[1:])
            
            if column not in df.columns:
                return f"Column '{column}' not found. Available columns: {list(df.columns)}"
            
            if action.lower() == 'sum':
                result = df[column].sum()
                return f"Sum of '{column}': {result}"
            elif action.lower() in ['average', 'mean']:
                result = df[column].mean()
                return f"Average of '{column}': {result}"
            elif action.lower() == 'count':
                result = df[column].count()
                return f"Count of non-null values in '{column}': {result}"
            elif action.lower() == 'max':
                result = df[column].max()
                return f"Maximum value in '{column}': {result}"
            elif action.lower() == 'min':
                result = df[column].min()
                return f"Minimum value in '{column}': {result}"
            else:
                return f"Unsupported operation: {action}. Try: sum, average, count, max, min"
                
        except Exception as e:
            return f"Error analyzing CSV: {str(e)}"
    
    return Tool(
        name="CSVAnalyzer",
        description="Analyze CSV files with operations like sum, average, count, max, min. Format: 'file_path|operation column_name'",
        func=analyze_csv
    ) 