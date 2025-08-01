# Personal AI Assistant with Tools - Complete Implementation Guide

## 🎯 Project Overview

**Goal**: Build an intelligent assistant that can perform multi-step tasks using various tools and chain actions intelligently.

**Core Capabilities**:
- Web search and information retrieval
- File processing (PDFs, CSVs, text files)
- Mathematical calculations
- Multi-step reasoning and task chaining
- Natural language interaction

## 🏗️ Architecture Overview

```
User Input → Agent (LangChain) → Tool Selection → Tool Execution → Response Generation
                ↓
        [Web Search, File Reader, Calculator, Memory]
```

## 📋 Step-by-Step Implementation

### Step 1: Environment Setup

```bash
# Create project directory
mkdir ai-assistant-tools
cd ai-assistant-tools

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install langchain langchain-google-genai serpapi python-dotenv
pip install pypdf2 pandas numpy matplotlib
pip install streamlit  # For web interface (optional)
pip install google-generativeai
```

### Step 2: Environment Configuration

Create `.env` file:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

**Getting Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### Step 3: Core Assistant Implementation

```python
# main.py
import os
import json
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage

# Load environment variables
load_dotenv()

class PersonalAIAssistant:
    def __init__(self):
        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            google_api_key=os.getenv('GOOGLE_API_KEY'),
            convert_system_message_to_human=True  # Gemini doesn't support system messages natively
        )
        
        # Initialize memory for conversation context
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize tools
        self.tools = self._setup_tools()
        
        # Initialize agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            max_iterations=5
        )
    
    def _setup_tools(self):
        """Setup all available tools"""
        tools = []
        
        # Web Search Tool
        tools.append(self._create_web_search_tool())
        
        # File Reader Tool
        tools.append(self._create_file_reader_tool())
        
        # Calculator Tool
        tools.append(self._create_calculator_tool())
        
        # CSV Analyzer Tool
        tools.append(self._create_csv_analyzer_tool())
        
        return tools
    
    def chat(self, message):
        """Main chat interface"""
        try:
            response = self.agent.run(message)
            return response
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
```

### Step 4: Tool Implementations

#### Web Search Tool
```python
# tools/web_search.py
import requests
import os
from langchain.tools import Tool

def create_web_search_tool():
    def search_web(query):
        """Search the web using SerpAPI"""
        try:
            params = {
                'q': query,
                'api_key': os.getenv('SERPAPI_API_KEY'),
                'engine': 'google',
                'num': 5
            }
            
            response = requests.get('https://serpapi.com/search', params=params)
            results = response.json()
            
            if 'organic_results' in results:
                search_results = []
                for result in results['organic_results'][:3]:
                    search_results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('snippet', ''),
                        'link': result.get('link', '')
                    })
                
                formatted_results = "\n".join([
                    f"Title: {r['title']}\nSummary: {r['snippet']}\nURL: {r['link']}\n"
                    for r in search_results
                ])
                
                return f"Web search results for '{query}':\n\n{formatted_results}"
            else:
                return "No search results found."
                
        except Exception as e:
            return f"Error searching web: {str(e)}"
    
    return Tool(
        name="WebSearch",
        description="Search the internet for current information. Use this when you need up-to-date information or facts not in your knowledge base.",
        func=search_web
    )
```

#### File Reader Tool
```python
# tools/file_reader.py
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
```

#### Calculator Tool
```python
# tools/calculator.py
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
```

#### CSV Analyzer Tool
```python
# tools/csv_analyzer.py
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
```

### Step 5: Enhanced Main Application

```python
# enhanced_main.py
import os
import sys
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory
from tools.web_search import create_web_search_tool
from tools.file_reader import create_file_reader_tool
from tools.calculator import create_calculator_tool
from tools.csv_analyzer import create_csv_analyzer_tool

class EnhancedPersonalAIAssistant:
    def __init__(self):
        load_dotenv()
        
        # Use Gemini Pro for better performance
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            google_api_key=os.getenv('GOOGLE_API_KEY'),
            convert_system_message_to_human=True,
            max_output_tokens=2048
        )
        
        # Memory with window to manage context length
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10  # Remember last 10 exchanges
        )
        
        # Setup tools
        self.tools = [
            create_web_search_tool(),
            create_file_reader_tool(),
            create_calculator_tool(),
            create_csv_analyzer_tool()
        ]
        
        # Create agent with better error handling for Gemini
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            max_iterations=3,
            handle_parsing_errors=True,
            early_stopping_method="generate"  # Better for Gemini
        )
    
    def chat(self, message):
        """Enhanced chat with error handling"""
        try:
            # Add some context for better Gemini performance
            enhanced_message = f"""
You are a helpful AI assistant with access to tools. 
User request: {message}

Please use the available tools when needed and provide a comprehensive response.
"""
            response = self.agent.run(enhanced_message)
            return response
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try rephrasing your request."
    
    def run_interactive(self):
        """Run interactive chat session"""
        print("🤖 Personal AI Assistant with Tools (Powered by Gemini)")
        print("Available capabilities:")
        print("- Web search for current information")
        print("- Read and analyze files (PDF, CSV, TXT)")
        print("- Perform calculations")
        print("- Chain multiple actions together")
        print("\nType 'quit' to exit\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\n🤖 Assistant: ")
            response = self.chat(user_input)
            print(response)
            print("\n" + "="*50 + "\n")

def main():
    try:
        assistant = EnhancedPersonalAIAssistant()
        assistant.run_interactive()
    except Exception as e:
        print(f"Failed to initialize assistant: {e}")
        print("Please check your GOOGLE_API_KEY in the .env file")

if __name__ == "__main__":
    main()
```

