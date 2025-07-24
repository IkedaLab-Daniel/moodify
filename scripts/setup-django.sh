#!/bin/bash

# Django Main Server Development Setup
echo "🐍 Setting up Django Main Server..."

# Navigate to django service directory
cd "$(dirname "$0")/../services/main-server"

# Activate virtual environment
echo "📦 Activating Django virtual environment..."
source venv/bin/activate

# Install dependencies
echo "⬇️  Installing Django dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Export environment variables
if [ -f .env ]; then
    echo "🔧 Loading environment variables..."
    export $(cat .env | xargs)
fi

# Django setup commands
echo "🔧 Running Django setup..."
python manage.py makemigrations
python manage.py migrate

echo "✅ Django main server setup complete!"
echo "🚀 To run: python manage.py runserver"
echo "🔗 URL: http://localhost:8000"

# Keep shell active with venv
exec $SHELL
