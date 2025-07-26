from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Health check endpoint
    path('health/', views.health_check, name='health_check'),
    
    # Flask microservice endpoints - simplified and mapped to actual Flask endpoints
    path('sentiment/', views.SentimentAnalysisView.as_view(), name='sentiment_analysis'),
    path('predict/', views.SentimentAnalysisView.as_view(), name='predict'),  # Direct mapping to Flask
    
    path('emotion/', views.EmotionAnalysisView.as_view(), name='emotion_analysis'),
    path('analyze/', views.EmotionAnalysisView.as_view(), name='analyze'),  # Direct mapping to Flask
    
    path('emotion-light/', views.LightEmotionAnalysisView.as_view(), name='light_emotion_analysis'),
    path('analyze-light/', views.LightEmotionAnalysisView.as_view(), name='analyze_light'),  # Direct mapping to Flask
    
    path('moodify/', views.MoodifyView.as_view(), name='moodify'),  # Direct mapping to Flask
    
    path('flask-health/', views.FlaskHealthView.as_view(), name='flask_health'),
    
    # Legacy endpoints for backward compatibility
    path('mood/', views.mood_proxy, name='mood_proxy'),
    
    # Generic Flask service proxy for any other endpoints
    path('flask/', views.flask_service_proxy, name='flask_service_proxy'),
    path('flask/<path:path>/', views.flask_service_proxy, name='flask_service_proxy_path'),
    
    # Express microservice (placeholder)
    path('express/', views.express_service_proxy, name='express_service_proxy'),
]
