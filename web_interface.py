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
    
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    
    # Sidebar with capabilities and file upload
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
                st.info(f"File saved as: {file_path}")
                
                # Show file info
                file_size = len(uploaded_file.getvalue())
                st.write(f"**File Size:** {file_size:,} bytes")
                st.write(f"**File Type:** {uploaded_file.type}")
        
        # Show uploaded files
        if st.session_state.uploaded_files:
            st.header("📋 Uploaded Files")
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
    
    # Main chat area
    col1, col2 = st.columns([3, 1])
    
    with col1:
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
    
    with col2:
        st.header("📊 Quick Actions")
        
        # Quick file analysis buttons
        if st.session_state.uploaded_files:
            st.subheader("Analyze Files")
            
            for filename, filepath in st.session_state.uploaded_files.items():
                if filename.endswith('.csv'):
                    if st.button(f"📊 Analyze {filename}", key=f"analyze_{filename}"):
                        # Add analysis request to chat
                        analysis_prompt = f"Read {filepath} and provide a summary of the data"
                        st.session_state.messages.append({"role": "user", "content": analysis_prompt})
                        with st.spinner("Analyzing..."):
                            response = st.session_state.assistant.chat(analysis_prompt)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
                
                elif filename.endswith('.pdf'):
                    if st.button(f"📄 Read {filename}", key=f"read_{filename}"):
                        # Add read request to chat
                        read_prompt = f"Read {filepath} and summarize the content"
                        st.session_state.messages.append({"role": "user", "content": read_prompt})
                        with st.spinner("Reading..."):
                            response = st.session_state.assistant.chat(read_prompt)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
        
        st.subheader("Sample Data")
        if st.button("📊 Load Sample CSV"):
            # Add sample data analysis
            sample_prompt = "Read sample_data.csv and calculate the total revenue"
            st.session_state.messages.append({"role": "user", "content": sample_prompt})
            with st.spinner("Processing..."):
                response = st.session_state.assistant.chat(sample_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("📄 Load Sample Report"):
            # Add sample report analysis
            report_prompt = "Read sample_report.txt and extract the key metrics"
            st.session_state.messages.append({"role": "user", "content": report_prompt})
            with st.spinner("Processing..."):
                response = st.session_state.assistant.chat(report_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

if __name__ == "__main__":
    main() 