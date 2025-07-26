# Moodify API Gateway - Quick Reference 🚀

## Start Services
```bash
# Terminal 1: Django API Gateway
cd services/main-server
source venv/bin/activate
python manage.py runserver 8000

# Terminal 2: Flask Microservice
cd services/flask-microservice
python start_lightweight.py
```

## Key Endpoints (No Auth Required! 🎉)

| Endpoint | Method | Purpose | Example |
|----------|--------|---------|---------|
| `/` | GET | API overview | `curl localhost:8000/` |
| `/api/health/` | GET | Health check | `curl localhost:8000/api/health/` |
| `/api/sentiment/` | POST | Basic sentiment | `curl -X POST localhost:8000/api/sentiment/ -H "Content-Type: application/json" -d '{"text":"I love this!"}'` |
| `/api/emotion/` | POST | Advanced emotions | `curl -X POST localhost:8000/api/emotion/ -H "Content-Type: application/json" -d '{"text":"I am excited!"}'` |
| `/api/emotion-light/` | POST | Fast emotions | `curl -X POST localhost:8000/api/emotion-light/ -H "Content-Type: application/json" -d '{"text":"Great job!"}'` |
| `/api/moodify/` | POST | Transform text | `curl -X POST localhost:8000/api/moodify/ -H "Content-Type: application/json" -d '{"text":"This is bad","target_sentiment":"positive"}'` |

## Quick Tests 🧪

```bash
# Test 1: Basic connectivity
curl localhost:8000/api/health/

# Test 2: Sentiment analysis  
curl -X POST localhost:8000/api/sentiment/ \
  -H "Content-Type: application/json" \
  -d '{"text": "I absolutely love this new feature!"}'

# Test 3: Emotion analysis
curl -X POST localhost:8000/api/emotion/ \
  -H "Content-Type: application/json" \
  -d '{"text": "I am feeling anxious but excited about tomorrow"}'

# Test 4: Text transformation
curl -X POST localhost:8000/api/moodify/ \
  -H "Content-Type: application/json" \
  -d '{"text": "This weather is terrible", "target_sentiment": "positive"}'
```

## Frontend Integration 🌐

```javascript
// React/JavaScript example
const analyzeText = async (text) => {
  const response = await fetch('http://localhost:8000/api/sentiment/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return await response.json();
};

// Usage
analyzeText("This API is amazing!").then(result => {
  console.log(result); // { sentiment: "positive", confidence: 0.9, ... }
});
```

## Python Client 🐍

```python
import requests

# Sentiment analysis
response = requests.post(
    'http://localhost:8000/api/sentiment/',
    json={'text': 'This is fantastic!'}
)
print(response.json())

# Emotion analysis
response = requests.post(
    'http://localhost:8000/api/emotion-light/',
    json={'text': 'I am thrilled about this project!'}
)
print(response.json())
```

## Troubleshooting 🔧

| Issue | Solution |
|-------|----------|
| Connection refused | Start Flask service on port 5000 |
| Import errors | Activate venv: `source venv/bin/activate` |
| CORS errors | Check `CORS_ALLOWED_ORIGINS` in `.env` |
| 503 errors | Verify Flask service: `curl localhost:5000/` |

## Documentation 📚

- **Full README**: `/services/main-server/README.md`
- **Interactive docs**: `GET localhost:8000/api/core/docs/`
- **API info**: `GET localhost:8000/api/core/info/`

---
**🎭 Ready to analyze! All endpoints are public - no authentication needed!**
