"""Django API Gateway views for routing requests to microservices."""

import json
import logging

import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def check_service_health(service_url):
    """Check if a microservice is healthy"""
    try:
        response = requests.get(f"{service_url}/", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

@api_view(['GET'])
def health_check(request):
    """Homepage endpoint displaying Django API Gateway information"""
    return Response({
        "app_name": "Moodify API Gateway",
        "version": "1.0.0",
        "status": "healthy",
        "description": "Django-based API Gateway for the Moodify application - A microservices architecture for sentiment analysis and mood tracking",
        "message": "🚀 Welcome to Moodify API Gateway!",
        "features": [
            "Sentiment Analysis Routing",
            "Microservice Health Monitoring", 
            "Request Proxying",
            "Error Handling & Logging"
        ],
        "architecture": {
            "framework": "Django REST Framework",
            "pattern": "API Gateway",
            "connected_services": ["Flask Microservice", "Express Microservice (planned)"]
        },
        "available_endpoints": {
            "health_check": {
                "path": "/",
                "method": "GET",
                "description": "Homepage and health status"
            },
            "gateway_status": {
                "path": "/status/",
                "method": "GET", 
                "description": "Status of all connected microservices"
            },
            "sentiment_analysis": {
                "predict": "/sentiment/predict/",
                "analyze": "/sentiment/analyze/",
                "analyze_light": "/sentiment/analyze-light/",
                "moodify": "/sentiment/moodify/"
            },
            "express_service": {
                "health": "/express/health/"
            }
        },
        "microservices": {
            "flask_microservice": {
                "purpose": "Sentiment analysis using VADER, TextBlob, and BERT models",
                "endpoints": ["predict", "analyze", "analyze-light", "moodify"]
            },
            "express_microservice": {
                "purpose": "Planned for additional functionality",
                "status": "In development"
            }
        },
        "documentation": {
            "project_structure": "See /docs/PROJECT_STRUCTURE.md",
            "python_environments": "See /docs/PYTHON_ENVIRONMENTS.md"
        }
    })

@api_view(['GET'])
def gateway_status(request):
    """Check status of all connected microservices"""
    flask_url = settings.FLASK_MICROSERVICE_URL
    express_url = settings.EXPRESS_MICROSERVICE_URL

    flask_healthy = check_service_health(flask_url)
    express_healthy = check_service_health(express_url)

    return Response({
        "gateway": "healthy",
        "services": {
            "flask_microservice": {
                "url": flask_url,
                "status": "healthy" if flask_healthy else "unhealthy",
                "endpoints": (["/predict", "/analyze", "/analyze-light", "/moodify"]
                             if flask_healthy else [])
            },
            "express_microservice": {
                "url": express_url,
                "status": "healthy" if express_healthy else "unhealthy",
                "note": "Not yet implemented"
            }
        }
    })

def proxy_to_flask(endpoint, request_data=None, method='GET'):
    """Proxy requests to Flask microservice"""
    flask_url = settings.FLASK_MICROSERVICE_URL
    url = f"{flask_url}{endpoint}"

    try:
        if method == 'POST':
            response = requests.post(
                url,
                json=request_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
        else:
            response = requests.get(url, timeout=10)

        return response.json(), response.status_code
    except requests.exceptions.Timeout:
        logger.error("Timeout when calling Flask service: %s", url)
        return {"error": "Service timeout"}, 504
    except requests.exceptions.ConnectionError:
        logger.error("Connection error when calling Flask service: %s", url)
        return {"error": "Service unavailable"}, 503
    except requests.exceptions.RequestException as e:
        logger.error("Request error when calling Flask service: %s", e)
        return {"error": "Service error"}, 500
    except json.JSONDecodeError:
        logger.error("Invalid JSON response from Flask service")
        return {"error": "Invalid service response"}, 502

@api_view(['POST'])
def sentiment_predict(request):
    """Proxy to Flask /predict endpoint for basic sentiment analysis"""
    if not request.data:
        return Response({"error": "Request body is required"},
                       status=status.HTTP_400_BAD_REQUEST)

    if 'text' not in request.data:
        return Response({"error": "Missing 'text' field"},
                       status=status.HTTP_400_BAD_REQUEST)

    response_data, response_status = proxy_to_flask('/predict', request.data, 'POST')
    return Response(response_data, status=response_status)

@api_view(['POST'])
def sentiment_analyze(request):
    """Proxy to Flask /analyze endpoint for advanced emotion analysis"""
    if not request.data:
        return Response({"error": "Request body is required"},
                       status=status.HTTP_400_BAD_REQUEST)

    if 'text' not in request.data:
        return Response({"error": "Missing 'text' field"},
                       status=status.HTTP_400_BAD_REQUEST)

    response_data, response_status = proxy_to_flask('/analyze', request.data, 'POST')
    return Response(response_data, status=response_status)

@api_view(['POST'])
def sentiment_analyze_light(request):
    """Proxy to Flask /analyze-light endpoint for lightweight emotion analysis"""
    if not request.data:
        return Response({"error": "Request body is required"},
                       status=status.HTTP_400_BAD_REQUEST)

    if 'text' not in request.data:
        return Response({"error": "Missing 'text' field"},
                       status=status.HTTP_400_BAD_REQUEST)

    response_data, response_status = proxy_to_flask('/analyze-light', request.data, 'POST')
    return Response(response_data, status=response_status)

@api_view(['POST'])
def sentiment_moodify(request):
    """Proxy to Flask /moodify endpoint for text mood transformation"""
    if not request.data:
        return Response({"error": "Request body is required"},
                       status=status.HTTP_400_BAD_REQUEST)

    required_fields = ['text', 'target_sentiment']
    for field in required_fields:
        if field not in request.data:
            return Response({"error": f"Missing '{field}' field"},
                           status=status.HTTP_400_BAD_REQUEST)

    response_data, response_status = proxy_to_flask('/moodify', request.data, 'POST')
    return Response(response_data, status=response_status)

@api_view(['GET'])
def express_health(request):
    """Check Express microservice health (placeholder)"""
    express_url = settings.EXPRESS_MICROSERVICE_URL

    try:
        response = requests.get(f"{express_url}/health", timeout=5)
        return Response({
            "service": "Express Microservice",
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "url": express_url
        })
    except requests.exceptions.RequestException:
        return Response({
            "service": "Express Microservice",
            "status": "unavailable",
            "url": express_url,
            "note": "Service not yet implemented or not running"
        }, status=503)
