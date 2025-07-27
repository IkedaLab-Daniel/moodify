from django.urls import path
from . import views

urlpatterns = [
    # Health check endpoint
    path('', views.health_check, name='health_check'),
    path('health/', views.health_check, name='health_check_alt'),
    
    # Flask microservice endpoints (sentiment analysis)
    path('sentiment/predict/', views.sentiment_predict, name='sentiment_predict'), # ? light TextBlob
    path('sentiment/analyze/', views.sentiment_analyze, name='sentiment_analyze'), # ? heavy BERT
    path('sentiment/analyze-light/', views.sentiment_analyze_light, name='sentiment_analyze_light'), # ? light VADER
    path('sentiment/moodify/', views.sentiment_moodify, name='sentiment_moodify'),
    
    # Express microservice endpoints (placeholder for future implementation)
    path('express/health/', views.express_health, name='express_health'),
    
    # Gateway status
    path('status/', views.gateway_status, name='gateway_status'),
]