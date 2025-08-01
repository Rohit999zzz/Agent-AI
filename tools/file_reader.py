import os
import PyPDF2
import pandas as pd
from langchain.tools import Tool

def create_file_reader_tool():
    def read_file(file_path):
        """Read various file types"""
        try:
            if not os.path.exists(file_path):
                return f"File not found: {file_path}"
            
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                return read_pdf(file_path)
            elif file_extension == '.csv':
                return read_csv_summary(file_path)
            elif file_extension in ['.txt', '.md']:
                return read_text_file(file_path)
            else:
                return f"Unsupported file type: {file_extension}"
                
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def read_pdf(file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages[:5]:  # Limit to first 5 pages
                text += page.extract_text()
            return f"PDF Content (first 5 pages):\n{text[:2000]}..."
    
    def read_csv_summary(file_path):
        df = pd.read_csv(file_path)
        summary = f"""
CSV File Summary:
- Shape: {df.shape[0]} rows, {df.shape[1]} columns
- Columns: {list(df.columns)}
- First 5 rows:
{df.head().to_string()}

- Data types:
{df.dtypes.to_string()}
        """
        return summary
    
    def read_text_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return f"Text file content:\n{content[:2000]}..."
    
    return Tool(
        name="FileReader",
        description="Read and analyze local files (PDF, CSV, TXT). Provide the full file path.",
        func=read_file
    ) 