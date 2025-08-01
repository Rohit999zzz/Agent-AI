import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from enhanced_main import EnhancedPersonalAIAssistant

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temporary location"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def main():
    st.set_page_config(
        page_title="Personal AI Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    # Custom CSS for clean ChatGPT-like interface
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    .file-upload-area {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        background-color: #f8f9fa;
    }
    .file-info {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .quick-questions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 15px 0;
    }
    .quick-question-btn {
        background-color: #f0f0f0;
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .quick-question-btn:hover {
        background-color: #e0e0e0;
    }
    .sidebar-section {
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🤖 Personal AI Assistant</h1>', unsafe_allow_html=True)
    
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
    
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    
    # Sidebar - Clean and minimal
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("🛠️ Capabilities")
        st.write("• 🔍 Web search")
        st.write("• 📄 Read PDF files")
        st.write("• 📊 Analyze CSV data")
        st.write("• 🧮 Mathematical calculations")
        st.write("• 🔗 Chain multiple actions")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("📋 Uploaded Files")
        if st.session_state.uploaded_files:
            for filename, filepath in st.session_state.uploaded_files.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"📄 {filename}")
                with col2:
                    if st.button("🗑️", key=f"del_{filename}"):
                        try:
                            os.unlink(filepath)
                            del st.session_state.uploaded_files[filename]
                            st.rerun()
                        except:
                            st.error("Could not delete file")
        else:
            st.write("No files uploaded yet")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("📝 Examples")
        examples = [
            "Search for latest AI news",
            "Calculate 15% of 1250",
            "What are the trends in my data?",
            "Summarize this document"
        ]
        
        for example in examples:
            if st.button(example, key=example):
                # Add to chat
                st.session_state.messages.append({"role": "user", "content": example})
                with st.spinner("Processing..."):
                    response = st.session_state.assistant.chat(example)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat area - Clean and focused
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # File upload area - Clean and integrated
        if not st.session_state.uploaded_files:
            st.markdown('<div class="file-upload-area">', unsafe_allow_html=True)
            st.subheader("📁 Upload Files to Analyze")
            st.write("Upload CSV, PDF, or text files to ask questions about them")
            
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['csv', 'pdf', 'txt'],
                help="Upload files to analyze"
            )
            
            if uploaded_file is not None:
                file_path = save_uploaded_file(uploaded_file)
                if file_path:
                    st.session_state.uploaded_files[uploaded_file.name] = file_path
                    st.success(f"✅ {uploaded_file.name} uploaded!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input with file upload integration
        st.markdown("---")
        
        # File upload in chat input area
        if st.session_state.uploaded_files:
            uploaded_file = st.file_uploader(
                "📁 Add more files",
                type=['csv', 'pdf', 'txt'],
                help="Upload additional files",
                key="additional_files"
            )
            
            if uploaded_file is not None:
                file_path = save_uploaded_file(uploaded_file)
                if file_path:
                    st.session_state.uploaded_files[uploaded_file.name] = file_path
                    st.success(f"✅ {uploaded_file.name} uploaded!")
                    st.rerun()
        
        # Chat input
        if prompt := st.chat_input("Ask me anything! Upload files and ask questions about them..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    response = st.session_state.assistant.chat(prompt)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.header("💡 Quick Actions")
        
        # File analysis suggestions
        if st.session_state.uploaded_files:
            st.subheader("📁 Your Files")
            
            for filename, filepath in st.session_state.uploaded_files.items():
                if filename.endswith('.csv'):
                    if st.button(f"📊 {filename}", key=f"quick_analyze_{filename}"):
                        analysis_prompt = f"Read {filepath} and provide a summary of the data"
                        st.session_state.messages.append({"role": "user", "content": analysis_prompt})
                        with st.spinner("Analyzing..."):
                            response = st.session_state.assistant.chat(analysis_prompt)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
                
                elif filename.endswith('.pdf'):
                    if st.button(f"📄 {filename}", key=f"quick_read_{filename}"):
                        read_prompt = f"Read {filepath} and summarize the content"
                        st.session_state.messages.append({"role": "user", "content": read_prompt})
                        with st.spinner("Reading..."):
                            response = st.session_state.assistant.chat(read_prompt)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
                
                elif filename.endswith('.txt'):
                    if st.button(f"📝 {filename}", key=f"quick_read_{filename}"):
                        read_prompt = f"Read {filepath} and summarize the content"
                        st.session_state.messages.append({"role": "user", "content": read_prompt})
                        with st.spinner("Reading..."):
                            response = st.session_state.assistant.chat(read_prompt)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
        
        # Quick suggestions for uploaded files
        if st.session_state.uploaded_files:
            st.subheader("💡 Quick Questions")
            
            for filename, filepath in st.session_state.uploaded_files.items():
                if filename.endswith('.csv'):
                    suggestions = [
                        f"Analyze trends in {filename}",
                        f"Calculate averages in {filename}",
                        f"Find insights in {filename}"
                    ]
                elif filename.endswith('.pdf'):
                    suggestions = [
                        f"Summarize {filename}",
                        f"Extract key points from {filename}",
                        f"Find conclusions in {filename}"
                    ]
                elif filename.endswith('.txt'):
                    suggestions = [
                        f"Summarize {filename}",
                        f"Extract key information from {filename}",
                        f"Find main themes in {filename}"
                    ]
                
                for suggestion in suggestions:
                    if st.button(suggestion, key=f"suggest_{filename}_{suggestion}"):
                        st.session_state.messages.append({"role": "user", "content": suggestion})
                        with st.spinner("Processing..."):
                            response = st.session_state.assistant.chat(suggestion)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
        
        st.subheader("📊 Sample Data")
        if st.button("📊 Sample CSV"):
            # Add sample data analysis
            sample_prompt = "Read sample_data.csv and calculate the total revenue"
            st.session_state.messages.append({"role": "user", "content": sample_prompt})
            with st.spinner("Processing..."):
                response = st.session_state.assistant.chat(sample_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("📄 Sample Report"):
            # Add sample report analysis
            report_prompt = "Read sample_report.txt and extract the key metrics"
            st.session_state.messages.append({"role": "user", "content": report_prompt})
            with st.spinner("Processing..."):
                response = st.session_state.assistant.chat(report_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

if __name__ == "__main__":
    main() 