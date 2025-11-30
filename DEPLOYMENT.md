# Streamlit Cloud Deployment Guide

## Quick Deploy to Streamlit Cloud

### Repository Information:
- **Repository**: `Sri-Charan-3-1-6/my-poetry-ai`
- **Branch**: `main`
- **Main file**: `app.py`

### Deployment Steps:

1. **Visit Streamlit Cloud**: https://share.streamlit.io/
2. **Click "New app"**
3. **Fill in the details**:
   ```
   Repository: Sri-Charan-3-1-6/my-poetry-ai
   Branch: main
   Main file path: app.py
   App URL (optional): my-poetry-ai
   ```
4. **Click "Deploy!"**

### Features Available:
- ✅ Multi-language poetry generation
- ✅ Text-to-speech with musical backgrounds
- ✅ Translation to 50+ languages including Indian languages
- ✅ AI-powered poetry enhancement
- ✅ Audio export functionality
- ✅ Advanced poetry algorithms

### Optional Configuration:
The app includes graceful fallbacks for all dependencies, so it will work even if some packages fail to install on Streamlit Cloud.

### App URL:
Once deployed, your app will be available at:
`https://[your-app-name].streamlit.app/`

### Support:
- All dependencies are listed in `requirements.txt`
- The app has built-in error handling for missing packages
- Audio features require internet connection for optimal performance