# Professional Stock Market Analysis AI Agent with Enhanced APIs
# Comprehensive financial intelligence platform with multiple data sources

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
    page_title="🚀 Professional Stock Analytics | Trading Intelligence Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .ai-analysis {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #e17055;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .info-section {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .info-title {
        font-weight: 600;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    code {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
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
            news_context = "Recent News Headlines:\n"
            for article in news_articles[:5]:
                news_context += f"- {article.get('title', '')}\n"
        
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

def create_enhanced_financial_analysis_tab(stock_data, av_data, risk_free_rate):
    """Create enhanced financial analysis tab with all data sources"""
    info = stock_data['info']
    
    st.markdown("### 📊 **Enhanced Financial Overview**")
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Price", f"${info.get('currentPrice', 0):.2f}", 
                 f"{info.get('regularMarketChangePercent', 0):.2%}")
    
    with col2:
        market_cap = info.get('marketCap', 0)
        if market_cap > 1e9:
            st.metric("Market Cap", f"${market_cap/1e9:.1f}B")
        else:
            st.metric("Market Cap", f"${market_cap/1e6:.1f}M")
    
    with col3:
        st.metric("P/E Ratio", f"{info.get('trailingPE', 0):.2f}")
    
    with col4:
        st.metric("Beta", f"{info.get('beta', 0):.2f}")
    
    # Enhanced metrics if Alpha Vantage data available
    if av_data:
        st.markdown("### 🚀 **Premium Analytics (Alpha Vantage)**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("EV/Revenue", f"{float(av_data.get('EVToRevenue', 0) or 0):.2f}")
        
        with col2:
            st.metric("Price/Sales", f"{float(av_data.get('PriceToSalesRatioTTM', 0) or 0):.2f}")
        
        with col3:
            st.metric("Current Ratio", f"{float(av_data.get('CurrentRatio', 0) or 0):.2f}")
        
        with col4:
            target_price = float(av_data.get('AnalystTargetPrice', 0) or 0)
            current_price = info.get('currentPrice', 0)
            if target_price > 0 and current_price > 0:
                upside = ((target_price / current_price) - 1) * 100
                st.metric("Analyst Target", f"${target_price:.2f}", f"{upside:+.1f}%")
            else:
                st.metric("Analyst Target", "N/A")

def create_news_analysis_tab(news_articles, symbol):
    """Create news and sentiment analysis tab"""
    if not news_articles:
        st.warning("📰 No recent news available. Add NEWS_API_KEY to .env file for news analysis.")
        st.info("Get your free API key from: https://newsapi.org")
        return
    
    st.markdown(f"### 📰 **Recent News for {symbol}**")
    
    for i, article in enumerate(news_articles[:8]):
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

# Existing functions (simplified versions of the previous implementation)
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

def create_professional_chart(data, symbol):
    """Create professional candlestick chart with technical indicators"""
    try:
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=(f'{symbol} Price Chart', 'Volume'),
            row_width=[0.7, 0.3]
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name=symbol,
                increasing_line_color='#00ff88',
                decreasing_line_color='#ff4444'
            ),
            row=1, col=1
        )
        
        # Volume chart
        colors = ['#ff4444' if close < open else '#00ff88' 
                 for close, open in zip(data['Close'], data['Open'])]
        
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.7
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f'{symbol} Technical Analysis',
            yaxis_title='Price ($)',
            xaxis_title='Date',
            height=600,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        
        return fig
        
    except Exception as e:
        st.error(f"Chart creation failed: {str(e)}")
        return None

def display_company_profile(info):
    """Display enhanced company profile"""
    st.markdown("### 🏢 **Company Profile**")
    
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
        st.markdown("### 📝 **Business Summary**")
        st.markdown(summary[:500] + "..." if len(summary) > 500 else summary)

