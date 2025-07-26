from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Health check endpoint
    path('health/', views.health_check, name='health_check'),
    
    # Microservice proxy endpoints
    path('sentiment/', views.sentiment_proxy, name='sentiment_proxy'),
    path('mood/', views.mood_proxy, name='mood_proxy'),
    
    # Flask microservice endpoints
    path('flask/', views.flask_service_proxy, name='flask_service_proxy'),
    
    # Express microservice endpoints  
    path('express/', views.express_service_proxy, name='express_service_proxy'),
]
