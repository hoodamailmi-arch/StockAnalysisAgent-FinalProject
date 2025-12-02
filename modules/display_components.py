# Display Components Module
# Handles all display logic and UI components

import streamlit as st
import pandas as pd
from datetime import datetime
from .config import UIConfig
from .visualizations import UIComponents


class DisplayManager:
    """Manages all display components and layouts"""
    
    @staticmethod
    def display_enhanced_financial_analysis(stock_data, av_data, risk_free_rate):
        """Display enhanced financial analysis with dark theme"""
        info = stock_data['info']
        
        st.markdown(UIComponents.create_section_header("Financial Overview"), unsafe_allow_html=True)
        
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
            st.markdown(UIComponents.create_section_header("Premium Analytics"), unsafe_allow_html=True)
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

    @staticmethod
    def display_financial_health(stock_data):
        """Display financial health metrics"""
        info = stock_data['info']
        
        st.markdown(UIComponents.create_section_header("Financial Health"), unsafe_allow_html=True)
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

    @staticmethod
    def display_technical_analysis(technical_indicators):
        """Display technical analysis indicators"""
        st.markdown(UIComponents.create_section_header("Technical Analysis"), unsafe_allow_html=True)
        
        if not technical_indicators:
            st.warning("No technical data available")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            current_price = technical_indicators.get('current_price', 0)
            st.metric("Current Price", f"${current_price:.2f}")
            
        with col2:
            sma_20 = technical_indicators.get('sma_20', 0)
            sma_20_diff = technical_indicators.get('sma_20_diff', 0)
            delta_color = "normal" if sma_20_diff >= 0 else "inverse"
            st.metric("20-Day SMA", f"${sma_20:.2f}" if not pd.isna(sma_20) else "N/A", 
                     f"{sma_20_diff:+.1f}%" if not pd.isna(sma_20) else None, delta_color=delta_color)
            
        with col3:
            sma_50 = technical_indicators.get('sma_50', 0)
            sma_50_diff = technical_indicators.get('sma_50_diff', 0)
            delta_color = "normal" if sma_50_diff >= 0 else "inverse"
            st.metric("50-Day SMA", f"${sma_50:.2f}" if not pd.isna(sma_50) else "N/A",
                     f"{sma_50_diff:+.1f}%" if not pd.isna(sma_50) else None, delta_color=delta_color)
            
        with col4:
            rsi = technical_indicators.get('rsi', 0)
            rsi_color = "normal" if 30 <= rsi <= 70 else ("inverse" if rsi > 70 else "off")
            st.metric("RSI (14)", f"{rsi:.1f}" if not pd.isna(rsi) else "N/A", 
                     "Overbought" if rsi > 70 else ("Oversold" if rsi < 30 else "Neutral"), 
                     delta_color=rsi_color)

    @staticmethod
    def display_company_profile(info, av_data=None):
        """Display company profile with clean design"""
        st.markdown(UIComponents.create_section_header("Company Profile"), unsafe_allow_html=True)
        
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
        
        # Show Alpha Vantage enhancements if available
        if av_data:
            st.markdown(UIComponents.create_section_header("Enhanced Company Data"), unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                description = av_data.get('Description', 'N/A')
                if description and description != 'N/A':
                    st.markdown(f"**Description:** {description[:200]}...")
                st.markdown(f"**Address:** {av_data.get('Address', 'N/A')}")
                
            with col2:
                st.markdown(f"**Fiscal Year End:** {av_data.get('FiscalYearEnd', 'N/A')}")
                st.markdown(f"**Latest Quarter:** {av_data.get('LatestQuarter', 'N/A')}")

    @staticmethod
    def display_news_analysis(news_articles, symbol):
        """Display news analysis with clean layout"""
        if not news_articles:
            st.warning("No recent news available. Add NEWS_API_KEY to .env file for news analysis.")
            return
        
        st.markdown(UIComponents.create_section_header(f"Recent News - {symbol}"), unsafe_allow_html=True)
        
        for i, article in enumerate(news_articles[:6]):
            with st.expander(f"News: {article.get('title', 'No title')}"):
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

    @staticmethod
    def display_api_status_dashboard(ai_analyzer, av_data, news_articles):
        """Display API status dashboard with AI model info"""
        st.markdown(UIComponents.create_section_header("API Status Dashboard"), unsafe_allow_html=True)
        api_col1, api_col2, api_col3, api_col4 = st.columns(4)
        
        with api_col1:
            st.metric("Yahoo Finance", "Active", "Free Tier")
            
        with api_col2:
            model_status = ai_analyzer.get_model_status()
            if model_status['is_available']:
                model_name = model_status['current_model'].replace('-versatile', '').replace('llama-', 'Llama ').replace('mixtral-', 'Mixtral ')
                st.metric("Groq AI", "Active", model_name)
            else:
                st.metric("Groq AI", "Inactive", "Setup Required")
                
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

    @staticmethod
    def display_ai_analysis(ai_analyzer, symbol, enhanced_metrics, news_articles):
        """Display AI analysis with improved state management"""
        
        # Show model status
        model_status = ai_analyzer.get_model_status()
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.markdown("**AI Model Status**")
            if model_status['is_available']:
                st.success(f"✅ {model_status['current_model']}")
                
                # Show sentiment analysis
                if news_articles:
                    headlines = [article.get('title', '') for article in news_articles[:5]]
                    headlines = [h for h in headlines if h]
                    
                    if headlines:
                        try:
                            sentiment = ai_analyzer.get_quick_sentiment(symbol, headlines)
                            st.markdown("**News Sentiment:**")
                            st.info(sentiment)
                        except:
                            st.markdown("**News Sentiment:**")
                            st.info("Analysis unavailable")
            else:
                if not model_status['api_key_configured']:
                    st.error("❌ No API Key")
                    st.markdown("Add GROQ_API_KEY to .env")
                elif not model_status['current_model']:
                    st.warning("⚠️ No Models Available")
                else:
                    st.error("❌ Connection Failed")
        
        with col1:
            if model_status['is_available']:
                st.markdown("### 🤖 AI Investment Analysis")
                
                # Session state key for this symbol
                analysis_key = f"ai_analysis_{symbol}"
                
                # Initialize session state
                if analysis_key not in st.session_state:
                    st.session_state[analysis_key] = None
                
                # Check if analysis exists
                if st.session_state[analysis_key] is None:
                    st.info("Click below to generate professional AI investment analysis")
                    
                    if st.button("🧠 Generate Professional Analysis", key=f"generate_ai_{symbol}", type="primary"):
                        with st.spinner(f"Generating analysis using {model_status['current_model']}..."):
                            try:
                                analysis = ai_analyzer.create_enhanced_ai_analysis(symbol, enhanced_metrics, news_articles)
                                st.session_state[analysis_key] = {
                                    'analysis': analysis,
                                    'news_articles': news_articles,
                                    'symbol': symbol
                                }
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Analysis failed: {str(e)}")
                else:
                    # Display existing analysis
                    result = st.session_state[analysis_key]
                    analysis = result['analysis']
                    stored_news = result.get('news_articles', [])
                    
                    st.markdown("---")
                    
                    if analysis and not analysis.startswith("❌"):
                        st.markdown(analysis)
                        
                        # Show news sources
                        if stored_news:
                            with st.expander("📰 News Sources Used"):
                                for i, article in enumerate(stored_news[:5], 1):
                                    st.markdown(f"**{i}.** {article.get('title', 'No title')}")
                                    source = article.get('source', {}).get('name', 'Unknown')
                                    st.caption(f"📰 {source}")
                    else:
                        st.error(analysis)
                    
                    # Control buttons
                    col_refresh, col_clear = st.columns(2)
                    with col_refresh:
                        if st.button("🔄 Generate New", key=f"refresh_ai_{symbol}"):
                            st.session_state[analysis_key] = None
                            st.rerun()
                    with col_clear:
                        if st.button("🗑️ Clear Analysis", key=f"clear_ai_{symbol}"):
                            st.session_state[analysis_key] = None
                            st.rerun()
                                
            else:
                st.markdown("### 🔧 Setup Required")
                
                if not model_status['api_key_configured']:
                    st.warning("**AI Analysis requires GROQ_API_KEY**")
                    st.markdown("""
                    **Quick Setup:**
                    1. Get free API key: [Groq Console](https://console.groq.com)
                    2. Add to .env file: `GROQ_API_KEY=your_key_here`
                    3. Restart application
                    """)
                elif not model_status['current_model']:
                    st.warning("**Groq models temporarily unavailable**")
                    st.info("💡 Please try again in a few minutes")
                else:
                    st.error("**Connection failed**")
                    st.info("💡 Check your internet connection and API key")
    
    @staticmethod
    def _show_analysis_result(analysis, news_articles, symbol):
        """Helper method to display analysis results"""
        if analysis and not analysis.startswith("❌"):
            st.markdown("---")
            st.markdown(analysis)
            
            # Show news sources used
            if news_articles:
                with st.expander("📰 News Sources Used"):
                    for i, article in enumerate(news_articles[:5], 1):
                        st.markdown(f"**{i}.** {article.get('title', 'No title')}")
                        source = article.get('source', {}).get('name', 'Unknown')
                        st.caption(f"📰 {source}")
            
            # Control buttons
            col_refresh, col_clear = st.columns(2)
            with col_refresh:
                if st.button("🔄 Generate New Analysis", key=f"refresh_analysis_{symbol}"):
                    analysis_key = f"ai_analysis_{symbol}_result"
                    st.session_state[analysis_key] = None
            
            with col_clear:
                if st.button("�️ Clear Analysis", key=f"clear_analysis_{symbol}"):
                    analysis_key = f"ai_analysis_{symbol}_result"
                    st.session_state[analysis_key] = None
        else:
            st.error(analysis)
            if st.button("� Try Again", key=f"retry_analysis_{symbol}"):
                analysis_key = f"ai_analysis_{symbol}_result"
                st.session_state[analysis_key] = None
