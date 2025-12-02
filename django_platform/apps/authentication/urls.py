"""
Authentication app URLs
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'authentication'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    # API key management
    path('api-keys/', views.APIKeyListCreateView.as_view(), name='api-keys'),
    path('api-keys/<int:pk>/', views.APIKeyDetailView.as_view(), name='api-key-detail'),
    
    # User utilities
    path('stats/', views.user_stats, name='user-stats'),
    path('deactivate/', views.deactivate_account, name='deactivate-account'),
]
