# Personal AI Assistant with Tools

A powerful AI assistant powered by Google's Gemini that can perform multi-step tasks using various tools and chain actions intelligently.

## 🎯 Features

- **🔍 Web Search**: Search the internet for current information
- **📄 File Processing**: Read and analyze PDFs, CSVs, and text files
- **🧮 Mathematical Calculations**: Perform complex calculations with math and numpy functions
- **📊 Data Analysis**: Analyze CSV files with statistical operations
- **🔗 Multi-step Reasoning**: Chain multiple actions together intelligently
- **💬 Natural Language Interaction**: Chat naturally with the assistant

## 🏗️ Architecture

```
User Input → Agent (LangChain) → Tool Selection → Tool Execution → Response Generation
                ↓
        [Web Search, File Reader, Calculator, Memory]
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. API Keys Setup

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

**Getting API Keys:**
- **Gemini API Key**: Get your free key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **SerpAPI Key**: Get your key from [SerpAPI](https://serpapi.com/) (optional for web search)

### 3. Run the Assistant

#### Web Interface (Recommended - with File Upload):
```bash
streamlit run web_interface.py
```

#### Command Line Interface:
```bash
python enhanced_main.py
```

#### Simple Version (No LangChain):
```bash
python simple_gemini_assistant.py
```

#### File Upload Demo:
```bash
streamlit run file_upload_demo.py
```

## 🛠️ Available Tools

### Web Search Tool
- Search the internet for current information
- Returns formatted results with titles, summaries, and URLs
- Powered by SerpAPI

### File Reader Tool
- **PDF Files**: Extract text from PDF documents (first 5 pages)
- **CSV Files**: Provide summary with shape, columns, and sample data
- **Text Files**: Read and display text content

### Calculator Tool
- Mathematical calculations with safe evaluation
- Supports basic math, trigonometry, and numpy functions
- Examples: `sqrt(16) + 2*3`, `sin(pi/2)`, `np.mean([1,2,3,4,5])`

### CSV Analyzer Tool
- Statistical operations on CSV data
- Operations: sum, average, count, max, min
- Format: `file_path|operation column_name`

## 📁 File Upload Feature

The web interface includes a powerful file upload system:

### Supported File Types
- **📊 CSV Files**: Upload and analyze data files
- **📄 PDF Files**: Upload and extract text from documents
- **📝 Text Files**: Upload and analyze text content

### How to Use File Upload
1. **Upload Files**: Use the file uploader in the sidebar
2. **Quick Analysis**: Click "Quick Actions" buttons for instant analysis
3. **Chat Integration**: Ask the assistant to analyze uploaded files
4. **File Management**: View, analyze, and delete uploaded files

### Example File Analysis Queries
- "Read my uploaded CSV file and calculate the average sales"
- "Analyze the PDF report and extract key metrics"
- "Summarize the text file content"

## 📝 Example Queries

1. **Multi-step Search & Calculation**:
   ```
   Search for current Python trends and calculate what 25% of developers would be if there are 10 million developers worldwide
   ```

2. **File Analysis**:
   ```
   Read the file data.csv and calculate the average of the 'sales' column
   ```

3. **Complex Calculation**:
   ```
   Calculate the compound interest for $1000 at 5% for 10 years using the formula A = P(1+r)^t
   ```

4. **Web Search & Summary**:
   ```
   Search for latest AI news and summarize the key developments
   ```

## 📁 Project Structure

```
ai-assistant-tools/
├── .env                    # API keys configuration
├── requirements.txt        # Python dependencies
├── enhanced_main.py       # Main Gemini implementation
├── simple_gemini_assistant.py  # Simple version without LangChain
├── web_interface.py       # Streamlit web interface
├── examples.py            # Example usage scenarios
├── README.md              # This file
└── tools/
    ├── __init__.py
    ├── web_search.py      # Web search functionality
    ├── file_reader.py     # File processing tools
    ├── calculator.py      # Mathematical calculations
    └── csv_analyzer.py    # CSV data analysis
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Gemini API key (required)
- `SERPAPI_API_KEY`: Your SerpAPI key (optional, for web search)

### Model Settings
- **Model**: `gemini-1.5-pro` (latest version)
- **Temperature**: 0.7 (balanced creativity and accuracy)
- **Max Output Tokens**: 2048
- **Memory Window**: 10 exchanges

## 🧪 Testing

Run the example scenarios:
```bash
python examples.py
```

## 🔍 Troubleshooting

### Common Issues:

1. **API Key Errors**:
   - Ensure Gemini API key is properly set in `.env` file
   - Check that the key is valid and has sufficient quota

2. **Import Errors**:
   - Make sure you installed `langchain-google-genai` not `langchain-openai`
   - Run `pip install -r requirements.txt`

3. **File Path Issues**:
   - Use absolute paths or ensure relative paths are correct
   - Check file permissions

4. **Memory Issues**:
   - Large files may cause memory problems - implement chunking if needed
   - The assistant limits PDF reading to first 5 pages

5. **Rate Limits**:
   - Gemini has generous free limits (15 requests per minute)
   - Add delays if you encounter rate limiting

### Gemini-Specific Tips:
- Gemini works better with explicit instructions
- Use `convert_system_message_to_human=True` for better compatibility
- Set `max_output_tokens` to control response length
- The free tier has 15 requests per minute limit

### Model Issues:
If you encounter model errors, run the model checker:
```bash
python check_models.py
```

This will show available models and test connectivity.

## 📈 Advanced Features

### Custom Tools
You can easily add custom tools by creating new functions in the `tools/` directory and adding them to the assistant.

### Memory Persistence
The assistant uses conversation memory to maintain context across interactions.

### Error Recovery
Built-in error handling and retry mechanisms for robust operation.

## 🤝 Contributing

Feel free to contribute by:
- Adding new tools
- Improving error handling
- Enhancing the UI
- Adding new features

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Google Gemini for the AI model
- LangChain for the agent framework
- Streamlit for the web interface
- SerpAPI for web search capabilities

---

**Happy coding with your Personal AI Assistant! 🤖✨** 