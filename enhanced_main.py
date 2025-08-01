import os
import sys
import time
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
        
        # Try different models in order of preference
        self.llm = self._initialize_llm()
        
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
    
    def _initialize_llm(self):
        """Initialize LLM with fallback models"""
        models_to_try = [
            "gemini-1.5-flash",  # Faster, less quota usage
            "gemini-1.5-pro",    # Most capable
            "gemini-pro"          # Legacy fallback
        ]
        
        for model_name in models_to_try:
            try:
                print(f"🔄 Trying model: {model_name}")
                llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    temperature=0.7,
                    google_api_key=os.getenv('GOOGLE_API_KEY'),
                    convert_system_message_to_human=True,
                    max_output_tokens=2048
                )
                
                # Test the model with a simple query
                test_response = llm.invoke("Hello")
                print(f"✅ Successfully initialized with {model_name}")
                return llm
                
            except Exception as e:
                print(f"❌ Failed with {model_name}: {str(e)[:100]}...")
                if "quota" in str(e).lower() or "rate" in str(e).lower():
                    print("⚠️  Rate limit exceeded, trying next model...")
                    time.sleep(2)  # Wait before trying next model
                continue
        
        # If all models fail, raise an error
        raise Exception("All Gemini models failed to initialize. Please check your API key and quota.")
    
    def chat(self, message):
        """Enhanced chat with error handling and rate limiting"""
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
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
                error_msg = str(e)
                if "quota" in error_msg.lower() or "rate" in error_msg.lower():
                    if attempt < max_retries - 1:
                        print(f"⚠️  Rate limit hit, waiting {retry_delay} seconds before retry...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        return "I'm experiencing high demand right now. Please try again in a few minutes."
                else:
                    return f"I encountered an error: {error_msg}. Please try rephrasing your request."
        
        return "Sorry, I'm unable to process your request right now. Please try again later."
    
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
        print("If you're getting quota errors, try again in a few minutes or check your API usage.")

if __name__ == "__main__":
    main() 