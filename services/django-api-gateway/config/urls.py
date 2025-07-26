"""
URL configuration for django-api-gateway project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gateway.urls')),
    path('', include('gateway.urls')),  # Root level access for health check
]
