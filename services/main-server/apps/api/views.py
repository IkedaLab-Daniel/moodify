import requests
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def simple_health_check(request):
    """Simple Django view without DRF to test basic access"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'simple-django-view',
        'method': request.method,
        'path': request.path
    })


class FlaskProxyMixin:
    """Mixin for proxying requests to Flask microservice"""
    
    def get_flask_url(self, endpoint):
        """Get the full Flask service URL for an endpoint"""
        base_url = getattr(settings, 'FLASK_SERVICE_URL', 'http://localhost:5000')
        return f"{base_url}/{endpoint.strip('/')}"
    
    def proxy_to_flask(self, request, endpoint):
        """Proxy request to Flask microservice"""
        try:
            flask_url = self.get_flask_url(endpoint)
            
            # Prepare request data
            kwargs = {'timeout': 30}
            
            if request.method == 'POST':
                if hasattr(request, 'data') and request.data:
                    kwargs['json'] = request.data
                else:
                    kwargs['json'] = {}
                kwargs['headers'] = {'Content-Type': 'application/json'}
            elif request.method == 'GET':
                kwargs['params'] = request.GET
            
            # Make request to Flask service
            response = requests.request(
                method=request.method,
                url=flask_url,
                **kwargs
            )
            
            # Return Flask response
            try:
                response_data = response.json() if response.content else {}
            except json.JSONDecodeError:
                response_data = {'content': response.text}
            
            return Response(response_data, status=response.status_code)
            
        except requests.exceptions.ConnectionError:
            return Response(
                {
                    'error': 'Flask microservice unavailable',
                    'message': 'Please ensure the Flask service is running on the configured URL',
                    'flask_url': self.get_flask_url(endpoint)
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except requests.exceptions.Timeout:
            return Response(
                {'error': 'Flask microservice timeout'},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        except Exception as e:
            logger.error(f"Unexpected error proxying to Flask: {e}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for the API gateway"""
    return Response({
        'status': 'healthy',
        'service': 'moodify-api-gateway',
        'version': '1.0.0',
        'flask_service': getattr(settings, 'FLASK_SERVICE_URL', 'http://localhost:5000'),
        'method': request.method,
        'authenticated': getattr(request, 'user', None) is not None and hasattr(request.user, 'is_authenticated') and request.user.is_authenticated
    })


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def test_endpoint(request):
    """Simple test endpoint to verify API access"""
    return Response({
        'message': 'Test endpoint working',
        'method': request.method,
        'data': request.data if request.method == 'POST' else None,
        'status': 'success'
    })

@method_decorator(csrf_exempt, name='dispatch')
class SentimentAnalysisView(APIView, FlaskProxyMixin):
    """
    Sentiment analysis endpoint - proxies to Flask /predict
    No authentication required for basic usage
    """
    authentication_classes = []  # Explicitly disable authentication
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Analyze sentiment of text"""
        return self.proxy_to_flask(request, 'predict')


@method_decorator(csrf_exempt, name='dispatch')
class EmotionAnalysisView(APIView, FlaskProxyMixin):
    """
    Advanced emotion analysis endpoint - proxies to Flask /analyze
    Uses BERT model with fallback to VADER
    """
    authentication_classes = []  # Explicitly disable authentication
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Analyze emotions in text using advanced models"""
        return self.proxy_to_flask(request, 'analyze')


@method_decorator(csrf_exempt, name='dispatch')
class LightEmotionAnalysisView(APIView, FlaskProxyMixin):
    """
    Lightweight emotion analysis endpoint - proxies to Flask /analyze-light
    Uses VADER sentiment analysis (fast, low memory)
    """
    authentication_classes = []  # Explicitly disable authentication
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Analyze emotions in text using lightweight VADER model"""
        return self.proxy_to_flask(request, 'analyze-light')


@method_decorator(csrf_exempt, name='dispatch')
class MoodifyView(APIView, FlaskProxyMixin):
    """
    Text transformation endpoint - proxies to Flask /moodify
    Transform text to target sentiment
    """
    authentication_classes = []  # Explicitly disable authentication
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Transform text to target sentiment"""
        return self.proxy_to_flask(request, 'moodify')


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def flask_health_check(request):
    """Flask service health check - proxies to Flask /"""
    try:
        flask_url = getattr(settings, 'FLASK_SERVICE_URL', 'http://localhost:5000')
        
        # Prepare request data
        kwargs = {'timeout': 30}
        
        # Make request to Flask service
        response = requests.get(flask_url, **kwargs)
        
        # Return Flask response
        try:
            response_data = response.json() if response.content else {}
        except json.JSONDecodeError:
            response_data = {'content': response.text}
        
        return Response(response_data, status=response.status_code)
        
    except requests.exceptions.ConnectionError:
        return Response(
            {
                'error': 'Flask microservice unavailable',
                'message': 'Please ensure the Flask service is running on the configured URL',
                'flask_url': flask_url
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except requests.exceptions.Timeout:
        return Response(
            {'error': 'Flask microservice timeout'},
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )
    except Exception as e:
        logger.error(f"Unexpected error proxying to Flask: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Legacy endpoints for backward compatibility
@csrf_exempt
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def sentiment_proxy(request):
    """Legacy sentiment analysis endpoint"""
    view = SentimentAnalysisView()
    view.request = request
    return view.post(request) if request.method == 'POST' else Response({'error': 'Use POST method'})


@csrf_exempt
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def mood_proxy(request):
    """Legacy mood analysis endpoint"""
    view = EmotionAnalysisView()
    view.request = request
    return view.post(request) if request.method == 'POST' else Response({'error': 'Use POST method'})


@csrf_exempt
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def flask_service_proxy(request):
    """Generic proxy for Flask microservice - for any unlisted endpoints"""
    try:
        # Get the path after /api/flask/
        path = request.path.replace('/api/flask/', '')
        
        proxy_mixin = FlaskProxyMixin()
        return proxy_mixin.proxy_to_flask(request, path)
        
    except Exception as e:
        logger.error(f"Unexpected error in flask_service_proxy: {e}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Remove express service proxy for now since we're focusing on Flask
@api_view(['GET'])
@permission_classes([AllowAny])
def express_service_proxy(request):
    """Express service not implemented yet"""
    return Response({
        'message': 'Express microservice not implemented yet',
        'available_services': ['flask']
    }, status=status.HTTP_501_NOT_IMPLEMENTED)
