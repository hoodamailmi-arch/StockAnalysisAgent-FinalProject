"""
Stock Analysis app configuration
"""

from django.apps import AppConfig


class StockAnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.stock_analysis'
    verbose_name = 'Stock Analysis'
    
    def ready(self):
        """Import signal handlers"""
        import apps.stock_analysis.signals
