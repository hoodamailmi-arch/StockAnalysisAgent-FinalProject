"""
Stock Analysis app views
"""

from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import timedelta
import uuid

from .models import (
    StockSymbol, StockData, TechnicalIndicator,
    AnalysisRequest, UserWatchlist, WatchlistItem, MarketData
)
from .serializers import (
    StockSymbolSerializer, StockDataSerializer, TechnicalIndicatorSerializer,
    AnalysisRequestSerializer, AnalysisResultSerializer, UserWatchlistSerializer,
    WatchlistItemSerializer, MarketDataSerializer, StockOverviewSerializer,
    StockAnalysisCreateSerializer
)
from .tasks import process_stock_analysis
from .utils import get_stock_data, update_market_data


class StockSymbolListView(generics.ListAPIView):
    """List all stock symbols"""
    
    queryset = StockSymbol.objects.filter(is_active=True)
    serializer_class = StockSymbolSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['exchange', 'sector', 'industry']
    search_fields = ['symbol', 'company_name']
    ordering_fields = ['symbol', 'market_cap']
    ordering = ['symbol']
    
    permission_classes = [permissions.IsAuthenticated]


class StockOverviewView(generics.RetrieveAPIView):
    """Get stock overview with current market data"""
    
    queryset = StockSymbol.objects.filter(is_active=True)
    serializer_class = StockOverviewSerializer
    lookup_field = 'symbol'
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        symbol = self.kwargs['symbol'].upper()
        return get_object_or_404(StockSymbol, symbol=symbol, is_active=True)


class StockDataView(generics.ListAPIView):
    """Get historical stock data"""
    
    serializer_class = StockDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['date']
    ordering = ['-date']
    
    def get_queryset(self):
        symbol = self.kwargs['symbol'].upper()
        stock = get_object_or_404(StockSymbol, symbol=symbol, is_active=True)
        
        # Get timeframe from query params
        timeframe = self.request.query_params.get('timeframe', '1y')
        end_date = timezone.now().date()
        
        # Calculate start date based on timeframe
        timeframe_days = {
            '1d': 1, '5d': 5, '1mo': 30, '3mo': 90,
            '6mo': 180, '1y': 365, '2y': 730, '5y': 1825
        }
        
        days = timeframe_days.get(timeframe, 365)
        start_date = end_date - timedelta(days=days)
        
        return StockData.objects.filter(
            symbol=stock,
            date__gte=start_date,
            date__lte=end_date
        )


class TechnicalIndicatorView(generics.ListAPIView):
    """Get technical indicators for a stock"""
    
    serializer_class = TechnicalIndicatorSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['-date']
    
    def get_queryset(self):
        symbol = self.kwargs['symbol'].upper()
        stock = get_object_or_404(StockSymbol, symbol=symbol, is_active=True)
        
        # Get timeframe from query params
        timeframe = self.request.query_params.get('timeframe', '1y')
        end_date = timezone.now().date()
        
        # Calculate start date based on timeframe
        timeframe_days = {
            '1d': 1, '5d': 5, '1mo': 30, '3mo': 90,
            '6mo': 180, '1y': 365, '2y': 730, '5y': 1825
        }
        
        days = timeframe_days.get(timeframe, 365)
        start_date = end_date - timedelta(days=days)
        
        return TechnicalIndicator.objects.filter(
            symbol=stock,
            date__gte=start_date,
            date__lte=end_date
        )


class CreateAnalysisView(generics.CreateAPIView):
    """Create a new stock analysis request"""
    
    serializer_class = StockAnalysisCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        analysis_request = serializer.save()
        
        # Queue the analysis task
        process_stock_analysis.delay(str(analysis_request.id))
        
        return Response({
            'id': analysis_request.id,
            'status': analysis_request.status,
            'message': 'Analysis request created and queued for processing'
        }, status=status.HTTP_201_CREATED)


class AnalysisRequestListView(generics.ListAPIView):
    """List user's analysis requests"""
    
    serializer_class = AnalysisResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'analysis_type']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return AnalysisRequest.objects.filter(user=self.request.user)


