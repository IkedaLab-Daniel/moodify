import requests
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for the API gateway"""
    return Response({
        'status': 'healthy',
        'service': 'moodify-api-gateway',
        'version': '1.0.0'
    })


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def sentiment_proxy(request):
    """Proxy requests to the sentiment analysis service"""
    try:
        flask_url = f"{settings.FLASK_SERVICE_URL}/sentiment"
        
        if request.method == 'POST':
            # Forward POST data to Flask service
            response = requests.post(
                flask_url,
                json=request.data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
        else:
            # Forward GET request to Flask service
            response = requests.get(
                flask_url,
                params=request.GET,
                timeout=30
            )
        
        # Return the response from the Flask service
        return Response(
            response.json() if response.content else {},
            status=response.status_code
        )
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Flask service: {e}")
        return Response(
            {'error': 'Sentiment service unavailable'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logger.error(f"Unexpected error in sentiment_proxy: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def mood_proxy(request):
    """Proxy requests to the mood analysis service"""
    try:
        flask_url = f"{settings.FLASK_SERVICE_URL}/mood"
        
        if request.method == 'POST':
            response = requests.post(
                flask_url,
                json=request.data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
        else:
            response = requests.get(
                flask_url,
                params=request.GET,
                timeout=30
            )
        
        return Response(
            response.json() if response.content else {},
            status=response.status_code
        )
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Flask service: {e}")
        return Response(
            {'error': 'Mood service unavailable'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logger.error(f"Unexpected error in mood_proxy: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def flask_service_proxy(request):
    """Generic proxy for Flask microservice"""
    try:
        # Get the path after /api/flask/
        path = request.path.replace('/api/flask/', '')
        flask_url = f"{settings.FLASK_SERVICE_URL}/{path}"
        
        # Prepare request data
        kwargs = {
            'timeout': 30,
            'headers': {'Content-Type': 'application/json'}
        }
        
        if request.method in ['POST', 'PUT', 'PATCH']:
            kwargs['json'] = request.data
        elif request.method == 'GET':
            kwargs['params'] = request.GET
        
        # Make request to Flask service
        response = requests.request(
            method=request.method,
            url=flask_url,
            **kwargs
        )
        
        return Response(
            response.json() if response.content else {},
            status=response.status_code
        )
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Flask service: {e}")
        return Response(
            {'error': 'Flask service unavailable'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logger.error(f"Unexpected error in flask_service_proxy: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def express_service_proxy(request):
    """Generic proxy for Express microservice"""
    try:
        # Get the path after /api/express/
        path = request.path.replace('/api/express/', '')
        express_url = f"{settings.EXPRESS_SERVICE_URL}/{path}"
        
        # Prepare request data
        kwargs = {
            'timeout': 30,
            'headers': {'Content-Type': 'application/json'}
        }
        
        if request.method in ['POST', 'PUT', 'PATCH']:
            kwargs['json'] = request.data
        elif request.method == 'GET':
            kwargs['params'] = request.GET
        
        # Make request to Express service
        response = requests.request(
            method=request.method,
            url=express_url,
            **kwargs
        )
        
        return Response(
            response.json() if response.content else {},
            status=response.status_code
        )
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Express service: {e}")
        return Response(
            {'error': 'Express service unavailable'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logger.error(f"Unexpected error in express_service_proxy: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
