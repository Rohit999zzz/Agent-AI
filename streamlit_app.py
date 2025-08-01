#!/usr/bin/env python3
"""
Personal AI Assistant - Streamlit Cloud Deployment
Main app file for deployment on Streamlit Cloud
"""

import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

# Import the assistant (with error handling for deployment)
try:
    from enhanced_main import EnhancedPersonalAIAssistant
    ASSISTANT_AVAILABLE = True
except Exception as e:
    st.error(f"Failed to import assistant: {e}")
    ASSISTANT_AVAILABLE = False

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temporary location"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def get_file_context():
    """Get context about uploaded files for the assistant"""
    if not st.session_state.uploaded_files:
        return ""
    
    context = "\n\n**Available Files:**\n"
    for filename, filepath in st.session_state.uploaded_files.items():
        context += f"- {filename} (saved at: {filepath})\n"
    context += "\nYou can ask questions about these files directly. For example:\n"
    context += "- 'Tell me about the PDF file'\n"
    context += "- 'Analyze the CSV data'\n"
    context += "- 'What are the key points in the document?'\n"
    return context

def main():
    st.set_page_config(
        page_title="Personal AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
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
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        st.error("⚠️ **GOOGLE_API_KEY not found!**")
        st.info("""
        To use this app, you need to set your Gemini API key:
        
        1. Get your free API key from: https://makersuite.google.com/app/apikey
        2. In Streamlit Cloud, go to your app settings
        3. Add a secret: `GOOGLE_API_KEY` with your API key value
        
        **For local development:** Create a `.env` file with:
        ```
        GOOGLE_API_KEY=your_api_key_here
        ```
        """)
        return
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    
    if 'assistant' not in st.session_state and ASSISTANT_AVAILABLE:
        try:
            with st.spinner("Initializing AI Assistant..."):
                st.session_state.assistant = EnhancedPersonalAIAssistant()
            st.success("✅ AI Assistant initialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize assistant: {e}")
            st.info("Please check your API key and try again.")
            return
    
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
                            # Check if file exists before trying to delete
                            if os.path.exists(filepath):
                                os.unlink(filepath)
                            # Remove from session state regardless
                            del st.session_state.uploaded_files[filename]
                            st.success(f"✅ {filename} deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Could not delete {filename}: {str(e)}")
                            # Still remove from session state even if file deletion fails
                            if filename in st.session_state.uploaded_files:
                                del st.session_state.uploaded_files[filename]
                            st.rerun()
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
                if 'assistant' in st.session_state:
                    # Add file context to the example
                    file_context = get_file_context()
                    enhanced_example = example + file_context
                    
                    st.session_state.messages.append({"role": "user", "content": example})
                    with st.spinner("Processing..."):
                        response = st.session_state.assistant.chat(enhanced_example)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
                else:
                    st.error("Assistant not initialized")
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
                    
                    # Auto-add a welcome message about the uploaded file
                    welcome_msg = f"I've uploaded {uploaded_file.name}. You can now ask me questions about this file!"
                    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
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
                    
                    # Auto-add a message about the new file
                    new_file_msg = f"I've also uploaded {uploaded_file.name}. You can ask questions about any of the uploaded files!"
                    st.session_state.messages.append({"role": "assistant", "content": new_file_msg})
                    st.rerun()
        
        # Chat input
        if prompt := st.chat_input("Ask me anything! Upload files and ask questions about them..."):
            if 'assistant' in st.session_state:
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Enhance prompt with file context
                file_context = get_file_context()
                enhanced_prompt = prompt + file_context
                
                # Get assistant response
                with st.chat_message("assistant"):
                    with st.spinner("🤔 Thinking..."):
                        response = st.session_state.assistant.chat(enhanced_prompt)
                        st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.error("Assistant not initialized. Please check your API key.")
        
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
                        if 'assistant' in st.session_state:
                            # Add file context to the suggestion
                            file_context = get_file_context()
                            enhanced_suggestion = suggestion + file_context
                            
                            st.session_state.messages.append({"role": "user", "content": suggestion})
                            with st.spinner("Processing..."):
                                response = st.session_state.assistant.chat(enhanced_suggestion)
                                st.session_state.messages.append({"role": "assistant", "content": response})
                            st.rerun()
                        else:
                            st.error("Assistant not initialized")
        
        st.subheader("📊 Sample Data")
        if st.button("📊 Sample CSV") and 'assistant' in st.session_state:
            sample_prompt = "Read sample_data.csv and calculate the total revenue"
            st.session_state.messages.append({"role": "user", "content": sample_prompt})
            with st.spinner("Processing..."):
                response = st.session_state.assistant.chat(sample_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("📄 Sample Report") and 'assistant' in st.session_state:
            report_prompt = "Read sample_report.txt and extract the key metrics"
            st.session_state.messages.append({"role": "user", "content": report_prompt})
            with st.spinner("Processing..."):
                response = st.session_state.assistant.chat(report_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px;'>
        <p>🤖 Personal AI Assistant | Powered by Google Gemini | Built with Streamlit</p>
        <p>Upload files and ask questions in the same chat interface!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 