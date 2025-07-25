from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from model import analyze_sentiment, moodify_text, LightweightEmotionAnalyzer

# Check if we should disable heavy models (for deployment)
DISABLE_HEAVY_MODELS = os.getenv('DISABLE_HEAVY_MODELS', 'false').lower() == 'true'
LIGHTWEIGHT_ONLY = os.getenv('LIGHTWEIGHT_ONLY', 'false').lower() == 'true'

app = Flask(__name__)
# CORS(app, origins=[
#     ""
#     "https://moodify-dev.netlify.app/",
#     "http://localhost:3000",  # For local development
#     "http://localhost:5173"   # For Vite dev server
# ])

# Initialize analyzers with environment-controlled loading
heavy_model_available = False
analyzer = None

if not DISABLE_HEAVY_MODELS and not LIGHTWEIGHT_ONLY:
    try:
        from model import EmotionAnalyzer
        analyzer = EmotionAnalyzer()
        heavy_model_available = True
        print("✅ Heavy BERT model loaded successfully")
    except Exception as e:
        heavy_model_available = False
        print(f"⚠️  Heavy model failed to load: {e}")
else:
    print("🚀 Heavy models disabled via environment variable (DISABLE_HEAVY_MODELS=true or LIGHTWEIGHT_ONLY=true)")

# Note: We don't need to initialize LightweightEmotionAnalyzer anymore
# The /analyze-light endpoint now uses TextBlob directly (same as /predict)
print("✅ Lightweight analysis will use TextBlob (same as /predict endpoint)")

