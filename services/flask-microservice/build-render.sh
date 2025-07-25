#!/bin/bash

echo "🚀 Installing dependencies for Render deployment..."

# Install basic requirements first
pip install --no-cache-dir Flask==3.0.0
pip install --no-cache-dir flask-cors==4.0.0
pip install --no-cache-dir textblob==0.17.1
pip install --no-cache-dir openai==1.97.1
pip install --no-cache-dir python-dotenv==1.0.0
pip install --no-cache-dir gunicorn==21.2.0

# Try multiple ways to install VADER
echo "📦 Installing VADER sentiment..."

# Method 1: Standard installation
pip install --no-cache-dir vaderSentiment==3.3.2 || \
# Method 2: Latest version
pip install --no-cache-dir vaderSentiment || \
# Method 3: Alternative source
pip install --no-cache-dir https://github.com/cjhutto/vaderSentiment/archive/master.zip || \
echo "⚠️ VADER installation failed, will use TextBlob fallback"

echo "✅ Installation complete!"

# Verify VADER installation
python -c "
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    print('✅ VADER installed successfully')
except ImportError:
    print('⚠️ VADER not available, will use TextBlob')
"
