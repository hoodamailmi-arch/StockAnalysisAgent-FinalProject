"""
Main URL configuration for stock_platform project.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apps.security.views import homepage

# API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Stock Analysis Platform API",
        default_version='v1',
        description="Professional Stock Market Analysis Platform with AI Insights",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@stockplatform.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Homepage
    path('', homepage, name='homepage'),
    
    # Stock Analysis Frontend Pages
    path('stocks/', include('apps.stock_analysis.urls')),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API v1
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/stocks/', include('apps.stock_analysis.urls')),
    path('api/v1/ai/', include('apps.ai_insights.urls')),
    path('api/v1/data/', include('apps.data_providers.urls')),
    
    # Health check
    path('health/', include('apps.security.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
