from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from model import analyze_sentiment, moodify_text

app = Flask(__name__)
# CORS(app, origins=[
#     ""
#     "https://moodify-dev.netlify.app/",
#     "http://localhost:3000",  # For local development
#     "http://localhost:5173"   # For Vite dev server
# ])

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

@app.route("/", methods=["GET"])
def health():
    # Template data
    template_data = {
        "title": "Ice's Sentiment Analysis Microservice",
        "emoji": "🎭",
        "service_name": "Ice's Sentiment Analysis Microservice",
        "status": "✅ Server is running!",
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
                "description": "Analyze text sentiment",
                "body": '{"text": "your text here"}'
            },
            {
                "method": "POST",
                "path": "/moodify",
                "description": "Transform text to target sentiment",
                "body": '{"text": "your text", "target_sentiment": "positive|negative|neutral"}'
            }
        ],
        "example_curl": """curl -X POST https://moodify-tk9p.onrender.com/predict \\
  -H "Content-Type: application/json" \\
  -d '{"text": "I love this amazing day!"}'""",
        "tech_stack": "Flask • TextBlob • OpenRouter AI"
    }
    
    return render_template('index.html', **template_data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)