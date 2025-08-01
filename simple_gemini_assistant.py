import google.generativeai as genai
import os
from dotenv import load_dotenv
from tools.web_search import create_web_search_tool
from tools.file_reader import create_file_reader_tool
from tools.calculator import create_calculator_tool

class SimpleGeminiAssistant:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.chat = self.model.start_chat(history=[])
        
        # Setup tools
        self.web_search = create_web_search_tool()
        self.file_reader = create_file_reader_tool()
        self.calculator = create_calculator_tool()
    
    def process_message(self, message):
        """Process message and decide which tools to use"""
        
        # Simple keyword-based tool selection
        if any(word in message.lower() for word in ['search', 'google', 'find', 'look up']):
            # Extract search query (simple approach)
            query = message.replace('search for', '').replace('google', '').replace('find', '').strip()
            search_result = self.web_search.func(query)
            
            response = self.chat.send_message(f"Based on this search result: {search_result}, please provide a helpful response to: {message}")
            return response.text
        
        elif any(word in message.lower() for word in ['calculate', 'compute', 'math']):
            # Try to extract calculation
            import re
            calc_pattern = r'[\d\+\-\*\/\(\)\.\s]+'
            calc_match = re.search(calc_pattern, message)
            if calc_match:
                calc_result = self.calculator.func(calc_match.group())
                response = self.chat.send_message(f"Calculation result: {calc_result}. Please provide context for: {message}")
                return response.text
        
        elif any(word in message.lower() for word in ['read', 'file', 'pdf', 'csv']):
            return "Please provide the file path you'd like me to read."
        
        else:
            # Regular chat
            response = self.chat.send_message(message)
            return response.text

# Usage
def main():
    assistant = SimpleGeminiAssistant()
    print("Simple Gemini Assistant Ready!")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        response = assistant.process_message(user_input)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main() 