# 🚀 Render Free Tier Deployment (Lightweight Mode)

This guide helps you deploy the Flask microservice on Render's free tier (512Mi memory limit) without memory issues.

## 🎯 Quick Deployment Steps

### 1. Environment Variables in Render Dashboard
Set these in your Render service environment variables:
```
DISABLE_HEAVY_MODELS=true
LIGHTWEIGHT_ONLY=true
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 2. Build Command
```bash
pip install -r requirements-light.txt
```

### 3. Start Command
```bash
gunicorn app:app
```

## 📊 Memory Usage Comparison

| Mode | Memory Usage | Models Available | Render Compatible |
|------|-------------|------------------|-------------------|
| **Full** | 500MB+ | BERT + VADER | ❌ Exceeds 512Mi limit |
| **Lightweight** | ~5MB | VADER only | ✅ Perfect for free tier |

## 🔧 How It Works

The app automatically detects the environment variables and:

1. **DISABLE_HEAVY_MODELS=true**: Skips loading BERT models entirely
2. **LIGHTWEIGHT_ONLY=true**: Forces lightweight mode
3. **No heavy imports**: Prevents torch/transformers from being imported

## 📡 Available Endpoints (Lightweight Mode)

### ✅ Working Endpoints:
- `GET /` - Health check & documentation
- `POST /predict` - Sentiment analysis (TextBlob)
- `POST /analyze-light` - Lightweight emotion analysis (VADER)
- `POST /moodify` - Text transformation (OpenRouter AI)

### ⚠️ Limited Endpoints:
- `POST /analyze` - Automatically falls back to VADER when BERT unavailable

## 🧪 Testing Deployment Locally

```bash
# Set environment variables
export DISABLE_HEAVY_MODELS=true
export LIGHTWEIGHT_ONLY=true

# Install lightweight dependencies
pip install -r requirements-light.txt

# Run the app
python app.py
```

## 🔍 Verification

After deployment, check your service logs for:
```
🚀 Heavy models disabled via environment variable
✅ Lightweight VADER model loaded successfully
```

## 📈 Performance

- **Startup time**: ~2-3 seconds (vs 30+ seconds with BERT)
- **Memory usage**: ~5MB (vs 500MB+ with BERT)
- **Response time**: ~50ms (vs 200ms+ with BERT)
- **Accuracy**: Good for most use cases (VADER is well-tested)

## 🆘 Troubleshooting

### Memory Issues
- Ensure `DISABLE_HEAVY_MODELS=true` is set
- Use `requirements-light.txt` not `requirements.txt`
- Check Render logs for import errors

### Missing Dependencies
- Verify `vaderSentiment` is in requirements-light.txt
- Check for typos in environment variable names

### API Errors
- Use `/analyze-light` instead of `/analyze` for guaranteed lightweight analysis
- Check OpenRouter API key for `/moodify` endpoint
