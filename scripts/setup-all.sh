#!/bin/bash

# Complete project setup for new developers
echo "🚀 Setting up complete Moodify project..."

# Make sure we're in the right directory
cd "$(dirname "$0")/.."

echo "📁 Current directory: $(pwd)"

# Setup Python services
echo ""
echo "🐍 Setting up Python services..."
./scripts/setup-django.sh &
DJANGO_PID=$!

./scripts/setup-flask.sh &
FLASK_PID=$!

# Setup Node.js service
echo ""
echo "📦 Setting up Express microservice..."
cd services/express-microservice
npm install
cd ../..

# Setup React client
echo ""
echo "⚛️  Setting up React client..."
cd client
npm install
cd ..

# Wait for Python setups to complete
wait $DJANGO_PID
wait $FLASK_PID

echo ""
echo "✅ Complete project setup finished!"
echo ""
echo "🚀 To start all services:"
echo "   ./scripts/start-dev.sh"
echo ""
echo "📖 Individual service commands:"
echo "   Django:  cd services/main-server && source venv/bin/activate && python manage.py runserver"
echo "   Flask:   cd services/flask-microservice && source venv/bin/activate && python app.py"
echo "   Express: cd services/express-microservice && npm run dev"
echo "   React:   cd client && npm run dev"
