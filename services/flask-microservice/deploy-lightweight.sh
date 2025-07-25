#!/bin/bash

# Render Deployment Script for Lightweight Mode
# This script sets environment variables to disable heavy models

echo "🚀 Setting up Render deployment with lightweight models only"

# Export environment variables for current session
export DISABLE_HEAVY_MODELS=true
export LIGHTWEIGHT_ONLY=true

echo "✅ Environment variables set:"
echo "   DISABLE_HEAVY_MODELS=$DISABLE_HEAVY_MODELS"
echo "   LIGHTWEIGHT_ONLY=$LIGHTWEIGHT_ONLY"

# Install lightweight dependencies only
echo "📦 Installing lightweight dependencies..."
pip install -r requirements-light.txt

echo "🎉 Ready for deployment!"
echo ""
echo "📋 To deploy on Render:"
echo "1. Set these environment variables in Render dashboard:"
echo "   - DISABLE_HEAVY_MODELS: true"
echo "   - LIGHTWEIGHT_ONLY: true"
echo "   - OPENROUTER_API_KEY: your_api_key"
echo ""
echo "2. Use this build command:"
echo "   pip install -r requirements-light.txt"
echo ""
echo "3. Use this start command:"
echo "   gunicorn app:app"
echo ""
echo "🎯 This configuration uses only ~5MB RAM instead of 500MB+"
