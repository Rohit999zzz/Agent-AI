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
    
    # Sidebar with capabilities
    with st.sidebar:
        st.header("🛠️ Capabilities")
        st.write("• 🔍 Web search")
        st.write("• 📄 Read PDF files")
        st.write("• 📊 Analyze CSV data")
        st.write("• 🧮 Mathematical calculations")
        st.write("• 🔗 Chain multiple actions")
        
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
        
        # File upload in main chat area
        st.markdown("---")
        st.subheader("📁 Upload Files & Ask Questions")
        
        # File upload section
        uploaded_file = st.file_uploader(
            "Choose a file to analyze",
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
                
                # Custom query input for the uploaded file
                st.subheader(f"🔍 Ask Questions About {uploaded_file.name}")
                
                # Query input
                custom_query = st.text_area(
                    f"Ask a specific question about {uploaded_file.name}:",
                    placeholder=f"e.g., What are the key insights from {uploaded_file.name}?",
                    height=100,
                    key=f"query_{uploaded_file.name}"
                )
                
                # Query buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🔍 Analyze File", key=f"analyze_{uploaded_file.name}"):
                        if 'assistant' in st.session_state:
                            analysis_prompt = f"Read {file_path} and provide a comprehensive analysis"
                            st.session_state.messages.append({"role": "user", "content": analysis_prompt})
                            with st.spinner("Analyzing..."):
                                response = st.session_state.assistant.chat(analysis_prompt)
                                st.session_state.messages.append({"role": "assistant", "content": response})
                            st.rerun()
                        else:
                            st.error("Assistant not initialized")
                
                with col2:
                    if st.button("❓ Ask Custom Question", key=f"custom_{uploaded_file.name}"):
                        if custom_query and 'assistant' in st.session_state:
                            custom_prompt = f"Read {file_path} and answer this specific question: {custom_query}"
                            st.session_state.messages.append({"role": "user", "content": custom_prompt})
                            with st.spinner("Processing custom query..."):
                                response = st.session_state.assistant.chat(custom_prompt)
                                st.session_state.messages.append({"role": "assistant", "content": response})
                            st.rerun()
                        elif not custom_query:
                            st.warning("Please enter a question first")
                        else:
                            st.error("Assistant not initialized")
                
                # Quick question suggestions
                st.subheader("💡 Quick Questions")
                quick_questions = []
                
                if uploaded_file.name.endswith('.csv'):
                    quick_questions = [
                        f"What are the main trends in {uploaded_file.name}?",
                        f"Calculate the average of all numeric columns in {uploaded_file.name}",
                        f"What are the top 5 values in {uploaded_file.name}?",
                        f"Are there any missing values in {uploaded_file.name}?",
                        f"What insights can you draw from {uploaded_file.name}?"
                    ]
                elif uploaded_file.name.endswith('.pdf'):
                    quick_questions = [
                        f"Summarize the key points from {uploaded_file.name}",
                        f"What are the main conclusions in {uploaded_file.name}?",
                        f"Extract all important dates and numbers from {uploaded_file.name}",
                        f"What are the recommendations in {uploaded_file.name}?",
                        f"List the key findings from {uploaded_file.name}"
                    ]
                elif uploaded_file.name.endswith('.txt'):
                    quick_questions = [
                        f"What are the main themes in {uploaded_file.name}?",
                        f"Summarize the key information in {uploaded_file.name}",
                        f"What are the important points mentioned in {uploaded_file.name}?",
                        f"Extract any numerical data from {uploaded_file.name}",
                        f"What insights can you provide from {uploaded_file.name}?"
                    ]
                
                for i, question in enumerate(quick_questions):
                    if st.button(question, key=f"quick_{uploaded_file.name}_{i}"):
                        if 'assistant' in st.session_state:
                            quick_prompt = f"Read {file_path} and answer: {question}"
                            st.session_state.messages.append({"role": "user", "content": quick_prompt})
                            with st.spinner("Processing..."):
                                response = st.session_state.assistant.chat(quick_prompt)
                                st.session_state.messages.append({"role": "assistant", "content": response})
                            st.rerun()
                        else:
                            st.error("Assistant not initialized")
        
        # Regular chat input
        st.markdown("---")
        st.subheader("💬 Chat with AI Assistant")
        
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
        
        # File analysis suggestions
        if st.session_state.uploaded_files:
            st.subheader("📁 Analyze Files")
            
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
        
        # Custom query suggestions
        if st.session_state.uploaded_files:
            st.subheader("💡 Custom Questions")
            
            for filename, filepath in st.session_state.uploaded_files.items():
                if filename.endswith('.csv'):
                    suggestions = [
                        f"Analyze trends in {filename}",
                        f"Calculate averages in {filename}",
                        f"Find insights in {filename}",
                        f"Check for missing data in {filename}"
                    ]
                elif filename.endswith('.pdf'):
                    suggestions = [
                        f"Summarize {filename}",
                        f"Extract key points from {filename}",
                        f"Find conclusions in {filename}",
                        f"List recommendations in {filename}"
                    ]
                elif filename.endswith('.txt'):
                    suggestions = [
                        f"Summarize {filename}",
                        f"Extract key information from {filename}",
                        f"Find main themes in {filename}",
                        f"List important points in {filename}"
                    ]
                
                for suggestion in suggestions:
                    if st.button(suggestion, key=f"suggest_{filename}_{suggestion}"):
                        st.session_state.messages.append({"role": "user", "content": suggestion})
                        with st.spinner("Processing..."):
                            response = st.session_state.assistant.chat(suggestion)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
        
        st.subheader("📊 Sample Data")
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