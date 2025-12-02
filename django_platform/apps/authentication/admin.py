"""
Authentication app admin configuration
"""

from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, APIKey


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User Profile admin"""
    
    list_display = ('user', 'risk_tolerance', 'investment_experience', 'location')
    list_filter = ('risk_tolerance', 'investment_experience', 'created_at')
    search_fields = ('user__username', 'user__email', 'location')
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'bio', 'location', 'birth_date')
        }),
        ('Trading Preferences', {
            'fields': ('risk_tolerance', 'investment_experience', 'preferred_sectors')
        }),
        ('Settings', {
            'fields': ('notification_preferences', 'is_premium', 'api_usage_count')
        }),
    )


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    """API Key admin"""
    
    list_display = ('user', 'name', 'is_active', 'usage_count', 'rate_limit', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'user__email', 'name', 'key')
    raw_id_fields = ('user',)
    readonly_fields = ('key', 'usage_count', 'last_used')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'is_active')
        }),
        ('API Details', {
            'fields': ('key', 'rate_limit', 'usage_count', 'last_used')
        }),
    )
