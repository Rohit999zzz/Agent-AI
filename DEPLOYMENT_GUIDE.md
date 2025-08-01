# 🚀 Streamlit Cloud Deployment Guide

This guide will help you deploy your Personal AI Assistant on Streamlit Cloud.

## 📋 Prerequisites

1. **GitHub Account**: You need a GitHub account to host your code
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Google Gemini API Key**: Get your free key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🎯 Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Create a GitHub Repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Personal AI Assistant"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Ensure these files are in your repository**:
   ```
   ├── streamlit_app.py          # Main app file (for deployment)
   ├── enhanced_main.py          # Assistant implementation
   ├── tools/                    # Tools directory
   ├── requirements.txt          # Python dependencies
   ├── .streamlit/config.toml    # Streamlit configuration
   ├── sample_data.csv           # Sample data
   ├── sample_report.txt         # Sample report
   └── README.md                 # Documentation
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)

2. **Sign in with GitHub**: Connect your GitHub account

3. **Deploy New App**:
   - Click "New app"
   - Select your repository
   - Set the path to your app: `streamlit_app.py`
   - Click "Deploy!"

### Step 3: Configure API Keys

1. **In Streamlit Cloud Dashboard**:
   - Go to your deployed app
   - Click "Settings" (⚙️ icon)
   - Scroll to "Secrets"

2. **Add Your API Keys**:
   ```toml
   GOOGLE_API_KEY = "your_gemini_api_key_here"
   SERPAPI_API_KEY = "your_serpapi_key_here"  # Optional
   ```

3. **Save and Redeploy**: Click "Save" and your app will redeploy automatically

## 🔧 Configuration Files

### streamlit_app.py
- Main deployment file
- Includes error handling for missing API keys
- Optimized for Streamlit Cloud

### .streamlit/config.toml
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

### requirements.txt
```
langchain
langchain-google-genai
google-generativeai
serpapi
python-dotenv
pypdf2
pandas
numpy
matplotlib
streamlit
requests
```

## 🚨 Troubleshooting

### Common Issues:

1. **"Module not found" errors**:
   - Ensure all files are in the repository
   - Check that `requirements.txt` includes all dependencies

2. **API Key not found**:
   - Verify the secret name is exactly `GOOGLE_API_KEY`
   - Check that the API key is valid

3. **App not loading**:
   - Check the app path is correct (`streamlit_app.py`)
   - Look at the logs in Streamlit Cloud dashboard

4. **Rate limiting errors**:
   - The app includes fallback models and retry logic
   - Check your Gemini API quota

### Debugging:

1. **Check Logs**: In Streamlit Cloud dashboard, click "Logs" to see error messages

2. **Test Locally First**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Verify API Key**:
   ```bash
   python check_models.py
   ```

## 🌐 Custom Domain (Optional)

1. **In Streamlit Cloud Settings**:
   - Go to your app settings
   - Click "Custom domain"
   - Add your domain

2. **DNS Configuration**:
   - Add CNAME record pointing to your Streamlit app
   - Wait for DNS propagation

## 📊 Monitoring

### Streamlit Cloud Dashboard:
- **App Status**: Check if app is running
- **Usage Statistics**: Monitor app usage
- **Logs**: View error logs and debugging info

### API Usage Monitoring:
- **Google AI Studio**: Monitor Gemini API usage
- **SerpAPI Dashboard**: Monitor web search usage

## 🔒 Security Best Practices

1. **Never commit API keys**:
   - Use Streamlit secrets for sensitive data
   - Keep `.env` files out of repository

2. **Rate Limiting**:
   - The app includes built-in rate limiting
   - Monitor API usage to avoid quota issues

3. **File Upload Security**:
   - Files are stored temporarily
   - Automatic cleanup after session

## 🎉 Success!

Once deployed, your app will be available at:
```
https://YOUR_APP_NAME-YOUR_USERNAME.streamlit.app
```

### Features Available:
- ✅ File upload (CSV, PDF, TXT)
- ✅ Web search capabilities
- ✅ Mathematical calculations
- ✅ Multi-step reasoning
- ✅ Chat interface
- ✅ Quick analysis buttons

## 📞 Support

If you encounter issues:

1. **Check the logs** in Streamlit Cloud dashboard
2. **Verify API keys** are correctly set
3. **Test locally** first to isolate issues
4. **Check GitHub issues** for common problems

---

**Happy Deploying! 🚀** 