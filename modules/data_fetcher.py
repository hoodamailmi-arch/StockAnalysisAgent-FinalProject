# API Integration Module
# Handles all external API calls and data fetching

import requests
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
from .config import APIConfig, APISettings


class DataFetcher:
    """Main class for fetching data from various APIs"""
    
    @staticmethod
    def fetch_risk_free_rate():
        """Fetch current 10-Year Treasury rate from FRED API"""
        try:
            if not APIConfig.FRED_API_KEY:
                return APISettings.DEFAULT_RISK_FREE_RATE
                
            url = f"{APISettings.FRED_BASE_URL}?series_id={APISettings.FRED_TREASURY_SERIES}&api_key={APIConfig.FRED_API_KEY}&limit=1&sort_order=desc&file_type=json"
            response = requests.get(url, timeout=APISettings.TIMEOUT_SECONDS)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('observations') and len(data['observations']) > 0:
                    rate = float(data['observations'][0]['value']) / 100
                    return rate
        except Exception as e:
            st.warning(f"Could not fetch risk-free rate: {str(e)}")
        
        return APISettings.DEFAULT_RISK_FREE_RATE

    @staticmethod
    def fetch_alpha_vantage_fundamentals(symbol):
        """Fetch enhanced fundamentals from Alpha Vantage"""
        try:
            if not APIConfig.ALPHA_VANTAGE_API_KEY:
                return None
                
            url = f"{APISettings.ALPHA_VANTAGE_BASE_URL}?function=OVERVIEW&symbol={symbol}&apikey={APIConfig.ALPHA_VANTAGE_API_KEY}"
            response = requests.get(url, timeout=APISettings.TIMEOUT_SECONDS)
            
            if response.status_code == 200:
                data = response.json()
                if 'Symbol' in data:  # Valid response
                    return data
        except Exception as e:
            st.warning(f"Alpha Vantage API error: {str(e)}")
        
        return None

    @staticmethod
    def fetch_company_news(symbol):
        """Fetch recent company news from NewsAPI"""
        try:
            if not APIConfig.NEWS_API_KEY:
                return []
                
            # Get company name for better search
            ticker = yf.Ticker(symbol)
            info = ticker.info
            company_name = info.get('longName', symbol)
            
            url = f"{APISettings.NEWS_API_BASE_URL}?q={company_name}&sortBy=publishedAt&pageSize=10&apiKey={APIConfig.NEWS_API_KEY}&language=en"
            response = requests.get(url, timeout=APISettings.TIMEOUT_SECONDS)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
        except Exception as e:
            st.warning(f"NewsAPI error: {str(e)}")
        
        return []

    @staticmethod
    def get_stock_data(symbol, period="1y"):
        """Fetch comprehensive stock data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get stock info and historical data
            info = ticker.info
            hist = ticker.history(period=period)
            
            if hist.empty:
                return {"success": False, "error": "No data found"}
            
            return {
                "success": True,
                "info": info,
                "historical": hist,
                "symbol": symbol
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class MetricsCalculator:
    """Calculate financial metrics and technical indicators"""
    
    @staticmethod
    def get_enhanced_financial_metrics(stock_data, av_data, risk_free_rate):
        """Calculate comprehensive financial metrics combining all data sources"""
        metrics = {}
        info = stock_data['info']
        
        # Basic metrics from Yahoo Finance
        metrics['current_price'] = info.get('currentPrice', 0)
        metrics['market_cap'] = info.get('marketCap', 0)
        metrics['pe_ratio'] = info.get('trailingPE', 0)
        metrics['forward_pe'] = info.get('forwardPE', 0)
        metrics['peg_ratio'] = info.get('pegRatio', 0)
        metrics['price_to_book'] = info.get('priceToBook', 0)
        metrics['dividend_yield'] = info.get('dividendYield', 0)
        metrics['beta'] = info.get('beta', 0)
        metrics['debt_to_equity'] = info.get('debtToEquity', 0)
        metrics['roe'] = info.get('returnOnEquity', 0)
        metrics['profit_margin'] = info.get('profitMargins', 0)
        metrics['operating_margin'] = info.get('operatingMargins', 0)
        metrics['revenue_growth'] = info.get('revenueGrowth', 0)
        metrics['earnings_growth'] = info.get('earningsGrowth', 0)
        
        # Enhanced metrics from Alpha Vantage if available
        if av_data:
            metrics['ev_revenue'] = float(av_data.get('EVToRevenue', 0) or 0)
            metrics['ev_ebitda'] = float(av_data.get('EVToEBITDA', 0) or 0)
            metrics['price_to_sales'] = float(av_data.get('PriceToSalesRatioTTM', 0) or 0)
            metrics['price_to_cash_flow'] = float(av_data.get('PriceToCashFlowRatio', 0) or 0)
            metrics['current_ratio'] = float(av_data.get('CurrentRatio', 0) or 0)
            metrics['quick_ratio'] = float(av_data.get('QuickRatio', 0) or 0)
            metrics['analyst_target'] = float(av_data.get('AnalystTargetPrice', 0) or 0)
            metrics['52_week_high'] = float(av_data.get('52WeekHigh', 0) or 0)
            metrics['52_week_low'] = float(av_data.get('52WeekLow', 0) or 0)
        
        # Risk metrics
        metrics['risk_free_rate'] = risk_free_rate
        
        # Historical price data analysis
        if not stock_data['historical'].empty:
            hist = stock_data['historical']
            metrics['volatility'] = hist['Close'].pct_change().std() * np.sqrt(252)
            metrics['price_change_1m'] = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-22]) - 1) if len(hist) >= 22 else 0
            metrics['price_change_3m'] = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-66]) - 1) if len(hist) >= 66 else 0
            metrics['price_change_1y'] = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-252]) - 1) if len(hist) >= 252 else 0
        
        return metrics

    @staticmethod
    def calculate_technical_indicators(historical_data):
        """Calculate technical analysis indicators"""
        if historical_data.empty:
            return {}
        
        indicators = {}
        
        # Simple Moving Averages
        indicators['sma_20'] = historical_data['Close'].rolling(window=20).mean().iloc[-1]
        indicators['sma_50'] = historical_data['Close'].rolling(window=50).mean().iloc[-1]
        indicators['current_price'] = historical_data['Close'].iloc[-1]
        
        # RSI Calculation
        delta = historical_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        indicators['rsi'] = 100 - (100 / (1 + rs)).iloc[-1]
        
        # Price performance
        indicators['sma_20_diff'] = ((indicators['current_price'] / indicators['sma_20']) - 1) * 100 if not pd.isna(indicators['sma_20']) else 0
        indicators['sma_50_diff'] = ((indicators['current_price'] / indicators['sma_50']) - 1) * 100 if not pd.isna(indicators['sma_50']) else 0
        
        return indicators