class AnalysisResultView(generics.RetrieveAPIView):
    """Get analysis result by ID"""
    
    serializer_class = AnalysisResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return AnalysisRequest.objects.filter(user=self.request.user)


class UserWatchlistView(generics.ListCreateAPIView):
    """List and create user watchlists"""
    
    serializer_class = UserWatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserWatchlist.objects.filter(user=self.request.user)


class WatchlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Watchlist detail view"""
    
    serializer_class = UserWatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserWatchlist.objects.filter(user=self.request.user)


class WatchlistItemView(generics.ListCreateAPIView):
    """List and add items to watchlist"""
    
    serializer_class = WatchlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        watchlist_id = self.kwargs['watchlist_id']
        return WatchlistItem.objects.filter(
            watchlist_id=watchlist_id,
            watchlist__user=self.request.user
        )
    
    def perform_create(self, serializer):
        watchlist_id = self.kwargs['watchlist_id']
        watchlist = get_object_or_404(
            UserWatchlist,
            id=watchlist_id,
            user=self.request.user
        )
        serializer.save(watchlist=watchlist)


class WatchlistItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Watchlist item detail view"""
    
    serializer_class = WatchlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        watchlist_id = self.kwargs['watchlist_id']
        return WatchlistItem.objects.filter(
            watchlist_id=watchlist_id,
            watchlist__user=self.request.user
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def refresh_market_data(request, symbol):
    """Refresh market data for a stock"""
    symbol = symbol.upper()
    stock = get_object_or_404(StockSymbol, symbol=symbol, is_active=True)
    
    try:
        success = update_market_data(stock)
        if success:
            return Response({'message': f'Market data updated for {symbol}'})
        else:
            return Response(
                {'error': f'Failed to update market data for {symbol}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def market_overview(request):
    """Get market overview data"""
    # Get top market cap stocks
    top_stocks = StockSymbol.objects.filter(
        is_active=True,
        market_cap__isnull=False
    ).order_by('-market_cap')[:10]
    
    # Get user's watchlist items
    user_watchlists = request.user.watchlists.all()
    watchlist_stocks = []
    for watchlist in user_watchlists:
        for item in watchlist.items.all():
            if item.symbol not in watchlist_stocks:
                watchlist_stocks.append(item.symbol)
    
    # Get recent analysis requests
    recent_analyses = AnalysisRequest.objects.filter(
        user=request.user,
        status='completed'
    ).order_by('-completed_at')[:5]
    
    return Response({
        'top_stocks': StockOverviewSerializer(top_stocks, many=True).data,
        'watchlist_stocks': StockOverviewSerializer(watchlist_stocks, many=True).data,
        'recent_analyses': AnalysisResultSerializer(recent_analyses, many=True).data,
        'user_stats': {
            'total_analyses': request.user.analysis_requests.count(),
            'completed_analyses': request.user.analysis_requests.filter(status='completed').count(),
            'watchlists': request.user.watchlists.count(),
        }
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_stocks(request):
    """Search for stocks by symbol or company name"""
    query = request.query_params.get('q', '').strip()
    
    if len(query) < 2:
        return Response({'results': []})
    
    stocks = StockSymbol.objects.filter(
        Q(symbol__icontains=query) | Q(company_name__icontains=query),
        is_active=True
    )[:20]
    
    return Response({
        'results': StockSymbolSerializer(stocks, many=True).data
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def cancel_analysis(request, analysis_id):
    """Cancel a pending analysis request"""
    try:
        analysis = AnalysisRequest.objects.get(
            id=analysis_id,
            user=request.user,
            status='pending'
        )
        analysis.status = 'failed'
        analysis.error_message = 'Cancelled by user'
        analysis.save()
        
        return Response({'message': 'Analysis cancelled'})
    except AnalysisRequest.DoesNotExist:
        return Response(
            {'error': 'Analysis not found or cannot be cancelled'},
            status=status.HTTP_404_NOT_FOUND
        )
