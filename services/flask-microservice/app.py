from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from model import analyze_sentiment, moodify_text, EmotionAnalyzer, LightweightEmotionAnalyzer

app = Flask(__name__)
# CORS(app, origins=[
#     ""
#     "https://moodify-dev.netlify.app/",
#     "http://localhost:3000",  # For local development
#     "http://localhost:5173"   # For Vite dev server
# ])

# Initialize analyzers with fallback logic
try:
    analyzer = EmotionAnalyzer()
    heavy_model_available = True
    print("✅ Heavy BERT model loaded successfully")
except Exception as e:
    heavy_model_available = False
    print(f"⚠️  Heavy model failed to load: {e}")

try:
    lightweight_analyzer = LightweightEmotionAnalyzer()
    lightweight_model_available = True
    print("✅ Lightweight VADER model loaded successfully")
except Exception as e:
    lightweight_model_available = False
    print(f"⚠️  Lightweight model failed to load: {e}")

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
    
    # Try heavy model first, fallback to lightweight
    if heavy_model_available:
        try:
            result = analyzer.analyze_emotion(text)
            result['analysis_type'] = 'heavy_bert'
            return jsonify(result)
        except Exception as e:
            print(f"Heavy model failed, falling back to lightweight: {e}")
    
    # Fallback to lightweight model
    if lightweight_model_available:
        try:
            result = lightweight_analyzer.analyze_emotion(text)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": f"Both models failed: {str(e)}"}), 500
    
    return jsonify({"error": "No emotion analysis models available"}), 503


@app.route('/analyze-light', methods=['POST'])
def analyze_light():
    """
    Lightweight emotion analysis endpoint using VADER sentiment
    Uses significantly less memory than BERT models - ideal for Render free tier
    """
    data = request.json
    if 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    text = data['text']
    
    if not lightweight_model_available:
        return jsonify({"error": "Lightweight model not available. Please install vaderSentiment."}), 503
    
    try:
        result = lightweight_analyzer.analyze_emotion(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Lightweight analysis failed: {str(e)}"}), 500


@app.route("/", methods=["GET"])
def health():
    # Check which models are available
    model_status = []
    if heavy_model_available:
        model_status.append("🤖 BERT model (high accuracy, high memory)")
    if lightweight_model_available:
        model_status.append("⚡ VADER model (fast, low memory)")
    
    status_message = "✅ Server is running!"
    if not heavy_model_available and not lightweight_model_available:
        status_message = "⚠️  Server running but no emotion models available"
    elif not heavy_model_available:
        status_message = "✅ Server running with lightweight model only"
    
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
                "description": "⚡ Lightweight emotion analysis using VADER (low memory, fast)",
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