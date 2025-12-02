"""
Stock Analysis utilities
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from django.utils import timezone
from .models import StockSymbol, StockData, MarketData, TechnicalIndicator


def get_stock_data(symbol, timeframe='1y'):
    """Fetch stock data from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=timeframe)
        
        if hist.empty:
            return False
        
        stock_symbol, created = StockSymbol.objects.get_or_create(
            symbol=symbol.upper(),
            defaults={
                'company_name': symbol.upper(),
                'exchange': 'UNKNOWN'
            }
        )
        
        # Save historical data
        for date, row in hist.iterrows():
            StockData.objects.update_or_create(
                symbol=stock_symbol,
                date=date.date(),
                defaults={
                    'open_price': row['Open'],
                    'high_price': row['High'],
                    'low_price': row['Low'],
                    'close_price': row['Close'],
                    'volume': row['Volume'],
                    'adjusted_close': row['Close']
                }
            )
        
        return True
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return False


def update_market_data(stock_symbol):
    """Update current market data for a stock"""
    try:
        ticker = yf.Ticker(stock_symbol.symbol)
        info = ticker.info
        hist = ticker.history(period='1d')
        
        if hist.empty:
            return False
        
        latest = hist.iloc[-1]
        
        MarketData.objects.update_or_create(
            symbol=stock_symbol,
            defaults={
                'current_price': latest['Close'],
                'change': latest['Close'] - latest['Open'],
                'change_percent': ((latest['Close'] - latest['Open']) / latest['Open']) * 100,
                'volume': latest['Volume'],
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow'),
                'last_updated': timezone.now()
            }
        )
        
        return True
    except Exception as e:
        print(f"Error updating market data for {stock_symbol.symbol}: {e}")
        return False


def calculate_technical_indicators(symbol, period=50):
    """Calculate technical indicators for a stock"""
    try:
        stock_data = StockData.objects.filter(
            symbol__symbol=symbol
        ).order_by('date')[:period]
        
        if len(stock_data) < period:
            return False
        
        # Convert to pandas DataFrame
        df = pd.DataFrame([
            {
                'date': data.date,
                'open': float(data.open_price),
                'high': float(data.high_price),
                'low': float(data.low_price),
                'close': float(data.close_price),
                'volume': data.volume
            }
            for data in stock_data
        ])
        
        # Calculate indicators (simplified)
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        df['ema_12'] = df['close'].ewm(span=12).mean()
        df['ema_26'] = df['close'].ewm(span=26).mean()
        
        # Save indicators
        stock_symbol = StockSymbol.objects.get(symbol=symbol)
        for _, row in df.iterrows():
            TechnicalIndicator.objects.update_or_create(
                symbol=stock_symbol,
                date=row['date'],
                defaults={
                    'sma_20': row.get('sma_20'),
                    'sma_50': row.get('sma_50'),
                    'ema_12': row.get('ema_12'),
                    'ema_26': row.get('ema_26'),
                }
            )
        
        return True
    except Exception as e:
        print(f"Error calculating indicators for {symbol}: {e}")
        return False


def format_analysis_prompt(analysis_request):
    """Format the prompt for AI analysis"""
    
    symbol = analysis_request.symbol.symbol
    analysis_type = analysis_request.analysis_type
    timeframe = analysis_request.timeframe
    
    # Get recent stock data
    recent_data = StockData.objects.filter(
        symbol=analysis_request.symbol
    ).order_by('-date')[:30]
    
    # Get market data
    try:
        market_data = analysis_request.symbol.market_data
        current_price = market_data.current_price
        change_percent = market_data.change_percent
    except:
        current_price = None
        change_percent = None
    
    # Base prompt
    prompt = f"""
    Analyze {symbol} stock for {analysis_type} analysis with {timeframe} timeframe.
    
    Current Price: ${current_price}
    Change: {change_percent}%
    
    Recent price data:
    """
    
    for data in recent_data[:10]:
        prompt += f"Date: {data.date}, Close: ${data.close_price}, Volume: {data.volume}\n"
    
    if analysis_request.custom_prompt:
        prompt += f"\n\nAdditional instructions: {analysis_request.custom_prompt}"
    
    prompt += "\n\nProvide a comprehensive analysis with specific recommendations, price targets, and risk assessment."
    
    return prompt
