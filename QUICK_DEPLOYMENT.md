# 🚀 Quick Streamlit Cloud Deployment

## ⚡ 5-Minute Deployment Guide

### Step 1: Prepare Your Code
```bash
# Run the deployment helper
python deploy.py

# Initialize git repository
git init
git add .
git commit -m "Initial commit: Personal AI Assistant"
```

### Step 2: Push to GitHub
```bash
# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set app path to: `streamlit_app.py`
6. Click "Deploy!"

### Step 4: Configure API Keys
1. In your deployed app, click Settings (⚙️)
2. Scroll to "Secrets"
3. Add your API keys:
   ```toml
   GOOGLE_API_KEY = "your_gemini_api_key_here"
   SERPAPI_API_KEY = "your_serpapi_key_here"
   ```
4. Click "Save"

### Step 5: Test Your App
Your app will be available at:
```
https://YOUR_APP_NAME-YOUR_USERNAME.streamlit.app
```

## 🎯 What You Get

✅ **File Upload**: Upload CSV, PDF, and text files  
✅ **Web Search**: Search the internet for current information  
✅ **Calculations**: Perform mathematical operations  
✅ **Chat Interface**: Natural language interaction  
✅ **Quick Analysis**: One-click file analysis  
✅ **Multi-step Reasoning**: Chain multiple actions together  

## 🔧 Troubleshooting

### Common Issues:
- **"Module not found"**: Check `requirements.txt` includes all dependencies
- **"API key not found"**: Verify secret name is exactly `GOOGLE_API_KEY`
- **"App not loading"**: Check logs in Streamlit Cloud dashboard

### Quick Fixes:
```bash
# Test locally first
streamlit run streamlit_app.py

# Check API key
python check_models.py

# Verify all files
python deploy.py
```

## 📞 Need Help?

1. Check the logs in Streamlit Cloud dashboard
2. Verify your API key is valid
3. Test locally to isolate issues
4. See `DEPLOYMENT_GUIDE.md` for detailed instructions

---

**🎉 Your AI Assistant will be live in minutes!** 