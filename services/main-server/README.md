# Moodify API Gateway 🎭

A Django-based API gateway that provides centralized access to sentiment and emotion analysis services. This gateway connects to Flask microservices to deliver powerful text analysis capabilities.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 4.2+
- Flask microservice running on port 5000

### Setup

1. **Navigate to the main-server directory:**
   ```bash
   cd services/main-server
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the Django server:**
   ```bash
   python manage.py runserver 8000
   ```

6. **Start the Flask microservice (in another terminal):**
   ```bash
   cd ../flask-microservice
   python start_lightweight.py
   ```

### Verify Setup
Visit `http://localhost:8000` to see the API status and available endpoints.

## 📡 API Endpoints

### 🏥 Health & Status

#### `GET /` - Root Status
Returns basic API gateway information and available endpoints.

**Response:**
```json
{
  "status": "running",
  "service": "Moodify API Gateway",
  "version": "1.0.0",
  "message": "Welcome to the Moodify API Gateway! 🎭",
  "endpoints": {
    "health": "/api/health/",
    "sentiment": "/api/sentiment/ or /api/predict/",
    "emotion_analysis": "/api/emotion/ or /api/analyze/",
    "light_emotion": "/api/emotion-light/ or /api/analyze-light/",
    "moodify": "/api/moodify/",
    "flask_health": "/api/flask-health/"
  }
}
```

#### `GET /api/health/` - API Gateway Health
Quick health check for the API gateway.

**Response:**
```json
{
  "status": "healthy",
  "service": "moodify-api-gateway",
  "version": "1.0.0",
  "flask_service": "http://localhost:5000"
}
```

#### `GET /api/flask-health/` - Flask Service Health
Proxies to Flask microservice health endpoint to check service availability.

#### `GET /api/core/info/` - Detailed API Information
Comprehensive API documentation with examples and usage notes.

### 🎭 Sentiment & Emotion Analysis

> **Note:** All analysis endpoints are **publicly accessible** - no authentication required!

#### `POST /api/sentiment/` or `POST /api/predict/` - Basic Sentiment Analysis
Analyze text sentiment using TextBlob (fast, lightweight).

**Request:**
```json
{
  "text": "I am so happy today!"
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.8,
  "polarity": 0.6,
  "subjectivity": 0.9
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/sentiment/ \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this new feature!"}'
```

#### `POST /api/emotion/` or `POST /api/analyze/` - Advanced Emotion Analysis
Deep emotion analysis using BERT models with VADER fallback (28+ emotions).

**Request:**
```json
{
  "text": "I am feeling anxious about tomorrow's presentation"
}
```

**Response:**
```json
{
  "emotions": {
    "anxiety": 0.75,
    "fear": 0.25,
    "nervousness": 0.60
  },
  "dominant_emotion": "anxiety",
  "confidence": 0.75,
  "analysis_type": "heavy_bert"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/emotion/ \
  -H "Content-Type: application/json" \
  -d '{"text": "I am feeling overwhelmed but excited about this opportunity"}'
```

#### `POST /api/emotion-light/` or `POST /api/analyze-light/` - Lightweight Emotion Analysis
Fast emotion analysis using VADER sentiment (optimized for speed and low memory).

**Request:**
```json
{
  "text": "This is absolutely wonderful news!"
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "compound": 0.8,
  "emotions": {
    "joy": 0.8,
    "excitement": 0.6
  },
  "analysis_type": "vader_light"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/emotion-light/ \
  -H "Content-Type: application/json" \
  -d '{"text": "What a fantastic day!"}'
```

#### `POST /api/moodify/` - Text Transformation
Transform text to match a target sentiment (positive, negative, or neutral).

**Request:**
```json
{
  "text": "This weather is terrible",
  "target_sentiment": "positive"
}
```

