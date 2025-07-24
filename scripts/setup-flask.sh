#!/bin/bash

# Flask Microservice Development Setup
echo "🌶️  Setting up Flask Microservice..."

# Navigate to flask service directory
cd "$(dirname "$0")/../services/flask-microservice"

# Activate virtual environment
echo "📦 Activating Flask virtual environment..."
source venv/bin/activate

# Install dependencies
echo "⬇️  Installing Flask dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Export environment variables
if [ -f .env ]; then
    echo "🔧 Loading environment variables..."
    export $(cat .env | xargs)
fi

echo "✅ Flask microservice setup complete!"
echo "🚀 To run: python app.py"
echo "🔗 URL: http://localhost:5000"

# Keep shell active with venv
exec $SHELL
