from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
import platform
import sys


@api_view(['GET'])
@permission_classes([AllowAny])
def status_view(request):
    """Return the status of the API gateway"""
    return Response({
        'status': 'running',
        'service': 'Moodify API Gateway',
        'version': '1.0.0',
        'message': 'Welcome to the Moodify API Gateway! 🎭',
        'python_version': sys.version,
        'platform': platform.platform(),
        'debug': settings.DEBUG,
        'endpoints': {
            'health': '/api/health/',
            'sentiment': '/api/sentiment/ or /api/predict/',
            'emotion_analysis': '/api/emotion/ or /api/analyze/',
            'light_emotion': '/api/emotion-light/ or /api/analyze-light/',
            'moodify': '/api/moodify/',
            'flask_health': '/api/flask-health/',
            'api_info': '/api/core/info/',
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def info_view(request):
    """Return information about the API gateway and available services"""
    return Response({
        'name': 'Moodify API Gateway',
        'description': 'Central API gateway for the Moodify application - Sentiment and Emotion Analysis',
        'version': '1.0.0',
        'authentication': {
            'required': False,
            'note': 'Authentication is optional. Create an account to save analysis history (future feature).',
            'endpoints': {
                'register': '/api/auth/users/',
                'login': '/api/auth/jwt/create/',
                'refresh': '/api/auth/jwt/refresh/',
            }
        },
        'endpoints': {
            'sentiment_analysis': {
                'url': '/api/sentiment/ or /api/predict/',
                'method': 'POST',
                'description': 'Analyze text sentiment using TextBlob',
                'body': '{"text": "your text here"}',
                'example': {
                    'request': '{"text": "I am so happy today!"}',
                    'response': '{"sentiment": "positive", "confidence": 0.8, "polarity": 0.6}'
                }
            },
            'emotion_analysis': {
                'url': '/api/emotion/ or /api/analyze/',
                'method': 'POST', 
                'description': 'Advanced emotion analysis using BERT (28 emotions) with VADER fallback',
                'body': '{"text": "your text here"}',
                'example': {
                    'request': '{"text": "I am feeling anxious about tomorrow"}',
                    'response': '{"emotions": {"anxiety": 0.75, "fear": 0.25}, "dominant_emotion": "anxiety"}'
                }
            },
            'light_emotion_analysis': {
                'url': '/api/emotion-light/ or /api/analyze-light/',
                'method': 'POST',
                'description': 'Fast, lightweight emotion analysis using VADER sentiment',
                'body': '{"text": "your text here"}',
                'note': 'Optimized for low memory usage, ideal for high-volume requests'
            },
            'text_transformation': {
                'url': '/api/moodify/',
                'method': 'POST',
                'description': 'Transform text to target sentiment',
                'body': '{"text": "your text", "target_sentiment": "positive|negative|neutral"}',
                'example': {
                    'request': '{"text": "This is terrible", "target_sentiment": "positive"}',
                    'response': '{"original_text": "This is terrible", "transformed_text": "This is wonderful", "target_sentiment": "positive"}'
                }
            },
            'health_checks': {
                'api_gateway': '/api/health/',
                'flask_service': '/api/flask-health/',
                'system_status': '/api/core/status/'
            }
        },
        'services': {
            'flask_microservice': {
                'url': settings.FLASK_SERVICE_URL,
                'description': 'Sentiment and emotion analysis service',
                'status': 'proxied through API gateway'
            }
        },
        'usage_notes': [
            'All endpoints are accessible without authentication',
            'POST requests should include Content-Type: application/json',
            'Responses are in JSON format',
            'Rate limiting may apply in production',
            'Create an account to access future features like analysis history'
        ]
    })
