#!/usr/bin/env python3
"""
File Upload Demo - Shows how to use file upload with the AI Assistant
"""

import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

def main():
    st.set_page_config(
        page_title="File Upload Demo",
        page_icon="📁",
        layout="wide"
    )
    
    st.title("📁 File Upload Demo")
    st.write("This demo shows how to upload and analyze files with the AI Assistant")
    
    # Check for API key
    load_dotenv()
    if not os.getenv('GOOGLE_API_KEY'):
        st.error("Please set your GOOGLE_API_KEY in the .env file")
        st.info("Get your free API key from: https://makersuite.google.com/app/apikey")
        return
    
    # File upload section
    st.header("📤 Upload Your Files")
    
    uploaded_files = st.file_uploader(
        "Choose files to analyze",
        type=['csv', 'pdf', 'txt'],
        accept_multiple_files=True,
        help="Upload multiple CSV, PDF, or text files"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")
        
        # Display uploaded files
        st.header("📋 Uploaded Files")
        
        for uploaded_file in uploaded_files:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"📄 **{uploaded_file.name}**")
                st.write(f"Type: {uploaded_file.type}")
                st.write(f"Size: {len(uploaded_file.getvalue()):,} bytes")
            
            with col2:
                if st.button("📊 Analyze", key=f"analyze_{uploaded_file.name}"):
                    st.info("Analysis would be performed here")
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{uploaded_file.name}"):
                    st.info("File would be deleted here")
            
            st.divider()
    
    # Instructions
    st.header("📖 How to Use File Upload")
    
    st.subheader("1. Upload Files")
    st.write("""
    - Click the "Browse files" button in the sidebar
    - Select CSV, PDF, or text files from your computer
    - Files will be uploaded and saved temporarily
    """)
    
    st.subheader("2. Analyze Files")
    st.write("""
    - Use the "Quick Actions" buttons to analyze uploaded files
    - Or ask the assistant directly: "Read my_file.csv and summarize the data"
    - The assistant will automatically use the uploaded file paths
    """)
    
    st.subheader("3. Supported File Types")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📊 CSV Files**")
        st.write("- Data analysis")
        st.write("- Statistical operations")
        st.write("- Column summaries")
    
    with col2:
        st.write("**📄 PDF Files**")
        st.write("- Text extraction")
        st.write("- Content summarization")
        st.write("- Key information extraction")
    
    with col3:
        st.write("**📝 Text Files**")
        st.write("- Content reading")
        st.write("- Text analysis")
        st.write("- Information extraction")
    
    st.header("🚀 Start Using")
    st.write("""
    To start using the full AI Assistant with file upload:
    
    ```bash
    streamlit run web_interface.py
    ```
    
    This will open the complete interface with:
    - File upload functionality
    - Chat interface
    - Tool integration
    - Quick analysis buttons
    """)

if __name__ == "__main__":
    main() 