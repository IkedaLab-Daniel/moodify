from textblob import TextBlob
import math
import re
import os
from openai import OpenAI
from dotenv import load_dotenv

# Try to import heavy models, but fallback gracefully
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    from torch.nn.functional import softmax
    HEAVY_MODELS_AVAILABLE = True
except ImportError:
    HEAVY_MODELS_AVAILABLE = False
    print("Warning: Heavy models not available, using lightweight alternatives")

# Import lightweight alternatives
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    print("Warning: VADER sentiment not available")

# Load environment variables
load_dotenv()

# Initialize OpenRouter client with error handling
def get_openai_client():
    try:
        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
    except Exception as e:
        print(f"Warning: Could not initialize OpenAI client: {e}")
        return None

client = get_openai_client()

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine sentiment category
    if polarity > 0.2:
        sentiment = "positive"
    elif polarity < -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    # Calculate confidence based on absolute polarity
    # Higher absolute polarity = higher confidence
    confidence = min(abs(polarity) * 2, 1.0)
    
    # Create detailed scores
    # Normalize polarity (-1 to 1) to positive scores (0 to 1)
    positive_score = max(0, polarity)
    negative_score = max(0, -polarity)
    neutral_score = 1 - abs(polarity)
    
    # Normalize scores so they sum to 1
    total = positive_score + negative_score + neutral_score
    if total > 0:
        positive_score /= total
        negative_score /= total
        neutral_score /= total
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "scores": {
            "positive": positive_score,
            "negative": negative_score,
            "neutral": neutral_score
        }
    }

def moodify_text(text, target_sentiment):
    """Transform text to match the target sentiment using LLM"""
    
    # Get original sentiment
    original_sentiment = analyze_sentiment(text)['sentiment']
    
    # If already the target sentiment, return original with note
    if original_sentiment == target_sentiment:
        return {
            "original_text": text,
            "modified_text": text,
            "target_sentiment": target_sentiment,
            "original_sentiment": original_sentiment,
            "new_sentiment": original_sentiment,
            "changes_made": [],
            "success": True,
            "message": f"Text is already {target_sentiment}! No changes needed."
        }
    
    # Check if OpenAI client is available
    if client is None:
        return fallback_word_replacement(text, target_sentiment, original_sentiment, "OpenAI client not available")
    
    # Create prompt for LLM
    prompt = f"""
Transform the following text to have a {target_sentiment} sentiment while preserving the core meaning and context. 
Keep the transformation natural and realistic.

Original text: "{text}"
Target sentiment: {target_sentiment}

Requirements:
1. Keep the same general topic and context
2. Make it sound natural and authentic
3. Don't change the fundamental message, just the emotional tone
4. Keep similar length and structure

Transformed text:"""

    try:
        # Call OpenRouter API with DeepSeek model
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert at transforming text sentiment while preserving meaning. Always respond with just the transformed text, no explanations or quotes."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        # ! Debug: Print the full response for inspection
        # print("=== OpenRouter API Response ===")
        # print(f"Full response object: {response}\n")
        # print(f"Response type: {type(response)}\n")
        # print(f"Response choices: {response.choices}\n")
        # print(f"Message content: {response.choices[0].message.content}\n")
        # print(f"Usage info: {getattr(response, 'usage', 'No usage info')}")
        # print("===============================")
        
        modified_text = response.choices[0].message.content.strip()
        
        # Remove quotes if the model added them
        if modified_text.startswith('"') and modified_text.endswith('"'):
            modified_text = modified_text[1:-1]
        
        # Analyze the new sentiment
        new_sentiment_analysis = analyze_sentiment(modified_text)
        new_sentiment = new_sentiment_analysis['sentiment']
        
        # Determine success and changes
        success = new_sentiment == target_sentiment
        
        # Create a summary of changes (simplified since we can't track word-by-word changes with LLM)
        changes_made = [
            f"Transformed from {original_sentiment} to {new_sentiment} sentiment",
            "Used AI language model for natural text transformation"
        ]
        
        if success:
            message = f"Successfully transformed text to {target_sentiment}!"
        else:
            message = f"Transformed text from {original_sentiment} to {new_sentiment} (target was {target_sentiment})"
        
        return {
            "original_text": text,
            "modified_text": modified_text,
            "target_sentiment": target_sentiment,
            "original_sentiment": original_sentiment,
            "new_sentiment": new_sentiment,
            "changes_made": changes_made,
            "success": success,
            "message": message
        }
        
    except Exception as e:
        # Fallback to simple word replacement if API fails
        return fallback_word_replacement(text, target_sentiment, original_sentiment, str(e))

