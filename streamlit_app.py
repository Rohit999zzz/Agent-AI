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

def main():
    st.set_page_config(
        page_title="Personal AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 Personal AI Assistant with Tools (Powered by Gemini)")
    st.markdown("---")
    
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
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Capabilities")
        st.write("• 🔍 Web search")
        st.write("• 📄 Read PDF files")
        st.write("• 📊 Analyze CSV data")
        st.write("• 🧮 Mathematical calculations")
        st.write("• 🔗 Chain multiple actions")
        
        st.header("📁 File Upload")
        st.write("Upload files to analyze them:")
        
        # File upload section
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'pdf', 'txt'],
            help="Upload CSV, PDF, or text files to analyze"
        )
        
        if uploaded_file is not None:
            # Save uploaded file
            file_path = save_uploaded_file(uploaded_file)
            if file_path:
                st.session_state.uploaded_files[uploaded_file.name] = file_path
                st.success(f"✅ {uploaded_file.name} uploaded successfully!")
                
                # Show file info
                file_size = len(uploaded_file.getvalue())
                st.write(f"**File Size:** {file_size:,} bytes")
                st.write(f"**File Type:** {uploaded_file.type}")
        
        # Show uploaded files with custom query functionality
        if st.session_state.uploaded_files:
            st.header("📋 Uploaded Files")
            for filename, filepath in st.session_state.uploaded_files.items():
                with st.expander(f"📄 {filename}", expanded=False):
                    # File info
                    st.write(f"**Path:** {filepath}")
                    
                    # Custom query section
                    st.subheader("🔍 Ask Custom Questions")
                    
                    # Query input
                    query_key = f"query_{filename}"
                    custom_query = st.text_area(
                        "Ask a specific question about this file:",
                        key=query_key,
                        placeholder="e.g., What are the key insights from this data?",
                        height=100
                    )
                    
                    # Query buttons
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col1:
                        if st.button("🔍 Analyze", key=f"analyze_{filename}"):
                            if 'assistant' in st.session_state:
                                analysis_prompt = f"Read {filepath} and provide a comprehensive analysis"
                                st.session_state.messages.append({"role": "user", "content": analysis_prompt})
                                with st.spinner("Analyzing..."):
                                    response = st.session_state.assistant.chat(analysis_prompt)
                                    st.session_state.messages.append({"role": "assistant", "content": response})
                                st.rerun()
                            else:
                                st.error("Assistant not initialized")
                    
                    with col2:
                        if st.button("❓ Custom Query", key=f"custom_{filename}"):
                            if custom_query and 'assistant' in st.session_state:
                                custom_prompt = f"Read {filepath} and answer this specific question: {custom_query}"
                                st.session_state.messages.append({"role": "user", "content": custom_prompt})
                                with st.spinner("Processing custom query..."):
                                    response = st.session_state.assistant.chat(custom_prompt)
                                    st.session_state.messages.append({"role": "assistant", "content": response})
                                st.rerun()
                            elif not custom_query:
                                st.warning("Please enter a question first")
                            else:
                                st.error("Assistant not initialized")
                    
                    with col3:
                        if st.button("🗑️ Delete", key=f"del_{filename}"):
                            try:
                                os.unlink(filepath)
                                del st.session_state.uploaded_files[filename]
                                st.rerun()
                            except:
                                st.error("Could not delete file")
                    
                    # Quick query suggestions
                    st.subheader("💡 Quick Questions")
                    quick_questions = []
                    
                    if filename.endswith('.csv'):
                        quick_questions = [
                            "What are the main trends in this data?",
                            "Calculate the average of all numeric columns",
                            "What are the top 5 values in this dataset?",
                            "Are there any missing values in this data?",
                            "What insights can you draw from this data?"
                        ]
                    elif filename.endswith('.pdf'):
                        quick_questions = [
                            "Summarize the key points from this document",
                            "What are the main conclusions?",
                            "Extract all important dates and numbers",
                            "What are the recommendations in this document?",
                            "List the key findings from this report"
                        ]
                    elif filename.endswith('.txt'):
                        quick_questions = [
                            "What are the main themes in this text?",
                            "Summarize the key information",
                            "What are the important points mentioned?",
                            "Extract any numerical data from this text",
                            "What insights can you provide from this content?"
                        ]
                    
                    for i, question in enumerate(quick_questions):
                        if st.button(question, key=f"quick_{filename}_{i}"):
                            if 'assistant' in st.session_state:
                                quick_prompt = f"Read {filepath} and answer: {question}"
                                st.session_state.messages.append({"role": "user", "content": quick_prompt})
                                with st.spinner("Processing..."):
                                    response = st.session_state.assistant.chat(quick_prompt)
                                    st.session_state.messages.append({"role": "assistant", "content": response})
                                st.rerun()
                            else:
                                st.error("Assistant not initialized")
        
        st.header("📝 Example Queries")
        examples = [
            "Search for latest AI news and summarize",
            "Calculate 15% of 1250",
            "Read data.csv and find the average sales",
            "Search Python tutorials and calculate study time for 10 topics at 2 hours each"
        ]
        
        for example in examples:
            if st.button(example, key=example):
                if 'assistant' in st.session_state:
                    st.session_state.messages.append({"role": "user", "content": example})
                    with st.spinner("Processing..."):
                        response = st.session_state.assistant.chat(example)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
                else:
                    st.error("Assistant not initialized")
    
    # Main chat area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything! I can search the web, read files, do calculations, and more..."):
            if 'assistant' in st.session_state:
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
            else:
                st.error("Assistant not initialized. Please check your API key.")
    
    with col2:
        st.header("📊 Quick Actions")
        
        # Quick file analysis buttons
        if st.session_state.uploaded_files and 'assistant' in st.session_state:
            st.subheader("Analyze Files")
            
            for filename, filepath in st.session_state.uploaded_files.items():
                if filename.endswith('.csv'):
                    if st.button(f"📊 Analyze {filename}", key=f"quick_analyze_{filename}"):
                        analysis_prompt = f"Read {filepath} and provide a summary of the data"
                        st.session_state.messages.append({"role": "user", "content": analysis_prompt})
                        with st.spinner("Analyzing..."):
                            response = st.session_state.assistant.chat(analysis_prompt)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
                
                elif filename.endswith('.pdf'):
                    if st.button(f"📄 Read {filename}", key=f"quick_read_{filename}"):
                        read_prompt = f"Read {filepath} and summarize the content"
                        st.session_state.messages.append({"role": "user", "content": read_prompt})
                        with st.spinner("Reading..."):
                            response = st.session_state.assistant.chat(read_prompt)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
        
        st.subheader("Sample Data")
        if st.button("📊 Load Sample CSV") and 'assistant' in st.session_state:
            sample_prompt = "Read sample_data.csv and calculate the total revenue"
            st.session_state.messages.append({"role": "user", "content": sample_prompt})
            with st.spinner("Processing..."):
                response = st.session_state.assistant.chat(sample_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("📄 Load Sample Report") and 'assistant' in st.session_state:
            report_prompt = "Read sample_report.txt and extract the key metrics"
            st.session_state.messages.append({"role": "user", "content": report_prompt})
            with st.spinner("Processing..."):
                response = st.session_state.assistant.chat(report_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🤖 Personal AI Assistant | Powered by Google Gemini | Built with Streamlit</p>
        <p>Upload files, ask questions, and get intelligent responses!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 