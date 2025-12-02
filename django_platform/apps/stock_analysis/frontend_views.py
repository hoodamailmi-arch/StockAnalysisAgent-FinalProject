"""
Frontend views for stock analysis web interface
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.core.paginator import Paginator
import json
import requests
from .models import StockSymbol, AnalysisRequest, UserWatchlist, WatchlistItem
from .serializers import StockSymbolSerializer, AnalysisRequestSerializer


def stock_analyzer(request):
    """Main stock analysis interface"""
    return render(request, 'stock_analysis/analyzer.html')


def market_dashboard(request):
    """Market overview dashboard"""
    # Get popular stocks for demo
    popular_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META', 'SPY']
    
    context = {
        'popular_symbols': popular_symbols
    }
    return render(request, 'stock_analysis/dashboard.html', context)


@login_required
def analysis_history(request):
    """User's analysis history"""
    analyses = AnalysisRequest.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(analyses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'analyses': page_obj.object_list
    }
    return render(request, 'stock_analysis/history.html', context)


@login_required
def watchlists_view(request):
    """User's watchlists"""
    watchlists = UserWatchlist.objects.filter(user=request.user)
    
    context = {
        'watchlists': watchlists
    }
    return render(request, 'stock_analysis/watchlists.html', context)


@login_required
def watchlist_detail(request, watchlist_id):
    """Individual watchlist view"""
    watchlist = get_object_or_404(UserWatchlist, id=watchlist_id, user=request.user)
    items = WatchlistItem.objects.filter(watchlist=watchlist).select_related('stock_symbol')
    
    context = {
        'watchlist': watchlist,
        'items': items
    }
    return render(request, 'stock_analysis/watchlist_detail.html', context)


def stock_search(request):
    """AJAX stock search"""
    query = request.GET.get('q', '')
    if len(query) < 1:
        return JsonResponse({'results': []})
    
    # Search stocks (simplified for demo)
    common_stocks = [
        'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META', 'SPY',
        'NFLX', 'UBER', 'BABA', 'DIS', 'PYPL', 'INTC', 'AMD', 'CRM',
        'ZOOM', 'SHOP', 'SQ', 'TWTR', 'SNAP', 'PINS', 'ROKU', 'SPOT'
    ]
    
    matches = [stock for stock in common_stocks if query.upper() in stock]
    results = [{'symbol': symbol, 'name': f'{symbol} Corporation'} for symbol in matches[:10]]
    
    return JsonResponse({'results': results})


@csrf_exempt
def ajax_analyze_stock(request):
    """AJAX endpoint for stock analysis"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        symbol = data.get('symbol', '').upper()
        analysis_type = data.get('analysis_type', 'basic')
        
        if not symbol:
            return JsonResponse({'error': 'Symbol is required'}, status=400)
        
        # Create analysis request (simplified)
        analysis_data = {
            'symbol': symbol,
            'analysis_type': analysis_type,
            'status': 'completed',  # For demo purposes
            'result': {
                'symbol': symbol,
                'current_price': 150.25,
                'change': '+2.45 (+1.66%)',
                'volume': '45.2M',
                'market_cap': '$2.85T',
                'pe_ratio': 28.5,
                'recommendation': 'BUY',
                'confidence': 85,
                'ai_analysis': f"Based on technical analysis, {symbol} shows strong upward momentum with support at $145 and resistance at $155. The stock has broken through key moving averages and shows positive momentum indicators. Volume patterns suggest institutional buying interest.",
                'technical_indicators': {
                    'RSI': 62.5,
                    'MACD': 'Bullish',
                    'SMA_50': 148.75,
                    'SMA_200': 142.30,
                    'Bollinger_Bands': 'Middle'
                },
                'key_levels': {
                    'support': [145.20, 142.50, 140.00],
                    'resistance': [155.75, 158.90, 162.00]
                }
            }
        }
        
        return JsonResponse(analysis_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_stock_data(request):
    """AJAX endpoint for real-time stock data"""
    symbol = request.GET.get('symbol', '').upper()
    
    if not symbol:
        return JsonResponse({'error': 'Symbol is required'}, status=400)
    
    # Mock real-time data (in production, this would call actual APIs)
    import random
    base_price = 150.00
    change = random.uniform(-5, 5)
    
    stock_data = {
        'symbol': symbol,
        'name': f'{symbol} Corporation',
        'price': round(base_price + change, 2),
        'change': round(change, 2),
        'change_percent': round((change / base_price) * 100, 2),
        'volume': f"{random.randint(10, 100)}.{random.randint(0, 9)}M",
        'market_cap': f"${random.randint(100, 3000)}B",
        'pe_ratio': round(random.uniform(15, 40), 1),
        'last_updated': 'Just now'
    }
    
    return JsonResponse(stock_data)


class StockAnalysisAjaxView(View):
    """AJAX view for stock analysis operations"""
    
    def post(self, request):
        """Handle analysis requests"""
        try:
            data = json.loads(request.body)
            symbol = data.get('symbol')
            analysis_type = data.get('analysis_type', 'basic')
            
            # Here you would integrate with your AI analysis system
            # For now, return mock data
            
            return JsonResponse({
                'status': 'success',
                'analysis_id': 'mock-123',
                'message': f'Analysis started for {symbol}'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
