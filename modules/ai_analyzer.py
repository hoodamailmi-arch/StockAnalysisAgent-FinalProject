# AI Analysis Module
# Handles AI-powered investment analysis using Groq API with model fallback

from groq import Groq
import streamlit as st
import time
from .config import APIConfig


class AIAnalyzer:
    """AI-powered financial analysis using Groq API with model fallback handling"""
    
    # Current Groq models (updated September 2025)
    PRIMARY_MODELS = [
        "llama-3.3-70b-versatile",      # Latest Llama model
        "llama-3.1-70b-versatile",     # Backup if 3.3 not available
        "mixtral-8x7b-32768",          # Mixtral for complex analysis
        "llama-3.1-8b-instant",       # Fast model for quick analysis
    ]
    
    def __init__(self):
        self.client = None
        self.current_model = None
        if APIConfig.GROQ_API_KEY:
            try:
                self.client = Groq(api_key=APIConfig.GROQ_API_KEY)
                self._validate_models()
            except Exception as e:
                print(f"Groq client initialization failed: {e}")
    
    def _validate_models(self):
        """Test which models are currently available"""
        for model in self.PRIMARY_MODELS:
            try:
                # Test with a simple prompt
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=10,
                    timeout=5
                )
                self.current_model = model
                print(f"✅ Using Groq model: {model}")
                break
            except Exception as e:
                print(f"❌ Model {model} unavailable: {str(e)[:50]}...")
                continue
        
        if not self.current_model:
            print("⚠️ No Groq models are currently available")
    
    def is_available(self):
        """Check if AI analysis is available"""
        return bool(self.client and self.current_model)
    
    def create_enhanced_ai_analysis(self, symbol, enhanced_metrics, news_articles):
        """Generate comprehensive AI analysis using enhanced data with model fallback"""
        if not self.client:
            return "❌ AI Analysis unavailable. Please add GROQ_API_KEY to .env file."
        
        if not self.current_model:
            return "❌ No Groq models are currently available. Please try again later."
        
        try:
            # Prepare comprehensive context
            financial_context = self._build_financial_context(symbol, enhanced_metrics)
            news_context = self._build_news_context(news_articles)
            
            prompt = self._build_institutional_prompt(symbol, financial_context, news_context)
            
            # Use current working model with retry logic
            return self._generate_with_retry(prompt)
            
        except Exception as e:
            return f"❌ AI Analysis Error: {str(e)}"
    
    def _generate_with_retry(self, prompt, max_retries=3):
        """Generate response with retry logic and model fallback"""
        
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.current_model,
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a senior equity research analyst at Goldman Sachs with 15+ years of experience in fundamental analysis and institutional investing."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    temperature=0.1,  # Low temperature for consistent analysis
                    max_tokens=2000,
                    top_p=0.9,
                    stream=False
                )
                
                return completion.choices[0].message.content
                
            except Exception as e:
                error_msg = str(e)
                
                # Handle model decommissioned error
                if "decommissioned" in error_msg or "model_decommissioned" in error_msg:
                    print(f"Model {self.current_model} decommissioned, trying next model...")
                    
                    # Try next available model
                    try:
                        current_index = self.PRIMARY_MODELS.index(self.current_model)
                        if current_index + 1 < len(self.PRIMARY_MODELS):
                            self.current_model = self.PRIMARY_MODELS[current_index + 1]
                            print(f"Switching to model: {self.current_model}")
                            continue
                    except ValueError:
                        pass
                    
                    return "❌ All Groq models are currently unavailable. Please try again later."
                
                # Handle rate limiting
                elif "rate_limit" in error_msg:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Rate limited, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                
                # Other errors
                else:
                    if attempt == max_retries - 1:
                        return f"❌ AI Analysis failed after {max_retries} attempts: {error_msg}"
                    time.sleep(1)
                    continue
        
        return "❌ AI Analysis temporarily unavailable. Please try again."
    
    def _build_financial_context(self, symbol, enhanced_metrics):
        """Build financial context string for AI prompt"""
        return f"""
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
    
    def _build_news_context(self, news_articles):
        """Build news context string for AI prompt"""
        if not news_articles:
            return ""
        
        news_context = "Recent News Headlines:\\n"
        for article in news_articles[:5]:
            news_context += f"- {article.get('title', '')}\\n"
        
        return news_context
    
    def _build_institutional_prompt(self, symbol, financial_context, news_context):
        """Build institutional-grade investment memo prompt"""
        return f"""
**INSTITUTIONAL INVESTMENT MEMO - {symbol}**

You are preparing a comprehensive investment analysis for institutional investors.

**FINANCIAL SNAPSHOT:**
{financial_context}

**MARKET CONTEXT:**
{news_context}

**REQUIRED ANALYSIS STRUCTURE:**

**1. EXECUTIVE SUMMARY & INVESTMENT THESIS**
Provide a clear recommendation (BUY/HOLD/SELL) with 2-3 sentence investment thesis.

**2. FUNDAMENTAL ANALYSIS**
• **Profitability & Efficiency:** Analyze ROE, profit margins, and operational efficiency
• **Valuation Assessment:** Is the stock fairly valued vs peers and intrinsic value?
• **Balance Sheet Strength:** Evaluate debt levels, liquidity, and financial resilience

**3. STRATEGIC ANALYSIS**
• **Competitive Position:** Assess market position and competitive advantages
• **Growth Prospects:** Revenue growth sustainability and expansion opportunities
• **Management Quality:** Capital allocation effectiveness and strategic execution

**4. RISK ASSESSMENT**
• **Top 3 Bull Case Factors:** Key drivers for outperformance
• **Top 3 Bear Case Factors:** Primary risks and headwinds
• **Volatility & Beta Analysis:** Risk-adjusted return expectations

**5. FINAL RECOMMENDATION**
• **Investment Rating:** BUY/HOLD/SELL with conviction level
• **Price Target:** 12-month target with upside/downside potential
• **Key Catalysts:** Near-term drivers that could move the stock

Provide specific, actionable insights with institutional-grade analysis depth.
        """
    
    def get_quick_sentiment(self, symbol, news_headlines):
        """Generate quick sentiment analysis for news headlines"""
        if not self.is_available() or not news_headlines:
            return "Neutral - No analysis available"
        
        headlines_text = "\n".join(f"• {headline}" for headline in news_headlines[:5])
        
        prompt = f"""
Analyze the sentiment of these recent news headlines for {symbol}:

{headlines_text}

Provide a one-sentence sentiment summary (Bullish/Bearish/Neutral) with key reasoning.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.current_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=100,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Sentiment analysis error: {str(e)}"
    
    def get_model_status(self):
        """Get current model status and availability"""
        return {
            "current_model": self.current_model,
            "available_models": self.PRIMARY_MODELS,
            "api_key_configured": bool(APIConfig.GROQ_API_KEY),
            "client_initialized": bool(self.client),
            "is_available": self.is_available()
        }
