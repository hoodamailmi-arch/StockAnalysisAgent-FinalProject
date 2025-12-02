# Professional Stock Market Analysis Platform
# Enterprise-grade financial intelligence with dark theme

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import os
from datetime import datetime, timedelta
from groq import Groq
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Professional Stock Analytics",
    page_icon="▓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Dark Theme CSS - Apple-inspired Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Variables */
    :root {
        --primary-bg: #000000;
        --secondary-bg: #1c1c1e;
        --tertiary-bg: #2c2c2e;
        --card-bg: #1c1c1e;
        --border-color: #38383a;
        --text-primary: #ffffff;
        --text-secondary: #8e8e93;
        --accent-blue: #007aff;
        --accent-green: #30d158;
        --accent-red: #ff453a;
        --accent-orange: #ff9f0a;
        --surface: rgba(255, 255, 255, 0.05);
        --hover: rgba(255, 255, 255, 0.1);
    }
    
    /* Base Styling */
    .stApp {
        background-color: var(--primary-bg);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit Elements */
    .stDeployButton { display: none; }
    header[data-testid="stHeader"] { display: none; }
    .stMainMenu { display: none; }
    footer { display: none; }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--secondary-bg);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    
    /* Main Header */
    .main-header {
        background: var(--secondary-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 32px;
        text-align: center;
        backdrop-filter: blur(20px);
    }
    
    .main-title {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 8px;
        color: var(--text-primary);
        letter-spacing: -0.025em;
    }
    
    .main-subtitle {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        color: var(--text-secondary);
        letter-spacing: -0.01em;
    }
    
    /* Section Headers */
    .section-header {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        padding: 16px 24px;
        border-radius: 12px;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 24px 0 16px 0;
        text-align: left;
        letter-spacing: -0.01em;
    }
    
    /* Chart Container */
    .chart-container {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
    }
    
    /* AI Analysis */
    .ai-analysis {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        position: relative;
    }
    
    .ai-analysis::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-green));
        border-radius: 16px 16px 0 0;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: var(--secondary-bg);
        border-right: 1px solid var(--border-color);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: var(--tertiary-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stSelectbox > div > div > select {
        background: var(--tertiary-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--accent-blue);
        border: none;
        border-radius: 8px;
        color: white;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 500;
        padding: 12px 24px;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #0056d6;
        transform: translateY(-1px);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--secondary-bg);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--text-secondary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 500;
        padding: 12px 16px;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-blue);
        color: white;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 16px;
    }
    
    [data-testid="metric-container"] [data-testid="metric-label"] {
        color: var(--text-secondary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Progress Bar */
    .stProgress .st-bo {
        background: var(--tertiary-bg);
        border-radius: 8px;
    }
    
    .stProgress .st-bp {
        background: var(--accent-blue);
        border-radius: 8px;
    }
    
    /* Custom Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
        letter-spacing: -0.025em;
    }
    
    p, span, div {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    
    /* Status Indicators */
    .status-active {
        color: var(--accent-green);
        font-weight: 600;
    }
    
    .status-inactive {
        color: var(--accent-red);
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        background: var(--secondary-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        margin-top: 32px;
        text-align: center;
    }
    
    .footer-title {
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .footer-subtitle {
        color: var(--text-secondary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# API Integration Functions
def fetch_risk_free_rate():
    """Fetch current 10-Year Treasury rate from FRED API"""
    try:
        fred_api_key = os.getenv('FRED_API_KEY')
        if not fred_api_key:
            return 0.03  # Default 3% if no API key
            
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id=GS10&api_key={fred_api_key}&limit=1&sort_order=desc&file_type=json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('observations') and len(data['observations']) > 0:
                rate = float(data['observations'][0]['value']) / 100
                return rate
    except Exception as e:
        st.warning(f"Could not fetch risk-free rate: {str(e)}")
    
    return 0.03  # Default fallback rate

def fetch_alpha_vantage_fundamentals(symbol):
    """Fetch enhanced fundamentals from Alpha Vantage"""
    try:
        av_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not av_api_key:
            return None
            
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={av_api_key}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if 'Symbol' in data:  # Valid response
                return data
    except Exception as e:
        st.warning(f"Alpha Vantage API error: {str(e)}")
    
    return None

def fetch_company_news(symbol):
    """Fetch recent company news from NewsAPI"""
    try:
        news_api_key = os.getenv('NEWS_API_KEY')
        if not news_api_key:
            return []
            
        # Get company name for better search
        ticker = yf.Ticker(symbol)
        info = ticker.info
        company_name = info.get('longName', symbol)
        
        url = f"https://newsapi.org/v2/everything?q={company_name}&sortBy=publishedAt&pageSize=10&apiKey={news_api_key}&language=en"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('articles', [])
    except Exception as e:
        st.warning(f"NewsAPI error: {str(e)}")
    
    return []

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

def create_enhanced_ai_analysis(symbol, enhanced_metrics, news_articles):
    """Generate comprehensive AI analysis using enhanced data"""
    try:
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        # Prepare comprehensive context
        financial_context = f"""
        Stock: {symbol}
        Current Price: ${enhanced_metrics.get('current_price', 0):.2f}
        Market Cap: ${enhanced_metrics.get('market_cap', 0):,.0f}
        P/E Ratio: {enhanced_metrics.get('pe_ratio', 0):.2f}
        Forward P/E: {enhanced_metrics.get('forward_pe', 0):.2f}
        PEG Ratio: {enhanced_metrics.get('peg_ratio', 0):.2f}
        Price-to-Book: {enhanced_metrics.get('price_to_book', 0):.2f}
        Price-to-Sales: {enhanced_metrics.get('price_to_sales', 0):.2f}
        EV/Revenue: {enhanced_metrics.get('ev_revenue', 0):.2f}
        EV/EBITDA: {enhanced_metrics.get('ev_ebitda', 0):.2f}
        Beta: {enhanced_metrics.get('beta', 0):.2f}
        Volatility: {enhanced_metrics.get('volatility', 0):.2%}
        ROE: {enhanced_metrics.get('roe', 0):.2%}
        Profit Margin: {enhanced_metrics.get('profit_margin', 0):.2%}
        Revenue Growth: {enhanced_metrics.get('revenue_growth', 0):.2%}
        Current Ratio: {enhanced_metrics.get('current_ratio', 0):.2f}
        Debt-to-Equity: {enhanced_metrics.get('debt_to_equity', 0):.2f}
        1-Month Performance: {enhanced_metrics.get('price_change_1m', 0):.2%}
        3-Month Performance: {enhanced_metrics.get('price_change_3m', 0):.2%}
        1-Year Performance: {enhanced_metrics.get('price_change_1y', 0):.2%}
        """
        
        # Add recent news context
        news_context = ""
        if news_articles:
            news_context = "Recent News Headlines:\\n"
            for article in news_articles[:5]:
                news_context += f"- {article.get('title', '')}\\n"
        
        prompt = f"""
        As a senior financial analyst, provide a comprehensive investment analysis for {symbol} based on the following data:

        {financial_context}

        {news_context}

        Please provide:
        1. **Investment Thesis** (2-3 key points)
        2. **Valuation Assessment** (fairly valued, undervalued, or overvalued)
        3. **Key Strengths** (3-4 positive factors)
        4. **Key Risks** (3-4 concerns or risks)
        5. **Technical Outlook** (price momentum and trend analysis)
        6. **Investment Recommendation** (Buy/Hold/Sell with price target if possible)

        Focus on actionable insights and be specific about why you reached your conclusions. Consider both fundamental and technical factors.
        """
        
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500,
            top_p=1,
            stream=False
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"AI Analysis Error: {str(e)}"

def get_stock_data(symbol, period="1y"):
    """Fetch comprehensive stock data"""
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

def get_us_stock_suggestions():
    """Get popular US stock suggestions"""
    return {
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

def create_dark_theme_chart(data, symbol):
    """Create professional dark theme chart with geometric styling"""
    try:
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=(f'{symbol} Price Movement', 'Volume Analysis'),
            row_heights=[0.7, 0.3]
        )
        
        # Candlestick chart with dark theme
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name=symbol,
                increasing_line_color='#30d158',
                decreasing_line_color='#ff453a',
                increasing_fillcolor='#30d158',
                decreasing_fillcolor='#ff453a'
            ),
            row=1, col=1
        )
        
        # Volume chart with matching colors
        colors = ['#ff453a' if close < open else '#30d158' 
                 for close, open in zip(data['Close'], data['Open'])]
        
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.6
            ),
            row=2, col=1
        )
        
        # Update layout for dark theme
        fig.update_layout(
            title={
                'text': f'{symbol} Technical Analysis',
                'font': {'color': '#ffffff', 'size': 20, 'family': 'Inter'},
                'x': 0.5
            },
            plot_bgcolor='#000000',
            paper_bgcolor='#1c1c1e',
            font={'color': '#ffffff', 'family': 'Inter'},
            height=600,
            showlegend=False,
            xaxis_rangeslider_visible=False
        )
        
        # Update axes
        fig.update_xaxes(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='#38383a',
            showline=True,
            linecolor='#38383a',
            color='#8e8e93'
        )
        fig.update_yaxes(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='#38383a',
            showline=True,
            linecolor='#38383a',
            color='#8e8e93'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Chart creation failed: {str(e)}")
        return None

def display_enhanced_financial_analysis(stock_data, av_data, risk_free_rate):
    """Display enhanced financial analysis with dark theme"""
    info = stock_data['info']
    
    st.markdown('<div class="section-header">Financial Overview</div>', unsafe_allow_html=True)
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_price = info.get('currentPrice', 0)
        change_percent = info.get('regularMarketChangePercent', 0)
        delta_color = "normal" if change_percent >= 0 else "inverse"
        st.metric("Current Price", f"${current_price:.2f}", f"{change_percent:.2%}", delta_color=delta_color)
    
    with col2:
        market_cap = info.get('marketCap', 0)
        if market_cap > 1e9:
            st.metric("Market Cap", f"${market_cap/1e9:.1f}B")
        else:
            st.metric("Market Cap", f"${market_cap/1e6:.1f}M")
    
    with col3:
        pe_ratio = info.get('trailingPE', 0)
        st.metric("P/E Ratio", f"{pe_ratio:.2f}" if pe_ratio else "N/A")
    
    with col4:
        beta = info.get('beta', 0)
        st.metric("Beta", f"{beta:.2f}" if beta else "N/A")
    
    # Enhanced metrics if Alpha Vantage data available
    if av_data:
        st.markdown('<div class="section-header">Premium Analytics</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ev_revenue = float(av_data.get('EVToRevenue', 0) or 0)
            st.metric("EV/Revenue", f"{ev_revenue:.2f}" if ev_revenue else "N/A")
        
        with col2:
            price_sales = float(av_data.get('PriceToSalesRatioTTM', 0) or 0)
            st.metric("Price/Sales", f"{price_sales:.2f}" if price_sales else "N/A")
        
        with col3:
            current_ratio = float(av_data.get('CurrentRatio', 0) or 0)
            st.metric("Current Ratio", f"{current_ratio:.2f}" if current_ratio else "N/A")
        
        with col4:
            target_price = float(av_data.get('AnalystTargetPrice', 0) or 0)
            if target_price > 0 and current_price > 0:
                upside = ((target_price / current_price) - 1) * 100
                delta_color = "normal" if upside >= 0 else "inverse"
                st.metric("Analyst Target", f"${target_price:.2f}", f"{upside:+.1f}%", delta_color=delta_color)
            else:
                st.metric("Analyst Target", "N/A")

def display_company_profile(info):
    """Display company profile with clean design"""
    st.markdown('<div class="section-header">Company Profile</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Company Name:** {info.get('longName', 'N/A')}")
        st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
        st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
        st.markdown(f"**Country:** {info.get('country', 'N/A')}")
    
    with col2:
        employees = info.get('fullTimeEmployees', 0)
        if employees:
            st.markdown(f"**Employees:** {employees:,}")
        st.markdown(f"**Website:** {info.get('website', 'N/A')}")
        st.markdown(f"**Exchange:** {info.get('exchange', 'N/A')}")
    
    # Business summary
    summary = info.get('longBusinessSummary', '')
    if summary:
        st.markdown("**Business Summary**")
        st.markdown(summary[:400] + "..." if len(summary) > 400 else summary)

def display_news_analysis(news_articles, symbol):
    """Display news analysis with clean layout"""
    if not news_articles:
        st.warning("No recent news available. Add NEWS_API_KEY to .env file for news analysis.")
        return
    
    st.markdown(f'<div class="section-header">Recent News - {symbol}</div>', unsafe_allow_html=True)
    
    for i, article in enumerate(news_articles[:6]):
        with st.expander(f"📰 {article.get('title', 'No title')}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Description:** {article.get('description', 'No description available')}")
                st.markdown(f"**Source:** {article.get('source', {}).get('name', 'Unknown')}")
                
            with col2:
                published_at = article.get('publishedAt', '')
                if published_at:
                    try:
                        date_obj = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                        st.markdown(f"**Published:** {date_obj.strftime('%Y-%m-%d %H:%M')}")
                    except:
                        st.markdown(f"**Published:** {published_at}")
                
                if article.get('url'):
                    st.markdown(f"[Read More]({article['url']})")

def display_technical_analysis(stock_data):
    """Display technical analysis indicators"""
    st.markdown('<div class="section-header">Technical Analysis</div>', unsafe_allow_html=True)
    
    if not stock_data['historical'].empty:
        hist = stock_data['historical']
        
        # Calculate technical indicators
        sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
        sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
        current_price = hist['Close'].iloc[-1]
        
        # Calculate RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Price", f"${current_price:.2f}")
            
        with col2:
            sma_20_diff = ((current_price / sma_20) - 1) * 100 if not pd.isna(sma_20) else 0
            delta_color = "normal" if sma_20_diff >= 0 else "inverse"
            st.metric("20-Day SMA", f"${sma_20:.2f}" if not pd.isna(sma_20) else "N/A", 
                     f"{sma_20_diff:+.1f}%" if not pd.isna(sma_20) else None, delta_color=delta_color)
            
        with col3:
            sma_50_diff = ((current_price / sma_50) - 1) * 100 if not pd.isna(sma_50) else 0
            delta_color = "normal" if sma_50_diff >= 0 else "inverse"
            st.metric("50-Day SMA", f"${sma_50:.2f}" if not pd.isna(sma_50) else "N/A",
                     f"{sma_50_diff:+.1f}%" if not pd.isna(sma_50) else None, delta_color=delta_color)
            
        with col4:
            rsi_color = "normal" if 30 <= rsi <= 70 else ("inverse" if rsi > 70 else "off")
            st.metric("RSI (14)", f"{rsi:.1f}" if not pd.isna(rsi) else "N/A", 
                     "Overbought" if rsi > 70 else ("Oversold" if rsi < 30 else "Neutral"), 
                     delta_color=rsi_color)

def main():
    """Main application function"""
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">Professional Stock Analytics</div>
        <div class="main-subtitle">Enterprise Financial Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.markdown('<div class="section-header">Configuration</div>', unsafe_allow_html=True)
    
    # Stock selection mode
    analysis_mode = st.sidebar.radio(
        "Analysis Mode",
        ["Popular Stocks", "Custom Symbol"],
        help="Choose analysis approach"
    )
    
    # Stock symbol selection
    st.sidebar.markdown('<div class="section-header">Stock Selection</div>', unsafe_allow_html=True)
    
    if analysis_mode == "Popular Stocks":
        us_stocks = get_us_stock_suggestions()
        selected_stock = st.sidebar.selectbox(
            "Select Stock",
            list(us_stocks.keys()),
            help="S&P 500 and NASDAQ leaders"
        )
        symbol = us_stocks[selected_stock]
        st.sidebar.code(symbol)
        
    else:  # Custom Symbol
        symbol = st.sidebar.text_input(
            "Enter Symbol",
            value="AAPL",
            help="Enter any valid ticker (e.g., AAPL, MSFT, GOOGL)"
        ).upper()
    
    # Time period selection
    st.sidebar.markdown('<div class="section-header">Timeframe</div>', unsafe_allow_html=True)
    period = st.sidebar.selectbox(
        "Analysis Period",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3,
        help="Historical data analysis window"
    )
    
    # Analysis execution
    st.sidebar.markdown('<div class="section-header">Execution</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("Execute Analysis", type="primary"):
        if symbol:
            # Initialize progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Fetching stock data...")
            progress_bar.progress(20)
            
            stock_data = get_stock_data(symbol, period)
            
            if stock_data['success']:
                progress_bar.progress(40)
                status_text.text("Gathering market intelligence...")
                
                # Get enhanced data
                info = stock_data['info']
                risk_free_rate = fetch_risk_free_rate()
                av_data = fetch_alpha_vantage_fundamentals(symbol)
                news_articles = fetch_company_news(symbol)
                
                progress_bar.progress(70)
                status_text.text("Processing AI analysis...")
                
                # API Status Dashboard
                st.markdown('<div class="section-header">API Status Dashboard</div>', unsafe_allow_html=True)
                api_col1, api_col2, api_col3, api_col4 = st.columns(4)
                
                with api_col1:
                    st.metric("Yahoo Finance", "Active", "Free Tier")
                    
                with api_col2:
                    if os.getenv('GROQ_API_KEY'):
                        st.metric("Groq AI", "Active", "Enhanced Analysis")
                    else:
                        st.metric("Groq AI", "Inactive", "API Key Required")
                        
                with api_col3:
                    if av_data:
                        st.metric("Alpha Vantage", "Active", "Premium Data")
                    else:
                        st.metric("Alpha Vantage", "Inactive", "API Key Required")
                        
                with api_col4:
                    if news_articles:
                        st.metric("NewsAPI", "Active", "Market Sentiment")
                    else:
                        st.metric("NewsAPI", "Inactive", "API Key Required")
                
                progress_bar.progress(90)
                status_text.text("Finalizing analysis...")
                
                # Create tabs with clean design
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                    "Enhanced Analysis", 
                    "Financial Health", 
                    "Technical Indicators",
                    "News & Sentiment",
                    "AI Investment Analysis",
                    "Company Profile"
                ])
                
                with tab1:
                    display_enhanced_financial_analysis(stock_data, av_data, risk_free_rate)
                
                with tab2:
                    # Financial Health Display
                    st.markdown('<div class="section-header">Financial Health</div>', unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        revenue = info.get('totalRevenue', 0)
                        if revenue:
                            st.metric("Revenue (TTM)", f"${revenue/1e9:.1f}B")
                        else:
                            st.metric("Revenue (TTM)", "N/A")
                            
                        gross_profit = info.get('grossProfits', 0)
                        if gross_profit:
                            st.metric("Gross Profit", f"${gross_profit/1e9:.1f}B")
                        else:
                            st.metric("Gross Profit", "N/A")
                        
                    with col2:
                        operating_margin = info.get('operatingMargins', 0)
                        st.metric("Operating Margin", f"{operating_margin:.2%}" if operating_margin else "N/A")
                        
                        profit_margin = info.get('profitMargins', 0)
                        st.metric("Profit Margin", f"{profit_margin:.2%}" if profit_margin else "N/A")
                        
                    with col3:
                        roe = info.get('returnOnEquity', 0)
                        st.metric("ROE", f"{roe:.2%}" if roe else "N/A")
                        
                        debt_equity = info.get('debtToEquity', 0)
                        st.metric("Debt to Equity", f"{debt_equity:.2f}" if debt_equity else "N/A")
                
                with tab3:
                    display_technical_analysis(stock_data)
                
                with tab4:
                    display_news_analysis(news_articles, symbol)
                
                with tab5:
                    # AI Analysis
                    if os.getenv('GROQ_API_KEY'):
                        try:
                            enhanced_metrics = get_enhanced_financial_metrics(stock_data, av_data, risk_free_rate)
                            analysis = create_enhanced_ai_analysis(symbol, enhanced_metrics, news_articles)
                            
                            if analysis:
                                st.markdown('<div class="ai-analysis">', unsafe_allow_html=True)
                                st.markdown("### AI Investment Analysis")
                                st.markdown(analysis)
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                if news_articles:
                                    with st.expander("News Context Used in Analysis"):
                                        for article in news_articles[:5]:
                                            st.markdown(f"- {article.get('title', '')}")
                                        
                        except Exception as e:
                            st.error(f"AI Analysis failed: {str(e)}")
                            st.info("Tip: Check your GROQ_API_KEY in .env file")
                    else:
                        st.warning("Add GROQ_API_KEY to .env file to enable AI analysis")
                        st.info("Get your free API key from: https://console.groq.com")
                        
                with tab6:
                    display_company_profile(info)
                    
                    # Show Alpha Vantage enhancements if available
                    if av_data:
                        st.markdown('<div class="section-header">Enhanced Company Data</div>', unsafe_allow_html=True)
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            description = av_data.get('Description', 'N/A')
                            if description and description != 'N/A':
                                st.markdown(f"**Description:** {description[:200]}...")
                            st.markdown(f"**Address:** {av_data.get('Address', 'N/A')}")
                            
                        with col2:
                            st.markdown(f"**Fiscal Year End:** {av_data.get('FiscalYearEnd', 'N/A')}")
                            st.markdown(f"**Latest Quarter:** {av_data.get('LatestQuarter', 'N/A')}")
                
                # Chart section
                if not stock_data['historical'].empty:
                    st.markdown('<div class="section-header">Technical Chart Analysis</div>', unsafe_allow_html=True)
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    fig = create_dark_theme_chart(stock_data['historical'], symbol)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)
                
                progress_bar.progress(100)
                status_text.text("Analysis complete")
                
            else:
                st.error(f"Failed to fetch data for {symbol}")
                progress_bar.empty()
                status_text.empty()
        else:
            st.sidebar.error("Please enter a trading symbol")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-title">Professional Trading Analytics</div>
        <div class="footer-subtitle">Multi-Source Financial Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
