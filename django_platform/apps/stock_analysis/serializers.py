"""
Stock Analysis app serializers
"""

from rest_framework import serializers
from .models import (
    StockSymbol, StockData, TechnicalIndicator,
    AnalysisRequest, UserWatchlist, WatchlistItem, MarketData
)


class StockSymbolSerializer(serializers.ModelSerializer):
    """Stock symbol serializer"""
    
    class Meta:
        model = StockSymbol
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class StockDataSerializer(serializers.ModelSerializer):
    """Stock data serializer"""
    
    symbol_name = serializers.CharField(source='symbol.symbol', read_only=True)
    
    class Meta:
        model = StockData
        fields = '__all__'


class TechnicalIndicatorSerializer(serializers.ModelSerializer):
    """Technical indicator serializer"""
    
    symbol_name = serializers.CharField(source='symbol.symbol', read_only=True)
    
    class Meta:
        model = TechnicalIndicator
        fields = '__all__'
        read_only_fields = ('created_at',)


class AnalysisRequestSerializer(serializers.ModelSerializer):
    """Analysis request serializer"""
    
    symbol_name = serializers.CharField(source='symbol.symbol', read_only=True)
    company_name = serializers.CharField(source='symbol.company_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = AnalysisRequest
        fields = '__all__'
        read_only_fields = (
            'id', 'user', 'result_data', 'error_message',
            'created_at', 'updated_at', 'completed_at', 'processing_time'
        )
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AnalysisResultSerializer(serializers.ModelSerializer):
    """Analysis result serializer for public consumption"""
    
    symbol_name = serializers.CharField(source='symbol.symbol', read_only=True)
    company_name = serializers.CharField(source='symbol.company_name', read_only=True)
    
    class Meta:
        model = AnalysisRequest
        fields = (
            'id', 'symbol_name', 'company_name', 'analysis_type',
            'status', 'timeframe', 'result_data', 'created_at',
            'completed_at', 'processing_time'
        )


class WatchlistItemSerializer(serializers.ModelSerializer):
    """Watchlist item serializer"""
    
    symbol_data = StockSymbolSerializer(source='symbol', read_only=True)
    
    class Meta:
        model = WatchlistItem
        fields = '__all__'
        read_only_fields = ('added_at',)


class UserWatchlistSerializer(serializers.ModelSerializer):
    """User watchlist serializer"""
    
    items = WatchlistItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UserWatchlist
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def get_item_count(self, obj):
        return obj.items.count()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class MarketDataSerializer(serializers.ModelSerializer):
    """Market data serializer"""
    
    symbol_data = StockSymbolSerializer(source='symbol', read_only=True)
    
    class Meta:
        model = MarketData
        fields = '__all__'


class StockOverviewSerializer(serializers.ModelSerializer):
    """Stock overview with current market data"""
    
    market_data = MarketDataSerializer(read_only=True)
    latest_indicators = serializers.SerializerMethodField()
    
    class Meta:
        model = StockSymbol
        fields = ('symbol', 'company_name', 'exchange', 'sector', 'industry', 'market_data', 'latest_indicators')
    
    def get_latest_indicators(self, obj):
        latest = obj.indicators.first()
        if latest:
            return TechnicalIndicatorSerializer(latest).data
        return None


class StockAnalysisCreateSerializer(serializers.Serializer):
    """Serializer for creating stock analysis requests"""
    
    symbol = serializers.CharField(max_length=10)
    analysis_type = serializers.ChoiceField(choices=AnalysisRequest.ANALYSIS_TYPES)
    timeframe = serializers.CharField(max_length=10, default='1y')
    custom_prompt = serializers.CharField(required=False, allow_blank=True)
    
    def validate_symbol(self, value):
        value = value.upper()
        try:
            StockSymbol.objects.get(symbol=value, is_active=True)
        except StockSymbol.DoesNotExist:
            raise serializers.ValidationError(f"Stock symbol '{value}' not found or inactive")
        return value
    
    def create(self, validated_data):
        symbol = StockSymbol.objects.get(symbol=validated_data['symbol'])
        return AnalysisRequest.objects.create(
            user=self.context['request'].user,
            symbol=symbol,
            analysis_type=validated_data['analysis_type'],
            timeframe=validated_data.get('timeframe', '1y'),
            custom_prompt=validated_data.get('custom_prompt', '')
        )
