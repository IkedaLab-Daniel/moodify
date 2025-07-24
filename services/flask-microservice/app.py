from flask import Flask, request, jsonify
from flask_cors import CORS
from model import analyze_sentiment, moodify_text

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "message": "Sentiment service is running"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)