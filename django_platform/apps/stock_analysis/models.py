"""
Stock Analysis app models
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class StockSymbol(models.Model):
    """Stock symbol information"""
    
    symbol = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=200)
    exchange = models.CharField(max_length=20)
    sector = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    market_cap = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stock_symbol'
        verbose_name = 'Stock Symbol'
        verbose_name_plural = 'Stock Symbols'
        ordering = ['symbol']
    
    def __str__(self):
        return f"{self.symbol} - {self.company_name}"


class StockData(models.Model):
    """Historical stock data"""
    
    symbol = models.ForeignKey(StockSymbol, on_delete=models.CASCADE, related_name='historical_data')
    date = models.DateField()
    open_price = models.DecimalField(max_digits=12, decimal_places=4)
    high_price = models.DecimalField(max_digits=12, decimal_places=4)
    low_price = models.DecimalField(max_digits=12, decimal_places=4)
    close_price = models.DecimalField(max_digits=12, decimal_places=4)
    volume = models.BigIntegerField()
    adjusted_close = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    
    class Meta:
        db_table = 'stock_data'
        verbose_name = 'Stock Data'
        verbose_name_plural = 'Stock Data'
        unique_together = ['symbol', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.symbol.symbol} - {self.date}"


class TechnicalIndicator(models.Model):
    """Technical indicators for stocks"""
    
    symbol = models.ForeignKey(StockSymbol, on_delete=models.CASCADE, related_name='indicators')
    date = models.DateField()
    
    # Moving averages
    sma_20 = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    sma_50 = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    sma_200 = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    ema_12 = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    ema_26 = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    
    # Oscillators
    rsi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    macd = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    macd_signal = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    macd_histogram = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    
    # Bollinger Bands
    bb_upper = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    bb_middle = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    bb_lower = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    
    # Volume indicators
    volume_sma = models.BigIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'technical_indicator'
        verbose_name = 'Technical Indicator'
        verbose_name_plural = 'Technical Indicators'
        unique_together = ['symbol', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.symbol.symbol} Indicators - {self.date}"


class AnalysisRequest(models.Model):
    """User analysis requests"""
    
    ANALYSIS_TYPES = [
        ('technical', 'Technical Analysis'),
        ('fundamental', 'Fundamental Analysis'),
        ('sentiment', 'Sentiment Analysis'),
        ('comprehensive', 'Comprehensive Analysis'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analysis_requests')
    symbol = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Request parameters
    timeframe = models.CharField(max_length=10, default='1y')  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    custom_prompt = models.TextField(blank=True)
    
    # Results
    result_data = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    processing_time = models.DurationField(null=True, blank=True)
    
    class Meta:
        db_table = 'analysis_request'
        verbose_name = 'Analysis Request'
        verbose_name_plural = 'Analysis Requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.symbol.symbol} ({self.analysis_type})"


class UserWatchlist(models.Model):
    """User stock watchlists"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_watchlist'
        verbose_name = 'User Watchlist'
        verbose_name_plural = 'User Watchlists'
        unique_together = ['user', 'name']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.user.email} - {self.name}"


class WatchlistItem(models.Model):
    """Items in user watchlists"""
    
    watchlist = models.ForeignKey(UserWatchlist, on_delete=models.CASCADE, related_name='items')
    symbol = models.ForeignKey(StockSymbol, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    
    # Alert settings
    price_alert_high = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    price_alert_low = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    volume_alert = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'watchlist_item'
        verbose_name = 'Watchlist Item'
        verbose_name_plural = 'Watchlist Items'
        unique_together = ['watchlist', 'symbol']
        ordering = ['added_at']
    
    def __str__(self):
        return f"{self.watchlist.name} - {self.symbol.symbol}"


class MarketData(models.Model):
    """Current market data and real-time info"""
    
    symbol = models.OneToOneField(StockSymbol, on_delete=models.CASCADE, related_name='market_data')
    current_price = models.DecimalField(max_digits=12, decimal_places=4)
    change = models.DecimalField(max_digits=12, decimal_places=4)
    change_percent = models.DecimalField(max_digits=6, decimal_places=2)
    volume = models.BigIntegerField()
    market_cap = models.BigIntegerField(null=True, blank=True)
    pe_ratio = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    fifty_two_week_high = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    fifty_two_week_low = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    last_updated = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'market_data'
        verbose_name = 'Market Data'
        verbose_name_plural = 'Market Data'
    
    def __str__(self):
        return f"{self.symbol.symbol} - ${self.current_price}"