CORS(app, origins="*")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"]
    try:
        result = analyze_sentiment(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route("/moodify", methods=["POST"])
def moodify():
    data = request.get_json()

    if not data or "text" not in data or "target_sentiment" not in data:
        return jsonify({"error": "Missing 'text' or 'target_sentiment' in request body"}), 400

    text = data["text"]
    target_sentiment = data["target_sentiment"]
    
    try:
        result = moodify_text(text, target_sentiment)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Moodification failed: {str(e)}"}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    if 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    text = data['text']
    
    # Try heavy model first, fallback to TextBlob-based analysis
    if heavy_model_available:
        try:
            result = analyzer.analyze_emotion(text)
            result['analysis_type'] = 'heavy_bert'
            return jsonify(result)
        except Exception as e:
            print(f"Heavy model failed, falling back to TextBlob: {e}")
    
    # Fallback to TextBlob-based emotion analysis (same logic as /analyze-light)
    try:
        # Get basic sentiment analysis (same as /predict endpoint)
        sentiment_result = analyze_sentiment(text)
        
        # Convert sentiment to emotion categories (simplified)
        confidence = sentiment_result['confidence']
        
        if sentiment_result['sentiment'] == 'positive':
            emotions = {"joy": round(confidence * 0.9, 4), "optimism": round(confidence * 0.7, 4)}
            dominant_emotion = "joy"
        elif sentiment_result['sentiment'] == 'negative':
            emotions = {"sadness": round(confidence * 0.9, 4), "disappointment": round(confidence * 0.7, 4)}
            dominant_emotion = "sadness"
        else:
            emotions = {"neutral": round(max(0.5, confidence), 4)}
            dominant_emotion = "neutral"
        
        result = {
            "emotions": emotions,
            "dominant_emotion": dominant_emotion,
            "confidence": round(max(emotions.values()) if emotions else 0.5, 4),
            "textblob_sentiment": sentiment_result,
            "analysis_type": "textblob_fallback"
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


@app.route('/analyze-light', methods=['POST'])
def analyze_light():
    """
    Lightweight emotion analysis endpoint using TextBlob sentiment
    Uses significantly less memory than BERT models - ideal for Render free tier
    """
    data = request.json
    if 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    text = data['text']
    
    # Use TextBlob directly since it's already working for /predict
    try:
        # Get basic sentiment analysis (same as /predict endpoint)
        sentiment_result = analyze_sentiment(text)
        
        # Convert sentiment to emotion categories
        polarity = sentiment_result['scores']['positive'] - sentiment_result['scores']['negative']
        confidence = sentiment_result['confidence']
        
        # Map sentiment to emotion categories
        emotions = {}
        dominant_emotion = "neutral"
        
        if sentiment_result['sentiment'] == 'positive':
            if confidence > 0.7:
                emotions = {
                    "joy": round(confidence * 0.9, 4),
                    "excitement": round(confidence * 0.8, 4),
                    "optimism": round(confidence * 0.7, 4)
                }
                dominant_emotion = "joy"
            else:
                emotions = {
                    "approval": round(confidence * 0.8, 4),
                    "gratitude": round(confidence * 0.6, 4),
                    "caring": round(confidence * 0.5, 4)
                }
                dominant_emotion = "approval"
        elif sentiment_result['sentiment'] == 'negative':
            if confidence > 0.7:
                emotions = {
                    "sadness": round(confidence * 0.9, 4),
                    "disappointment": round(confidence * 0.8, 4),
                    "annoyance": round(confidence * 0.7, 4)
                }
                dominant_emotion = "sadness"
            else:
                emotions = {
                    "disapproval": round(confidence * 0.6, 4),
                    "disappointment": round(confidence * 0.5, 4)
                }
                dominant_emotion = "disapproval"
        else:
            emotions = {
                "neutral": round(max(0.5, confidence), 4),
                "realization": round(confidence * 0.3, 4)
            }
            dominant_emotion = "neutral"
        
        # Build response in same format as BERT/VADER models
        result = {
            "emotions": emotions,
            "dominant_emotion": dominant_emotion,
            "confidence": round(max(emotions.values()) if emotions else 0.5, 4),
            "textblob_sentiment": sentiment_result,
            "analysis_type": "lightweight_textblob"
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Lightweight analysis failed: {str(e)}"}), 500


@app.route("/", methods=["GET"])
def health():
    # Check which models are available
    model_status = []
    if heavy_model_available:
        model_status.append("🤖 BERT model (high accuracy, high memory)")
    model_status.append("⚡ TextBlob model (fast, low memory, always available)")
    
    status_message = "✅ Server is running!"
    if not heavy_model_available:
        status_message = "✅ Server running with TextBlob model only"
    
    # Template data
    template_data = {
        "title": "Ice's Sentiment Analysis Microservice",
        "emoji": "🎭",
        "service_name": "Ice's Sentiment Analysis Microservice",
        "status": status_message,
        "model_status": model_status,
        "endpoints": [
            {
                "method": "GET",
                "path": "/",
                "description": "Health check & service info (this page)",
                "body": None
            },
            {
                "method": "POST",
                "path": "/predict",
                "description": "Analyze text sentiment with confidence scores (TextBlob)",
                "body": '{"text": "your text here"}'
            },
            {
                "method": "POST",
                "path": "/analyze",
                "description": "🤖 Advanced emotion analysis using BERT (28 emotions, fallback to VADER)",
                "body": '{"text": "your text here"}'
            },
            {
                "method": "POST",
                "path": "/analyze-light",
                "description": "⚡ Lightweight emotion analysis using TextBlob (low memory, fast)",
                "body": '{"text": "your text here"}',
                "note": "🚀 Optimized for Render free tier (512Mi memory limit)"
            },
            {
                "method": "POST",
                "path": "/moodify",
                "description": "Transform text to target sentiment",
                "body": '{"text": "your text", "target_sentiment": "positive|negative|neutral"}'
            }
        ],
        "example_curl": """curl -X POST https://moodify-tk9p.onrender.com/analyze-light \\
  -H "Content-Type: application/json" \\
  -d '{"text": "I am so excited about this new opportunity!"}'""",
        "tech_stack": "Flask • TextBlob • BERT • VADER • OpenRouter AI"
    }
    
    return render_template('index.html', **template_data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)