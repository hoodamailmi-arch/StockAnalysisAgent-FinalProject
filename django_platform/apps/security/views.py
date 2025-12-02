"""
Security views
"""

from rest_framework import generics
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


def homepage(request):
    """Serve the main homepage"""
    return render(request, 'index.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Stock Analysis Platform is running',
        'version': '1.0.0'
    })


def custom_404(request, exception=None):
    """Custom 404 error handler"""
    return JsonResponse({
        'error': 'Not Found',
        'message': 'The requested resource was not found.',
        'status': 404
    }, status=404)


def custom_500(request):
    """Custom 500 error handler"""
    return JsonResponse({
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred.',
        'status': 500
    }, status=500)
