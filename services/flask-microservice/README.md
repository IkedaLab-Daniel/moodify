# 🎭 Sentiment Analysis Microservice

A Flask-based microservice for sentiment analysis and text mood transformation using TextBlob and OpenRouter AI.

## 🚀 Features

- **Sentiment Analysis**: Analyze text sentiment with confidence scores
- **Advanced Emotion Analysis**: BERT-powered multi-emotion detection with 28 emotion categories
- **Text Moodification**: Transform text to target sentiment (positive/negative/neutral)
- **AI-Powered**: Uses OpenRouter AI with DeepSeek model for natural transformations
- **Fallback System**: TextBlob-based fallback when AI is unavailable
- **Production Ready**: Dockerized with Gunicorn

## 📡 API Endpoints

### `POST /predict`
Analyze sentiment of provided text.

**Request:**
```json
{
  "text": "I love this amazing day!"
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.8,
  "polarity": 0.8,
  "subjectivity": 0.9,
  "scores": {
    "positive": 0.8,
    "negative": 0.0,
    "neutral": 0.2
  }
}
```

### `POST /analyze` ✨ NEW
Advanced emotion analysis using BERT model with 28 emotion categories.

**Request:**
```json
{
  "text": "I'm so excited about this new opportunity!"
}
```

**Response:**
```json
{
  "emotions": {
    "excitement": 0.8234,
    "joy": 0.1234,
    "optimism": 0.0456,
    "gratitude": 0.0076
  },
  "dominant_emotion": "excitement",
  "confidence": 0.8234
}
```

### `POST /moodify`
Transform text to target sentiment.

**Request:**
```json
{
  "text": "This is terrible",
  "target_sentiment": "positive"
}
```

**Response:**
```json
{
  "original_text": "This is terrible",
  "modified_text": "This is wonderful",
  "target_sentiment": "positive",
  "original_sentiment": "negative",
  "new_sentiment": "positive",
  "changes_made": ["Transformed from negative to positive sentiment"],
  "success": true,
  "message": "Successfully transformed text to positive!"
}
```

## 🐳 Docker Usage

### Build & Run
```bash
# Build the image
docker build -t sentiment-microservice .

# Run the container
docker run -p 5000:5000 --env-file .env sentiment-microservice
```

### Docker Compose (Development)
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- OpenRouter API key

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your OPENROUTER_API_KEY

# Run development server
python app.py
```

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | OpenRouter API key for AI transformations | Yes |

## 📊 Tech Stack

- **Flask**: Web framework
- **TextBlob**: Sentiment analysis library
- **BERT**: Advanced emotion analysis with 28 emotion categories
- **Transformers**: Hugging Face transformers library
- **OpenRouter AI**: Advanced text transformation
- **Gunicorn**: WSGI HTTP Server
- **Docker**: Containerization

## 🚦 Health Check

Visit `http://localhost:5000/` for service status and API documentation.

## 📈 Roadmap

- [x] ~~Upgrade to BERT model for improved accuracy~~ ✅ **COMPLETED!**
  - Added `/analyze` endpoint with BERT-based emotion detection
  - 28 emotion categories including joy, anger, fear, surprise, sadness, and more
  - Higher accuracy and granular emotion insights
- [ ] Add batch processing for multiple texts
- [ ] Implement emotion trend analysis over time
- [ ] Add support for multilingual emotion detection