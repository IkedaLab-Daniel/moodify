# Django API Gateway

A simple Django REST API gateway that routes requests to microservices.

## Features

- Routes requests to Flask sentiment analysis microservice
- Health check endpoints for all services
- CORS enabled for frontend integration
- Simple proxy functionality with error handling
- Ready for Express microservice integration

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the server:**
   ```bash
   python manage.py runserver 8000
   ```

## API Endpoints

### Health Check
- `GET /` - Gateway health check
- `GET /health/` - Alternative health check
- `GET /status/` - Check all microservices status

### Sentiment Analysis (Flask Microservice Proxy)
- `POST /sentiment/predict/` - Basic sentiment analysis
- `POST /sentiment/analyze/` - Advanced emotion analysis (BERT)
- `POST /sentiment/analyze-light/` - Lightweight emotion analysis (VADER)
- `POST /sentiment/moodify/` - Text mood transformation

### Express Microservice (Placeholder)
- `GET /express/health/` - Express service health check

## Request Examples

### Basic Sentiment Analysis
```bash
curl -X POST http://localhost:8000/sentiment/predict/ \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this new feature!"}'
```

### Advanced Emotion Analysis
```bash
curl -X POST http://localhost:8000/sentiment/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"text": "I am so excited about this opportunity!"}'
```

### Lightweight Analysis
```bash
curl -X POST http://localhost:8000/sentiment/analyze-light/ \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!"}'
```

### Mood Transformation
```bash
curl -X POST http://localhost:8000/sentiment/moodify/ \
  -H "Content-Type: application/json" \
  -d '{"text": "This is terrible", "target_sentiment": "positive"}'
```

## Environment Variables

- `DEBUG` - Enable/disable debug mode
- `SECRET_KEY` - Django secret key
- `FLASK_MICROSERVICE_URL` - URL of Flask sentiment service
- `EXPRESS_MICROSERVICE_URL` - URL of Express service

## Architecture

```
Client (React) 
    ↓
Django API Gateway (Port 8000)
    ↓
Flask Microservice (Port 5000) - Sentiment Analysis
Express Microservice (Port 3001) - [Not yet implemented]
```

## Development

The gateway automatically handles:
- Request validation
- Service discovery and health checks
- Error handling and timeouts
- CORS for frontend integration
- JSON request/response formatting