def display_financial_health(stock_data):
    """Display financial health metrics"""
    info = stock_data['info']
    
    st.markdown("### 💰 **Financial Health Metrics**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Revenue (TTM)", f"${info.get('totalRevenue', 0)/1e9:.1f}B" if info.get('totalRevenue') else "N/A")
        st.metric("Gross Profit", f"${info.get('grossProfits', 0)/1e9:.1f}B" if info.get('grossProfits') else "N/A")
        
    with col2:
        st.metric("Operating Margin", f"{info.get('operatingMargins', 0):.2%}" if info.get('operatingMargins') else "N/A")
        st.metric("Profit Margin", f"{info.get('profitMargins', 0):.2%}" if info.get('profitMargins') else "N/A")
        
    with col3:
        st.metric("ROE", f"{info.get('returnOnEquity', 0):.2%}" if info.get('returnOnEquity') else "N/A")
        st.metric("Debt to Equity", f"{info.get('debtToEquity', 0):.2f}" if info.get('debtToEquity') else "N/A")

def display_technical_analysis(technical, historical):
    """Display technical analysis indicators"""
    st.markdown("### 📈 **Technical Analysis**")
    
    if not historical.empty:
        # Calculate simple technical indicators
        sma_20 = historical['Close'].rolling(window=20).mean().iloc[-1]
        sma_50 = historical['Close'].rolling(window=50).mean().iloc[-1]
        current_price = historical['Close'].iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Price", f"${current_price:.2f}")
            
        with col2:
            st.metric("20-Day SMA", f"${sma_20:.2f}" if not pd.isna(sma_20) else "N/A")
            
        with col3:
            st.metric("50-Day SMA", f"${sma_50:.2f}" if not pd.isna(sma_50) else "N/A")

