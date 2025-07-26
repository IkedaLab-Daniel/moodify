#!/bin/bash

# Django API Gateway Startup Script

echo "🚀 Starting Django API Gateway..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser if needed (optional)
# echo "👤 Creating superuser..."
# python manage.py createsuperuser --noinput || true

# Start the server
echo "🌟 Starting Django API Gateway on port 8000..."
echo "📱 Gateway will be available at: http://localhost:8000"
echo "📊 Admin panel available at: http://localhost:8000/admin"
echo "🔍 API status at: http://localhost:8000/status"

python manage.py runserver 8000
