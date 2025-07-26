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
        'python_version': sys.version,
        'platform': platform.platform(),
        'debug': settings.DEBUG,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def info_view(request):
    """Return information about the API gateway and available services"""
    return Response({
        'name': 'Moodify API Gateway',
        'description': 'Central API gateway for the Moodify application',
        'version': '1.0.0',
        'endpoints': {
            'authentication': '/api/auth/',
            'sentiment_analysis': '/api/sentiment/',
            'mood_analysis': '/api/mood/',
            'flask_service': '/api/flask/',
            'express_service': '/api/express/',
            'health_check': '/api/health/',
            'status': '/api/core/status/',
            'info': '/api/core/info/',
        },
        'services': {
            'flask_microservice': settings.FLASK_SERVICE_URL,
            'express_microservice': settings.EXPRESS_SERVICE_URL,
        }
    })
