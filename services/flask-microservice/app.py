from flask import Flask, request, jsonify
from flask_cors import CORS
from model import analyze_sentiment, moodify_text

app = Flask(__name__)
CORS(app, origins=[
    "https://moodify-dev.netlify.app/",
    "http://localhost:3000",  # For local development
    "http://localhost:5173"   # For Vite dev server
])

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

# formerly /health
@app.route("/", methods=["GET"])
def health():
    return '''
    <html>
        <head>
            <title>Ice's Sentiment Analysis Microservice</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; }
                .wake-up { background: #e8f4fd; padding: 15px; border-left: 4px solid #2196F3; margin: 20px 0; }
                .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 3px solid #28a745; }
                .method { background: #007bff; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px; }
                .url { font-family: monospace; color: #333; font-weight: bold; }
                .description { color: #666; margin-top: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎭 Ice's Sentiment Analysis Microservice</h1>
                <p><strong>Status:</strong> ✅ Server is running!</p>
                
                <div class="wake-up">
                    <strong>💡 Use this endpoint to wake up server</strong><br>
                    Perfect for keeping Render free tier active
                </div>
                
                <h2>📡 API Endpoints</h2>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/</span>
                    <div class="description">Health check & service info (this page)</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/predict</span>
                    <div class="description">
                        Analyze text sentiment<br>
                        <strong>Body:</strong> {"text": "your text here"}
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/moodify</span>
                    <div class="description">
                        Transform text to target sentiment<br>
                        <strong>Body:</strong> {"text": "your text", "target_sentiment": "positive|negative|neutral"}
                    </div>
                </div>
                
                <h3>Example Usage:</h3>
                <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">
curl -X POST https://moodify-tk9p.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this amazing day!"}'
                </pre>
                
                <footer style="margin-top: 30px; text-align: center; color: #666; font-size: 14px;">
                    Powered by Flask • TextBlob • OpenRouter AI
                </footer>
            </div>
        </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)