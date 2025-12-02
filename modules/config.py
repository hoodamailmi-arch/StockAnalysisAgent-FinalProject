# Configuration and Constants
# Global settings for the Professional Stock Analytics Platform

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
class APIConfig:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    FRED_API_KEY = os.getenv('FRED_API_KEY')

# UI Configuration
class UIConfig:
    # Color Scheme (Dark Theme)
    COLORS = {
        'primary_bg': '#000000',
        'secondary_bg': '#1c1c1e',
        'tertiary_bg': '#2c2c2e',
        'card_bg': '#1c1c1e',
        'border_color': '#38383a',
        'text_primary': '#ffffff',
        'text_secondary': '#8e8e93',
        'accent_blue': '#007aff',
        'accent_green': '#30d158',
        'accent_red': '#ff453a',
        'accent_orange': '#ff9f0a',
        'surface': 'rgba(255, 255, 255, 0.05)',
        'hover': 'rgba(255, 255, 255, 0.1)'
    }
    
    # Typography
    FONTS = {
        'primary': 'Inter',
        'system': '-apple-system, BlinkMacSystemFont, sans-serif'
    }
    
    # Layout
    LAYOUT = {
        'border_radius': '12px',
        'card_padding': '24px',
        'section_spacing': '32px'
    }

# App Configuration
class AppConfig:
    # Page settings
    PAGE_TITLE = "Professional Stock Analytics"
    PAGE_ICON = "▓"
    LAYOUT = "wide"
    
    # Default values
    DEFAULT_SYMBOL = "AAPL"
    DEFAULT_PERIOD = "1y"
    
    # Stock suggestions
    POPULAR_STOCKS = {
        "Apple Inc.": "AAPL",
        "Microsoft Corp.": "MSFT", 
        "Amazon.com Inc.": "AMZN",
        "Alphabet Inc.": "GOOGL",
        "Tesla Inc.": "TSLA",
        "Meta Platforms": "META",
        "NVIDIA Corp.": "NVDA",
        "Netflix Inc.": "NFLX",
        "Adobe Inc.": "ADBE",
        "Salesforce Inc.": "CRM"
    }
    
    # Time periods
    TIME_PERIODS = ["1mo", "3mo", "6mo", "1y", "2y", "5y"]

# API URLs and Settings
class APISettings:
    # FRED API
    FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
    FRED_TREASURY_SERIES = "GS10"
    
    # Alpha Vantage API
    ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
    
    # News API
    NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"
    
    # Request timeouts
    TIMEOUT_SECONDS = 15
    
    # Default fallback values
    DEFAULT_RISK_FREE_RATE = 0.03  # 3%
