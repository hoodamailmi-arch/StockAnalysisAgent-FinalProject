"""
Stock Analysis app URLs
"""

from django.urls import path, include
from . import views
from . import frontend_views

app_name = 'stock_analysis'

urlpatterns = [
    # Frontend Pages
    path('analyzer/', frontend_views.stock_analyzer, name='analyzer'),
    path('dashboard/', frontend_views.market_dashboard, name='dashboard'),
    path('history/', frontend_views.analysis_history, name='history'),
    path('watchlists/', frontend_views.watchlists_view, name='watchlists-page'),
    path('watchlists/<int:watchlist_id>/', frontend_views.watchlist_detail, name='watchlist-detail-page'),
    
    # AJAX Endpoints
    path('ajax/search/', frontend_views.stock_search, name='ajax-search'),
    path('ajax/analyze/', frontend_views.ajax_analyze_stock, name='ajax-analyze'),
    path('ajax/stock-data/', frontend_views.get_stock_data, name='ajax-stock-data'),
    
    # API Stock symbol endpoints
    path('symbols/', views.StockSymbolListView.as_view(), name='stock-symbols'),
    path('symbols/<str:symbol>/', views.StockOverviewView.as_view(), name='stock-overview'),
    path('symbols/<str:symbol>/data/', views.StockDataView.as_view(), name='stock-data'),
    path('symbols/<str:symbol>/indicators/', views.TechnicalIndicatorView.as_view(), name='technical-indicators'),
    path('symbols/<str:symbol>/refresh/', views.refresh_market_data, name='refresh-market-data'),
    
    # API Analysis endpoints
    path('analyze/', views.CreateAnalysisView.as_view(), name='create-analysis'),
    path('analyses/', views.AnalysisRequestListView.as_view(), name='analysis-list'),
    path('analyses/<uuid:id>/', views.AnalysisResultView.as_view(), name='analysis-result'),
    path('analyses/<uuid:analysis_id>/cancel/', views.cancel_analysis, name='cancel-analysis'),
    
    # API Watchlist endpoints
    path('api/watchlists/', views.UserWatchlistView.as_view(), name='watchlists'),
    path('api/watchlists/<int:pk>/', views.WatchlistDetailView.as_view(), name='watchlist-detail'),
    path('api/watchlists/<int:watchlist_id>/items/', views.WatchlistItemView.as_view(), name='watchlist-items'),
    path('api/watchlists/<int:watchlist_id>/items/<int:pk>/', views.WatchlistItemDetailView.as_view(), name='watchlist-item-detail'),
    
    # API Utility endpoints
    path('search/', views.search_stocks, name='search-stocks'),
    path('overview/', views.market_overview, name='market-overview'),
]