**Response:**
```json
{
  "original_text": "This weather is terrible",
  "transformed_text": "This weather is beautiful",
  "target_sentiment": "positive",
  "success": true
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/moodify/ \
  -H "Content-Type: application/json" \
  -d '{"text": "I hate Mondays", "target_sentiment": "positive"}'
```

### 🔐 Authentication (Optional)

While authentication is **not required** for basic usage, you can create an account to access future features like analysis history.

#### `POST /api/auth/users/` - Register
Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword",
  "re_password": "securepassword"
}
```

#### `POST /api/auth/jwt/create/` - Login
Obtain JWT tokens for authenticated requests.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### `POST /api/auth/jwt/refresh/` - Refresh Token
Refresh an expired access token.

## 🛠️ Architecture

### Components
- **Django API Gateway** (Port 8000): Central routing and authentication
- **Flask Microservice** (Port 5000): Sentiment and emotion analysis
- **SQLite Database**: User management and future history storage

### Flow
1. Client sends request to Django API Gateway
2. Gateway validates request (optional authentication)
3. Gateway proxies request to appropriate Flask microservice
4. Flask processes the analysis
5. Gateway returns response to client

## 🧪 Testing

### Test Basic Connectivity
```bash
# Test API Gateway
curl http://localhost:8000/api/health/

# Test Flask Service (through gateway)
curl http://localhost:8000/api/flask-health/

# Test sentiment analysis
curl -X POST http://localhost:8000/api/sentiment/ \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test message"}'
```

### Frontend Integration
```javascript
// Example JavaScript usage
const analyzeText = async (text) => {
  const response = await fetch('http://localhost:8000/api/sentiment/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text: text })
  });
  
  const result = await response.json();
  console.log(result);
};

analyzeText("I love this API!");
```

### Python Client Example
```python
import requests

# Sentiment analysis
response = requests.post(
    'http://localhost:8000/api/sentiment/',
    json={'text': 'This API is amazing!'}
)
print(response.json())

# Emotion analysis
response = requests.post(
    'http://localhost:8000/api/emotion/',
    json={'text': 'I am so excited about this project!'}
)
print(response.json())
```

## 🚦 Status Codes

- `200` - Success
- `400` - Bad Request (missing or invalid data)
- `503` - Service Unavailable (Flask microservice down)
- `504` - Gateway Timeout (Flask microservice timeout)
- `500` - Internal Server Error

## 🔧 Configuration

### Environment Variables (.env)
```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Service URLs
FLASK_SERVICE_URL=http://localhost:5000
EXPRESS_SERVICE_URL=http://localhost:3001

# CORS settings
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

## 🐛 Troubleshooting

### Common Issues

1. **Flask service connection failed**
   - Ensure Flask microservice is running on port 5000
   - Check `FLASK_SERVICE_URL` in `.env` file
   - Verify Flask service health: `curl http://localhost:5000/`

2. **Import errors in Django**
   - Activate virtual environment: `source venv/bin/activate`
   - Install requirements: `pip install -r requirements.txt`

3. **Database errors**
   - Run migrations: `python manage.py migrate`
   - Check database permissions

4. **CORS errors from frontend**
   - Update `CORS_ALLOWED_ORIGINS` in `.env`
   - Restart Django server after changes

### Logs
- Django logs: Check terminal output when running `python manage.py runserver`
- Flask logs: Check Flask microservice terminal output

## 🚀 Production Deployment

### Security Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up HTTPS
- [ ] Configure rate limiting
- [ ] Set up proper logging
- [ ] Use production database (PostgreSQL)

### Performance Tips
- Use `/api/emotion-light/` for high-volume requests
- Consider caching frequent requests
- Monitor Flask microservice resource usage
- Scale Flask services horizontally as needed

## 📞 API Support

For questions or issues:
1. Check this README
2. Visit `/api/core/info/` for comprehensive API documentation
3. Test endpoints with the provided cURL examples
4. Check server logs for error details

---

**Happy Analyzing! 🎭✨**
