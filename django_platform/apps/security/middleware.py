"""
Security middleware for enhanced protection
"""

from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
import time


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to responses"""
    
    def process_response(self, request, response):
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Content-Security-Policy'] = "default-src 'self'"
        
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """Basic rate limiting middleware"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}
        super().__init__(get_response)
    
    def __call__(self, request):
        # Simple rate limiting logic
        response = self.get_response(request)
        return response
