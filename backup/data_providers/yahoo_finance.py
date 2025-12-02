import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
from .base import DataProvider

# Robust logging setup
try:
    from loguru import logger
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class YahooFinanceProvider(DataProvider):
    """Yahoo Finance data provider implementation"""
    
    def __init__(self):
        self.name = "Yahoo Finance"
    
    async def get_stock_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """
        Get historical stock data from Yahoo Finance
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            ticker = yf.Ticker(symbol)
            data = await asyncio.to_thread(ticker.history, period=period)
            
            if data.empty:
                logger.warning(f"No data found for symbol: {symbol}")
                return pd.DataFrame()
            
            # Clean and standardize column names
            data.columns = [col.replace(' ', '_').lower() for col in data.columns]
            data.reset_index(inplace=True)
            
            logger.info(f"Retrieved {len(data)} rows of data for {symbol}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching stock data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    async def get_real_time_price(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock price and key metrics"""
        try:
            ticker = yf.Ticker(symbol)
            info = await asyncio.to_thread(lambda: ticker.info)
            
            return {
                'symbol': symbol,
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'change': info.get('currentPrice', 0) - info.get('previousClose', 0),
                'change_percent': ((info.get('currentPrice', 0) - info.get('previousClose', 0)) / info.get('previousClose', 1)) * 100,
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching real-time price for {symbol}: {str(e)}")
            return {}
    
    async def get_financial_statements(self, symbol: str) -> Dict[str, Any]:
        """Get financial statements (Income Statement, Balance Sheet, Cash Flow)"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get financial statements
            income_stmt = await asyncio.to_thread(lambda: ticker.financials)
            balance_sheet = await asyncio.to_thread(lambda: ticker.balance_sheet)
            cash_flow = await asyncio.to_thread(lambda: ticker.cashflow)
            
            return {
                'income_statement': income_stmt.to_dict() if not income_stmt.empty else {},
                'balance_sheet': balance_sheet.to_dict() if not balance_sheet.empty else {},
                'cash_flow': cash_flow.to_dict() if not cash_flow.empty else {},
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching financial statements for {symbol}: {str(e)}")
            return {}
    
    async def get_key_metrics(self, symbol: str) -> Dict[str, Any]:
        """Get key financial metrics and ratios"""
        try:
            ticker = yf.Ticker(symbol)
            info = await asyncio.to_thread(lambda: ticker.info)
            
            return {
                'symbol': symbol,
                'company_name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                
                # Valuation Metrics
                'market_cap': info.get('marketCap', 0),
                'enterprise_value': info.get('enterpriseValue', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'peg_ratio': info.get('pegRatio', 0),
                'price_to_book': info.get('priceToBook', 0),
                'price_to_sales': info.get('priceToSalesTrailing12Months', 0),
                'ev_to_revenue': info.get('enterpriseToRevenue', 0),
                'ev_to_ebitda': info.get('enterpriseToEbitda', 0),
                
                # Profitability Metrics
                'profit_margin': info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0,
                'operating_margin': info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0,
                'return_on_assets': info.get('returnOnAssets', 0) * 100 if info.get('returnOnAssets') else 0,
                'return_on_equity': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
                
                # Financial Health
                'current_ratio': info.get('currentRatio', 0),
                'quick_ratio': info.get('quickRatio', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'total_cash': info.get('totalCash', 0),
                'total_debt': info.get('totalDebt', 0),
                
                # Growth Metrics
                'revenue_growth': info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0,
                'earnings_growth': info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else 0,
                
                # Dividend Information
                'dividend_rate': info.get('dividendRate', 0),
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'payout_ratio': info.get('payoutRatio', 0) * 100 if info.get('payoutRatio') else 0,
                
                # Trading Metrics
                'beta': info.get('beta', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0),
                'avg_volume': info.get('averageVolume', 0),
                
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching key metrics for {symbol}: {str(e)}")
            return {}
    
    async def get_analyst_recommendations(self, symbol: str) -> Dict[str, Any]:
        """Get analyst recommendations and target prices"""
        try:
            ticker = yf.Ticker(symbol)
            recommendations = await asyncio.to_thread(lambda: ticker.recommendations)
            
            if recommendations is None or recommendations.empty:
                return {}
            
            # Get latest recommendations
            latest = recommendations.tail(5)
            
            return {
                'symbol': symbol,
                'recommendations': latest.to_dict('records'),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching analyst recommendations for {symbol}: {str(e)}")
            return {}
