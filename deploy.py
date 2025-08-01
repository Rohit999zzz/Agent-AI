#!/usr/bin/env python3
"""
Deployment Helper Script
Prepares your project for Streamlit Cloud deployment
"""

import os
import shutil
import subprocess
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    required_files = [
        'streamlit_app.py',
        'enhanced_main.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'sample_data.csv',
        'sample_report.txt',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found!")
    return True

def check_tools_directory():
    """Check if tools directory has all required files"""
    tools_files = [
        'tools/__init__.py',
        'tools/web_search.py',
        'tools/file_reader.py',
        'tools/calculator.py',
        'tools/csv_analyzer.py'
    ]
    
    missing_tools = []
    for file in tools_files:
        if not os.path.exists(file):
            missing_tools.append(file)
    
    if missing_tools:
        print("❌ Missing tools files:")
        for file in missing_tools:
            print(f"   - {file}")
        return False
    
    print("✅ All tools files found!")
    return True

def create_gitignore():
    """Create .gitignore file if it doesn't exist"""
    gitignore_content = """
# Environment variables
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Temporary files
*.tmp
*.temp
"""
    
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content.strip())
        print("✅ Created .gitignore file")
    else:
        print("✅ .gitignore file already exists")

def check_git_status():
    """Check git status and provide instructions"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository initialized")
            print("\n📋 Git Status:")
            print(result.stdout)
        else:
            print("❌ Git repository not initialized")
            print("Run: git init")
    except FileNotFoundError:
        print("❌ Git not found. Please install Git first.")

def create_deployment_checklist():
    """Create a deployment checklist"""
    checklist = """
# 🚀 Streamlit Cloud Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Files Ready
- [ ] streamlit_app.py (main deployment file)
- [ ] enhanced_main.py (assistant implementation)
- [ ] tools/ directory (all tool files)
- [ ] requirements.txt (dependencies)
- [ ] .streamlit/config.toml (configuration)
- [ ] packages.txt (system dependencies)
- [ ] sample_data.csv (sample data)
- [ ] sample_report.txt (sample report)
- [ ] README.md (documentation)

### 2. API Keys Ready
- [ ] Google Gemini API key from https://makersuite.google.com/app/apikey
- [ ] SerpAPI key (optional) from https://serpapi.com/

### 3. GitHub Repository
- [ ] Repository created on GitHub
- [ ] All files committed and pushed
- [ ] Repository is public (for free Streamlit Cloud)

## 🚀 Deployment Steps

### Step 1: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set app path to: `streamlit_app.py`
6. Click "Deploy!"

### Step 2: Configure Secrets
1. In your deployed app, click Settings (⚙️)
2. Scroll to "Secrets"
3. Add your API keys:
   ```toml
   GOOGLE_API_KEY = "your_gemini_api_key_here"
   SERPAPI_API_KEY = "your_serpapi_key_here"
   ```
4. Click "Save"

### Step 3: Test Your App
1. Wait for deployment to complete
2. Test file upload functionality
3. Test chat interface
4. Test sample data analysis

## 🔧 Troubleshooting

### Common Issues:
- **Module not found**: Check requirements.txt includes all dependencies
- **API key not found**: Verify secret name is exactly `GOOGLE_API_KEY`
- **App not loading**: Check logs in Streamlit Cloud dashboard
- **Rate limiting**: Check your Gemini API quota

### Debugging:
1. Test locally first: `streamlit run streamlit_app.py`
2. Check logs in Streamlit Cloud dashboard
3. Verify API key: `python check_models.py`

## 🎉 Success!

Your app will be available at:
```
https://YOUR_APP_NAME-YOUR_USERNAME.streamlit.app
```

## 📞 Support

- Check Streamlit Cloud logs for errors
- Verify API keys are correctly set
- Test locally to isolate issues
"""
    
    with open('DEPLOYMENT_CHECKLIST.md', 'w', encoding='utf-8') as f:
        f.write(checklist.strip())
    print("✅ Created DEPLOYMENT_CHECKLIST.md")

def main():
    """Main deployment helper function"""
    print("🚀 Streamlit Cloud Deployment Helper")
    print("=" * 50)
    
    # Check files
    if not check_files():
        print("\n❌ Please fix missing files before deployment")
        return
    
    if not check_tools_directory():
        print("\n❌ Please fix missing tools files before deployment")
        return
    
    # Create .gitignore
    create_gitignore()
    
    # Check git status
    check_git_status()
    
    # Create deployment checklist
    create_deployment_checklist()
    
    print("\n🎉 Deployment preparation complete!")
    print("\n📋 Next steps:")
    print("1. Review DEPLOYMENT_CHECKLIST.md")
    print("2. Push your code to GitHub")
    print("3. Deploy on Streamlit Cloud")
    print("4. Configure API keys in Streamlit Cloud")
    print("\n📖 For detailed instructions, see DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main() 