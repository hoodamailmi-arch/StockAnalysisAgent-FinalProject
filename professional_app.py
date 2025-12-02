# Professional Stock Market Analysis Platform - Modular Version
# Enterprise-grade financial intelligence with clean modular architecture

import streamlit as st
import warnings
warnings.filterwarnings('ignore')

# Import modular components
from modules import (
    AppConfig, 
    DataFetcher, 
    MetricsCalculator, 
    AIAnalyzer,
    ChartCreator,
    DisplayManager,
    get_dark_theme_css
)

def setup_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title=AppConfig.PAGE_TITLE,
        page_icon=AppConfig.PAGE_ICON,
        layout=AppConfig.LAYOUT,
        initial_sidebar_state="expanded"
    )

def apply_styling():
    """Apply dark theme CSS styling"""
    st.markdown(get_dark_theme_css(), unsafe_allow_html=True)

def create_header():
    """Create main application header"""
    st.markdown("""
    <div class="main-header">
        <div class="main-title">Professional Stock Analytics</div>
        <div class="main-subtitle">Enterprise Financial Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create and return sidebar configuration"""
    st.sidebar.markdown('<div class="section-header">Configuration</div>', unsafe_allow_html=True)
    
    # Analysis mode selection
    analysis_mode = st.sidebar.radio(
        "Analysis Mode",
        ["Popular Stocks", "Custom Symbol"],
        help="Choose analysis approach"
    )
    
    # Stock symbol selection
    st.sidebar.markdown('<div class="section-header">Stock Selection</div>', unsafe_allow_html=True)
    
    if analysis_mode == "Popular Stocks":
        selected_stock = st.sidebar.selectbox(
            "Select Stock",
            list(AppConfig.POPULAR_STOCKS.keys()),
            help="S&P 500 and NASDAQ leaders"
        )
        symbol = AppConfig.POPULAR_STOCKS[selected_stock]
        st.sidebar.code(symbol)
    else:
        symbol = st.sidebar.text_input(
            "Enter Symbol",
            value=AppConfig.DEFAULT_SYMBOL,
            help="Enter any valid ticker (e.g., AAPL, MSFT, GOOGL)"
        ).upper()
    
    # Time period selection
    st.sidebar.markdown('<div class="section-header">Timeframe</div>', unsafe_allow_html=True)
    period = st.sidebar.selectbox(
        "Analysis Period",
        AppConfig.TIME_PERIODS,
        index=3,
        help="Historical data analysis window"
    )
    
    return symbol, period

def execute_analysis(symbol, period):
    """Execute comprehensive stock analysis"""
    # Initialize progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Fetch stock data
        status_text.text("Fetching stock data...")
        progress_bar.progress(20)
        
        stock_data = DataFetcher.get_stock_data(symbol, period)
        
        if not stock_data['success']:
            st.error(f"Failed to fetch data for {symbol}: {stock_data['error']}")
            return
        
        # Step 2: Gather enhanced data
        progress_bar.progress(40)
        status_text.text("Gathering market intelligence...")
        
        risk_free_rate = DataFetcher.fetch_risk_free_rate()
        av_data = DataFetcher.fetch_alpha_vantage_fundamentals(symbol)
        news_articles = DataFetcher.fetch_company_news(symbol)
        
        # Step 3: Process metrics and indicators
        progress_bar.progress(70)
        status_text.text("Processing analysis...")
        
        enhanced_metrics = MetricsCalculator.get_enhanced_financial_metrics(
            stock_data, av_data, risk_free_rate
        )
        technical_indicators = MetricsCalculator.calculate_technical_indicators(
            stock_data['historical']
        )
        
        # Step 4: Initialize AI analyzer
        ai_analyzer = AIAnalyzer()
        
        progress_bar.progress(90)
        status_text.text("Finalizing analysis...")
        
        # Display API Status Dashboard
        DisplayManager.display_api_status_dashboard(
            ai_analyzer, av_data, news_articles
        )
        
        # Create analysis tabs
        create_analysis_tabs(
            stock_data, av_data, risk_free_rate, enhanced_metrics, 
            technical_indicators, news_articles, ai_analyzer, symbol
        )
        
        # Display chart
        display_chart(stock_data, symbol)
        
        progress_bar.progress(100)
        status_text.text("Analysis complete")
        
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
    finally:
        # Clean up progress indicators
        progress_bar.empty()
        status_text.empty()

def create_analysis_tabs(stock_data, av_data, risk_free_rate, enhanced_metrics, 
                        technical_indicators, news_articles, ai_analyzer, symbol):
    """Create tabbed analysis interface"""
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Enhanced Analysis", 
        "Financial Health", 
        "Technical Indicators",
        "News & Sentiment",
        "AI Investment Analysis",
        "Company Profile"
    ])
    
    with tab1:
        DisplayManager.display_enhanced_financial_analysis(stock_data, av_data, risk_free_rate)
    
    with tab2:
        DisplayManager.display_financial_health(stock_data)
    
    with tab3:
        DisplayManager.display_technical_analysis(technical_indicators)
    
    with tab4:
        DisplayManager.display_news_analysis(news_articles, symbol)
    
    with tab5:
        DisplayManager.display_ai_analysis(ai_analyzer, symbol, enhanced_metrics, news_articles)
    
    with tab6:
        DisplayManager.display_company_profile(stock_data['info'], av_data)

def display_chart(stock_data, symbol):
    """Display technical chart"""
    if not stock_data['historical'].empty:
        st.markdown('<div class="section-header">Technical Chart Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        fig = ChartCreator.create_dark_theme_chart(stock_data['historical'], symbol)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('</div>', unsafe_allow_html=True)

def create_footer():
    """Create application footer"""
    st.markdown("""
    <div class="footer">
        <div class="footer-title">Professional Trading Analytics</div>
        <div class="footer-subtitle">Multi-Source Financial Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function with modular architecture"""
    # Setup and styling
    setup_page()
    apply_styling()
    
    # Create main interface
    create_header()
    
    # Sidebar configuration
    st.sidebar.markdown('<div class="section-header">Execution</div>', unsafe_allow_html=True)
    symbol, period = create_sidebar()
    
    # Analysis execution
    if st.sidebar.button("Execute Analysis", type="primary"):
        if symbol:
            execute_analysis(symbol, period)
        else:
            st.sidebar.error("Please enter a trading symbol")
    
    # Footer
    create_footer()

if __name__ == "__main__":
    main()
