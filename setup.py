#!/usr/bin/env python3
"""
Setup script for Personal AI Assistant
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        sys.exit(1)

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# API Keys Configuration
# Get your Gemini API key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_gemini_api_key_here

# Get your SerpAPI key from: https://serpapi.com/ (optional for web search)
SERPAPI_API_KEY=your_serpapi_key_here
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ .env file created")
        print("⚠️  Please update the .env file with your API keys")
    else:
        print("✅ .env file already exists")

def check_env_keys():
    """Check if API keys are set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    google_key = os.getenv('GOOGLE_API_KEY')
    serpapi_key = os.getenv('SERPAPI_API_KEY')
    
    if not google_key or google_key == 'your_gemini_api_key_here':
        print("⚠️  GOOGLE_API_KEY not set in .env file")
        print("   Get your free key from: https://makersuite.google.com/app/apikey")
    else:
        print("✅ GOOGLE_API_KEY is configured")
    
    if not serpapi_key or serpapi_key == 'your_serpapi_key_here':
        print("⚠️  SERPAPI_API_KEY not set (optional for web search)")
        print("   Get your key from: https://serpapi.com/")
    else:
        print("✅ SERPAPI_API_KEY is configured")

def create_directories():
    """Create necessary directories"""
    directories = ["tools"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created")

def main():
    """Main setup function"""
    print("🚀 Setting up Personal AI Assistant...\n")
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Install requirements
    install_requirements()
    
    # Create .env file
    create_env_file()
    
    # Check environment
    check_env_keys()
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Update the .env file with your API keys")
    print("2. Run the assistant:")
    print("   - Command line: python enhanced_main.py")
    print("   - Web interface: streamlit run web_interface.py")
    print("   - Simple version: python simple_gemini_assistant.py")
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main() 