### Step 6: Example Usage Scenarios

```python
# examples.py
"""
Example usage scenarios for the AI Assistant
"""

examples = [
    {
        "query": "Search for the latest news about AI and then calculate the percentage increase if AI adoption went from 30% to 85%",
        "expected_flow": "WebSearch → Calculator"
    },
    {
        "query": "Read the sales_data.csv file and calculate the total revenue",
        "expected_flow": "FileReader → CSVAnalyzer"
    },
    {
        "query": "Find information about Python programming best practices and summarize the key points",
        "expected_flow": "WebSearch → Summary"
    },
    {
        "query": "Read this PDF report and calculate the average of the numbers mentioned in it",
        "expected_flow": "FileReader → Calculator"
    }
]
```

### Step 7: Streamlit Web Interface (Gemini Version)

```python
# web_interface.py
import streamlit as st
import os
from dotenv import load_dotenv
from enhanced_main import EnhancedPersonalAIAssistant

def main():
    st.title("🤖 Personal AI Assistant with Tools (Powered by Gemini)")
    
    # Check for API key
    load_dotenv()
    if not os.getenv('GOOGLE_API_KEY'):
        st.error("Please set your GOOGLE_API_KEY in the .env file")
        st.info("Get your free API key from: https://makersuite.google.com/app/apikey")
        return
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        try:
            st.session_state.assistant = EnhancedPersonalAIAssistant()
            st.success("✅ Gemini AI Assistant initialized successfully!")
        except Exception as e:
            st.error(f"Failed to initialize assistant: {e}")
            return
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar with capabilities
    with st.sidebar:
        st.header("🛠️ Capabilities")
        st.write("• 🔍 Web search")
        st.write("• 📄 Read PDF files")
        st.write("• 📊 Analyze CSV data")
        st.write("• 🧮 Mathematical calculations")
        st.write("• 🔗 Chain multiple actions")
        
        st.header("📝 Example Queries")
        examples = [
            "Search for latest AI news and summarize",
            "Calculate 15% of 1250",
            "Read data.csv and find the average sales",
            "Search Python tutorials and calculate study time for 10 topics at 2 hours each"
        ]
        
        for example in examples:
            if st.button(example, key=example):
                # Add to chat
                st.session_state.messages.append({"role": "user", "content": example})
                with st.spinner("Processing..."):
                    response = st.session_state.assistant.chat(example)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything! I can search the web, read files, do calculations, and more..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking and using tools..."):
                response = st.session_state.assistant.chat(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
```

### Alternative: Simple Gemini Implementation (Without LangChain)

If you want a simpler implementation without LangChain complexity:

```python
# simple_gemini_assistant.py
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
        
        self.model = genai.GenerativeModel('gemini-pro')
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
```

## 🚀 Running the Application

### Command Line Interface:
```bash
python enhanced_main.py
```

### Web Interface:
```bash
streamlit run web_interface.py
```

## 🧪 Testing Examples

1. **Multi-step Query**: "Search for current Python trends and calculate what 25% of developers would be if there are 10 million developers worldwide"

2. **File Analysis**: "Read the file data.csv and calculate the average of the 'sales' column"

3. **Complex Calculation**: "Calculate the compound interest for $1000 at 5% for 10 years using the formula A = P(1+r)^t"

## 📈 Advanced Features to Add

1. **Custom Tools**: Add tools for specific domains (weather, news, database queries)
2. **Memory Persistence**: Save conversation history to file
3. **Tool Chaining Optimization**: Better planning for multi-step tasks
4. **Error Recovery**: More robust error handling and retry mechanisms
5. **Performance Monitoring**: Track tool usage and response times

## 🔧 Troubleshooting

### Common Issues:
- **API Key Errors**: Ensure Gemini API key is properly set in .env file
- **Import Errors**: Make sure you installed `langchain-google-genai` not `langchain-openai`
- **File Path Issues**: Use absolute paths or ensure relative paths are correct
- **Memory Issues**: Large files may cause memory problems - implement chunking
- **Rate Limits**: Gemini has generous free limits, but add delays if needed
- **Agent Parsing**: Gemini sometimes has different response formats - the `handle_parsing_errors=True` helps

### Gemini-Specific Tips:
- Gemini works better with explicit instructions
- Use `convert_system_message_to_human=True` for better compatibility
- Set `max_output_tokens` to control response length
- The free tier has 15 requests per minute limit

## 📊 Project Structure
```
ai-assistant-tools/
├── .env                    # GOOGLE_API_KEY and SERPAPI_API_KEY
├── main.py
├── enhanced_main.py        # Main Gemini implementation
├── simple_gemini_assistant.py  # Alternative simple version
├── web_interface.py
├── tools/
│   ├── __init__.py
│   ├── web_search.py
│   ├── file_reader.py
│   ├── calculator.py
│   └── csv_analyzer.py
├── examples.py
└── requirements.txt
```

## 📦 Updated Requirements.txt
```txt
langchain
langchain-google-genai
google-generativeai
serpapi
python-dotenv
pypdf2
pandas
numpy
matplotlib
streamlit
```

This implementation provides a solid foundation for a Personal AI Assistant that can intelligently chain tools together to accomplish complex tasks!