def main():
    """Main application function"""
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🚀 PROFESSIONAL STOCK ANALYTICS</div>
        <div class="main-subtitle">Advanced Financial Intelligence Platform | Powered by Multi-Source APIs</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.markdown('<div class="section-header">⚙️ CONFIGURATION</div>', unsafe_allow_html=True)
    
    # Stock selection mode
    analysis_mode = st.sidebar.radio(
        "📊 Analysis Mode",
        ["🎯 Popular Stocks", "🔍 Custom Symbol"],
        help="Choose analysis approach"
    )
    
    # Stock symbol selection
    st.sidebar.markdown('<div class="section-header">📈 STOCK SELECTION</div>', unsafe_allow_html=True)
    
    if analysis_mode == "🎯 Popular Stocks":
        us_stocks = get_us_stock_suggestions()
        selected_stock = st.sidebar.selectbox(
            "🔥 Select Popular Stock",
            list(us_stocks.keys()),
            help="S&P 500 and NASDAQ leaders"
        )
        symbol = us_stocks[selected_stock]
        st.sidebar.markdown(f'<div class="info-section"><div class="info-title">Trading Symbol</div><code>{symbol}</code></div>', unsafe_allow_html=True)
        
    else:  # Custom Symbol
        symbol = st.sidebar.text_input(
            "🎯 Enter Trading Symbol",
            value="AAPL",
            help="Enter any valid ticker (e.g., AAPL, MSFT, GOOGL)"
        ).upper()
    
    # Time period selection
    st.sidebar.markdown('<div class="section-header">⏱ TIMEFRAME</div>', unsafe_allow_html=True)
    period = st.sidebar.selectbox(
        "📅 Analysis Period",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3,
        help="Historical data analysis window"
    )
    
    # Analysis execution
    st.sidebar.markdown('<div class="section-header">🚀 EXECUTION</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🚀 EXECUTE COMPREHENSIVE ANALYSIS", type="primary"):
        if symbol:
            # Initialize progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔍 Fetching stock data...")
            progress_bar.progress(20)
            
            stock_data = get_stock_data(symbol, period)
            
            if stock_data['success']:
                progress_bar.progress(40)
                status_text.text("📊 Gathering market intelligence...")
                
                # Get enhanced data
                info = stock_data['info']
                risk_free_rate = fetch_risk_free_rate()
                av_data = fetch_alpha_vantage_fundamentals(symbol)
                news_articles = fetch_company_news(symbol)
                
                progress_bar.progress(70)
                status_text.text("🧠 Processing AI analysis...")
                
                # API Status Dashboard
                st.markdown('<div class="section-header">🔗 API STATUS DASHBOARD</div>', unsafe_allow_html=True)
                api_col1, api_col2, api_col3, api_col4 = st.columns(4)
                
                with api_col1:
                    st.metric("📈 Yahoo Finance", "✅ Active", delta="Free Tier")
                    
                with api_col2:
                    if os.getenv('GROQ_API_KEY'):
                        st.metric("🧠 Groq AI", "✅ Active", delta="Enhanced Analysis")
                    else:
                        st.metric("🧠 Groq AI", "❌ Inactive", delta="API Key Required")
                        
                with api_col3:
                    if av_data:
                        st.metric("📊 Alpha Vantage", "✅ Active", delta="Premium Data")
                    else:
                        st.metric("📊 Alpha Vantage", "❌ Inactive", delta="API Key Required")
                        
                with api_col4:
                    if news_articles:
                        st.metric("📰 NewsAPI", "✅ Active", delta="Market Sentiment")
                    else:
                        st.metric("📰 NewsAPI", "❌ Inactive", delta="API Key Required")
                
                progress_bar.progress(90)
                status_text.text("🎯 Finalizing comprehensive analysis...")
                
                # Create enhanced tabs
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                    "📊 Enhanced Analysis", 
                    "💰 Financial Health", 
                    "📈 Technical Indicators",
                    "📰 News & Sentiment",
                    "🧠 AI Investment Analysis",
                    "🏢 Company Profile"
                ])
                
                with tab1:
                    create_enhanced_financial_analysis_tab(stock_data, av_data, risk_free_rate)
                
                with tab2:
                    display_financial_health(stock_data)
                
                with tab3:
                    display_technical_analysis({}, stock_data['historical'])
                
                with tab4:
                    create_news_analysis_tab(news_articles, symbol)
                
                with tab5:
                    # Enhanced AI Analysis
                    if os.getenv('GROQ_API_KEY'):
                        try:
                            # Get enhanced metrics for AI analysis
                            enhanced_metrics = get_enhanced_financial_metrics(stock_data, av_data, risk_free_rate)
                            
                            # Generate comprehensive AI analysis
                            analysis = create_enhanced_ai_analysis(symbol, enhanced_metrics, news_articles)
                            
                            if analysis:
                                st.markdown('<div class="ai-analysis">', unsafe_allow_html=True)
                                st.markdown("### 🧠 **AI Investment Analysis**")
                                st.markdown(analysis)
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                # Show news context if available
                                if news_articles:
                                    with st.expander("📰 News Context Used in Analysis"):
                                        for article in news_articles[:5]:
                                            st.markdown(f"- {article.get('title', '')}")
                                        
                        except Exception as e:
                            st.error(f"❌ AI Analysis failed: {str(e)}")
                            st.info("💡 Tip: Check your GROQ_API_KEY in .env file")
                    else:
                        st.warning("🔑 Add GROQ_API_KEY to .env file to enable AI analysis")
                        st.info("Get your free API key from: https://console.groq.com")
                        
                with tab6:
                    display_company_profile(info)
                    
                    # Show Alpha Vantage enhancements if available
                    if av_data:
                        st.markdown("### 📊 **Enhanced Company Data (Alpha Vantage)**")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            description = av_data.get('Description', 'N/A')
                            if description and description != 'N/A':
                                st.markdown(f"**Description:** {description[:200]}...")
                            st.markdown(f"**Address:** {av_data.get('Address', 'N/A')}")
                            
                        with col2:
                            st.markdown(f"**Fiscal Year End:** {av_data.get('FiscalYearEnd', 'N/A')}")
                            st.markdown(f"**Latest Quarter:** {av_data.get('LatestQuarter', 'N/A')}")
                
                # Enhanced chart section
                if not stock_data['historical'].empty:
                    st.markdown('<div class="section-header">📊 TECHNICAL CHART ANALYSIS</div>', unsafe_allow_html=True)
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    fig = create_professional_chart(stock_data['historical'], symbol)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
            else:
                st.error(f"❌ Failed to fetch data for {symbol}")
                progress_bar.empty()
                status_text.empty()
        else:
            st.sidebar.error("⚠️ Please enter a trading symbol")
    
    # Professional footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 10px; margin-top: 2rem;">
        <div style="color: #00d4ff; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
            🚀 PROFESSIONAL TRADING ANALYTICS | Multi-Source Financial Intelligence
        </div>
        <div style="color: #b0b0b0; font-size: 0.9rem;">
            Powered by Yahoo Finance, Alpha Vantage, NewsAPI, FRED & Groq AI | Enterprise-Grade Analysis Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
