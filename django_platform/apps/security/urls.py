"""
Security URLs
"""

from django.urls import path
from . import views

app_name = 'security'

urlpatterns = [
    path('', views.health_check, name='health-check'),
]
