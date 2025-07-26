from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Core functionality endpoints
    path('status/', views.status_view, name='status'),
    path('info/', views.info_view, name='info'),
]