def fallback_word_replacement(text, target_sentiment, original_sentiment, error_message):
    """Fallback method using simple word replacement if LLM fails"""
    
    # Simple word mappings as fallback
    positive_words = {
        'bad': 'good', 'terrible': 'wonderful', 'awful': 'amazing', 
        'hate': 'love', 'dislike': 'like', 'horrible': 'fantastic',
        'disappointed': 'pleased', 'frustrated': 'satisfied', 
        'angry': 'happy', 'sad': 'joyful', 'upset': 'delighted',
        'worst': 'best', 'failed': 'succeeded', 'problem': 'opportunity'
    }
    
    negative_words = {
        'good': 'bad', 'wonderful': 'terrible', 'amazing': 'awful',
        'love': 'hate', 'like': 'dislike', 'fantastic': 'horrible',
        'pleased': 'disappointed', 'satisfied': 'frustrated',
        'happy': 'angry', 'joyful': 'sad', 'delighted': 'upset',
        'best': 'worst', 'succeeded': 'failed', 'opportunity': 'problem'
    }
    
    neutral_words = {
        'love': 'like', 'hate': 'dislike', 'amazing': 'okay',
        'terrible': 'mediocre', 'wonderful': 'decent', 'awful': 'poor',
        'fantastic': 'fine', 'horrible': 'average'
    }
    
    # Select word map based on target sentiment
    if target_sentiment == "positive":
        word_map = positive_words
    elif target_sentiment == "negative":
        word_map = negative_words
    else:
        word_map = neutral_words
    
    # Apply simple replacements
    modified_text = text
    changes_made = [f"Fallback method used (API error: {error_message})"]
    
    words = text.split()
    new_words = []
    
    for word in words:
        clean_word = re.sub(r'[^\w]', '', word.lower())
        if clean_word in word_map:
            replacement = word_map[clean_word]
            if word[0].isupper():
                replacement = replacement.capitalize()
            
            punctuation = re.findall(r'[^\w]', word)
            if punctuation:
                replacement += ''.join(punctuation)
            
            new_words.append(replacement)
            changes_made.append(f"'{word}' → '{replacement}'")
        else:
            new_words.append(word)
    
    modified_text = ' '.join(new_words)
    
    # Analyze new sentiment
    new_sentiment = analyze_sentiment(modified_text)['sentiment']
    success = new_sentiment == target_sentiment
    
    return {
        "original_text": text,
        "modified_text": modified_text,
        "target_sentiment": target_sentiment,
        "original_sentiment": original_sentiment,
        "new_sentiment": new_sentiment,
        "changes_made": changes_made,
        "success": success,
        "message": f"Used fallback method. Result: {new_sentiment} sentiment"
    }

class EmotionAnalyzer:
    def __init__(self):
        if not HEAVY_MODELS_AVAILABLE:
            raise ImportError("Heavy models (transformers, torch) not available. Use LightweightEmotionAnalyzer instead.")
        
        model_name = "bhadresh-savani/bert-base-go-emotion"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.labels = self.model.config.id2label

    def analyze_emotion(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        probs = softmax(outputs.logits, dim=1)[0]

        emotion_scores = {
            self.labels[i]: round(float(probs[i]), 4)
            for i in range(len(probs))
            if float(probs[i]) > 0.01
        }

        # Identify dominant emotion
        dominant_idx = torch.argmax(probs).item()
        dominant_emotion = self.labels[dominant_idx]
        confidence = round(float(probs[dominant_idx]), 4)

        return {
            "emotions": emotion_scores,
            "dominant_emotion": dominant_emotion,
            "confidence": confidence
        }


class LightweightEmotionAnalyzer:
    """
    A lightweight emotion analyzer that uses VADER sentiment analysis
    and maps it to common emotion categories. Uses much less memory than BERT models.
    """
    
    def __init__(self):
        if not VADER_AVAILABLE:
            raise ImportError("VADER sentiment not available. Install with: pip install vaderSentiment")
        
        self.analyzer = SentimentIntensityAnalyzer()
        
        # Map VADER scores to emotion categories
        self.emotion_mapping = {
            'positive_high': ['joy', 'excitement', 'love', 'pride', 'optimism'],
            'positive_medium': ['approval', 'admiration', 'amusement', 'gratitude'],
            'positive_low': ['caring', 'relief', 'curiosity'],
            'neutral': ['neutral', 'realization', 'confusion'],
            'negative_low': ['disappointment', 'embarrassment', 'nervousness'],
            'negative_medium': ['disapproval', 'annoyance', 'fear', 'sadness'],
            'negative_high': ['anger', 'disgust', 'grief', 'remorse']
        }
    
    def analyze_emotion(self, text):
        """
        Analyze emotion using VADER sentiment and map to emotion categories
        Returns format similar to BERT model for compatibility
        """
        scores = self.analyzer.polarity_scores(text)
        
        compound = scores['compound']
        pos = scores['pos']
        neg = scores['neg']
        neu = scores['neu']
        
        # Determine emotion category based on compound score and intensity
        if compound >= 0.5:
            category = 'positive_high'
            primary_emotions = self.emotion_mapping['positive_high']
        elif compound >= 0.1:
            category = 'positive_medium'
            primary_emotions = self.emotion_mapping['positive_medium']
        elif compound >= -0.1:
            if pos > neg:
                category = 'positive_low'
                primary_emotions = self.emotion_mapping['positive_low']
            else:
                category = 'neutral'
                primary_emotions = self.emotion_mapping['neutral']
        elif compound >= -0.5:
            category = 'negative_medium'
            primary_emotions = self.emotion_mapping['negative_medium']
        else:
            category = 'negative_high'
            primary_emotions = self.emotion_mapping['negative_high']
        
        # Create emotion scores similar to BERT output
        emotion_scores = {}
        
        # Add primary emotions from the determined category
        for emotion in primary_emotions:
            if category.startswith('positive'):
                emotion_scores[emotion] = round(pos * (0.8 + 0.2 * abs(compound)), 4)
            elif category.startswith('negative'):
                emotion_scores[emotion] = round(neg * (0.8 + 0.2 * abs(compound)), 4)
            else:
                emotion_scores[emotion] = round(neu * 0.8, 4)
        
        # Add neutral if significant
        if neu > 0.3:
            emotion_scores['neutral'] = round(neu, 4)
        
        # Filter out very low scores
        emotion_scores = {k: v for k, v in emotion_scores.items() if v > 0.05}
        
        # Determine dominant emotion
        if emotion_scores:
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = emotion_scores[dominant_emotion]
        else:
            dominant_emotion = 'neutral'
            confidence = 0.5
        
        return {
            "emotions": emotion_scores,
            "dominant_emotion": dominant_emotion,
            "confidence": confidence,
            "vader_scores": {
                "compound": compound,
                "positive": pos,
                "negative": neg,
                "neutral": neu
            },
            "analysis_type": "lightweight_vader"
        }
