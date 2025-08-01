#!/usr/bin/env python3
"""
Script to check available Gemini models and troubleshoot model issues
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

def check_available_models():
    """Check and display available Gemini models"""
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        print("Please add your API key to the .env file")
        return
    
    try:
        genai.configure(api_key=api_key)
        
        # List available models
        print("🔍 Checking available models...")
        models = genai.list_models()
        
        print("\n📋 Available Models:")
        print("=" * 50)
        
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"✅ {model.name}")
                print(f"   Display Name: {model.display_name}")
                print(f"   Description: {model.description}")
                print(f"   Generation Methods: {model.supported_generation_methods}")
                print("-" * 30)
        
        # Test specific models
        test_models = [
            "gemini-1.5-pro",
            "gemini-1.5-flash", 
            "gemini-pro",
            "gemini-pro-vision"
        ]
        
        print("\n🧪 Testing Model Access:")
        print("=" * 50)
        
        for model_name in test_models:
            try:
                model = genai.GenerativeModel(model_name)
                print(f"✅ {model_name} - Available")
            except Exception as e:
                print(f"❌ {model_name} - Error: {str(e)}")
        
        print("\n💡 Recommended Models:")
        print("- gemini-1.5-pro (latest, most capable)")
        print("- gemini-1.5-flash (faster, good for simple tasks)")
        print("- gemini-pro (legacy, still works)")
        
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        print("Please check your API key and internet connection")

def test_model_connection():
    """Test basic model connection"""
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found")
        return False
    
    try:
        genai.configure(api_key=api_key)
        
        # Try to create a model instance
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Test with a simple prompt
        response = model.generate_content("Hello, can you respond with 'OK'?")
        
        if response.text:
            print("✅ Model connection successful!")
            print(f"Response: {response.text}")
            return True
        else:
            print("❌ No response from model")
            return False
            
    except Exception as e:
        print(f"❌ Model connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Gemini Model Checker")
    print("=" * 50)
    
    print("\n1. Testing model connection...")
    if test_model_connection():
        print("\n2. Checking available models...")
        check_available_models()
    else:
        print("\n❌ Cannot proceed without successful model connection")
        print("Please check your API key and try again") 