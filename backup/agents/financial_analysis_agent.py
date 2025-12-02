from groq import Groq
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
from config.settings import settings

# Robust logging setup
try:
    from loguru import logger
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class FinancialAnalysisAgent:
    """AI Agent for comprehensive financial analysis using Groq LLM"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.DEFAULT_MODEL
        
    async def generate_investment_memo(self, 
                                     company_data: Dict[str, Any],
                                     financial_data: Dict[str, Any],
                                     market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive investment memo following institutional standards
        """
        
        # Prepare context for the LLM
        context = self._prepare_analysis_context(company_data, financial_data, market_data)
        
        prompt = self._create_investment_memo_prompt(context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "symbol": company_data.get("symbol", ""),
                "company_name": company_data.get("company_name", ""),
                "analysis_date": datetime.now().isoformat(),
                "investment_memo": analysis,
                "data_sources": ["Yahoo Finance", "Alpha Vantage", "FRED"],
                "model_used": self.model
            }
            
        except Exception as e:
            logger.error(f"Error generating investment memo: {str(e)}")
            return {"error": str(e)}
    
    def _get_system_prompt(self) -> str:
        """System prompt defining the AI agent's role and expertise"""
        return """
        You are a senior investment analyst with 15+ years of experience at top-tier global investment firms 
        (BlackRock, Goldman Sachs Asset Management). You have deep expertise in:
        
        - Advanced financial analysis and valuation models
        - Competitive strategy frameworks (Porter's Five Forces, SWOT, moat analysis)
        - Macroeconomic and geopolitical risk assessment
        - Impact of disruptive technologies, particularly AI, across industry sectors
        - Institutional-grade investment research and memo writing
        
        Your analysis must be:
        - Precise to every decimal point in financial calculations
        - Data-driven with institutional rigor
        - Professional and suitable for institutional investors
        - Critical and unbiased, highlighting both opportunities and risks
        
        Always provide specific numerical analysis, ratios, and forward-looking assessments.
        """
    
    def _create_investment_memo_prompt(self, context: Dict[str, Any]) -> str:
        """Create detailed prompt for investment memo generation"""
        
        return f"""
        Analyze the following company and provide a comprehensive investment memo:
        
        COMPANY DATA:
        {json.dumps(context['company_info'], indent=2)}
        
        FINANCIAL METRICS:
        {json.dumps(context['financial_metrics'], indent=2)}
        
        STOCK PERFORMANCE:
        {json.dumps(context['stock_performance'], indent=2)}
        
        MARKET CONTEXT:
        {json.dumps(context['market_context'], indent=2)}
        
        Please structure your analysis as follows:
        
        1. EXECUTIVE SUMMARY & INVESTMENT THESIS
           - Investment recommendation (Strong Buy/Buy/Hold/Sell/Strong Sell)
           - Target price with 12-month horizon
           - Core investment thesis in 2-3 sentences
           - Key risk/reward assessment
        
        2. FUNDAMENTAL ANALYSIS
           - Profitability Analysis: Calculate and analyze ROIC, ROE, Operating Margin, FCF conversion
           - Valuation Analysis: Apply DCF, P/E, EV/EBITDA, P/S ratios vs. sector peers
           - Balance Sheet Health: Debt/EBITDA, Current Ratio, Cash position analysis
           - Quality of Earnings: Assess revenue quality, one-time items, cash conversion
        
        3. COMPETITIVE & STRATEGIC ANALYSIS
           - Economic Moat Assessment: Analyze competitive advantages and durability
           - Porter's Five Forces: Industry structure and competitive dynamics
           - Market Position: Market share, competitive positioning, differentiation
           - AI Impact Analysis: How AI affects this company's business model and competitive position
        
        4. MANAGEMENT & GOVERNANCE
           - Capital Allocation Track Record: ROIC trends, dividend/buyback policy
           - Executive Compensation Alignment: Pay-for-performance analysis
           - Strategic Vision: Management's strategic initiatives and execution capability
        
        5. MACRO & GEOPOLITICAL OVERLAY
           - Secular Trends Exposure: Positioning within major industry trends
           - Geographic Revenue Diversification: Exposure to different regions/currencies
           - Geopolitical Risk Assessment: Trade tensions, regulatory risks, supply chain
           - ESG Considerations: Environmental, social, governance risks and opportunities
        
        6. RISK ASSESSMENT
           - Bull Case (3 scenarios): Best-case drivers and potential upside
           - Bear Case (3 scenarios): Key risks and potential downside
           - Base Case Probability: Most likely outcome with supporting rationale
        
        7. CATALYSTS & RECOMMENDATION
           - Near-term Catalysts (0-6 months): Earnings, product launches, regulatory decisions
           - Long-term Catalysts (6-24 months): Strategic initiatives, market expansion
           - Price Target Methodology: Detailed valuation approach and assumptions
           - Final Recommendation: Reiterate stance with conviction level
        
        CRITICAL REQUIREMENTS:
        - All financial calculations must be precise to 2 decimal places
        - Include specific numerical ranges for all valuations
        - Provide quantitative risk/reward ratios
        - Compare all metrics to sector and market averages
        - Be critical and objective - don't shy away from negative analysis
        """
    
    def _prepare_analysis_context(self, 
                                company_data: Dict[str, Any],
                                financial_data: Dict[str, Any],
                                market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare structured context for analysis"""
        
        return {
            "company_info": {
                "symbol": company_data.get("symbol", ""),
                "name": company_data.get("company_name", ""),
                "sector": company_data.get("sector", ""),
                "industry": company_data.get("industry", ""),
                "market_cap": company_data.get("market_cap", 0),
                "employees": company_data.get("employees", 0)
            },
            "financial_metrics": {
                "valuation": {
                    "pe_ratio": financial_data.get("pe_ratio", 0),
                    "forward_pe": financial_data.get("forward_pe", 0),
                    "peg_ratio": financial_data.get("peg_ratio", 0),
                    "price_to_book": financial_data.get("price_to_book", 0),
                    "price_to_sales": financial_data.get("price_to_sales", 0),
                    "ev_to_ebitda": financial_data.get("ev_to_ebitda", 0)
                },
                "profitability": {
                    "profit_margin": financial_data.get("profit_margin", 0),
                    "operating_margin": financial_data.get("operating_margin", 0),
                    "return_on_assets": financial_data.get("return_on_assets", 0),
                    "return_on_equity": financial_data.get("return_on_equity", 0)
                },
                "financial_health": {
                    "current_ratio": financial_data.get("current_ratio", 0),
                    "quick_ratio": financial_data.get("quick_ratio", 0),
                    "debt_to_equity": financial_data.get("debt_to_equity", 0),
                    "total_cash": financial_data.get("total_cash", 0),
                    "total_debt": financial_data.get("total_debt", 0)
                },
                "growth": {
                    "revenue_growth": financial_data.get("revenue_growth", 0),
                    "earnings_growth": financial_data.get("earnings_growth", 0)
                }
            },
            "stock_performance": {
                "current_price": market_data.get("current_price", 0),
                "change_percent": market_data.get("change_percent", 0),
                "52_week_high": financial_data.get("52_week_high", 0),
                "52_week_low": financial_data.get("52_week_low", 0),
                "beta": financial_data.get("beta", 0),
                "volume": market_data.get("volume", 0)
            },
            "market_context": {
                "analysis_date": datetime.now().strftime("%Y-%m-%d"),
                "risk_free_rate": settings.RISK_FREE_RATE,
                "market_return": settings.MARKET_RETURN
            }
        }
    
    async def calculate_dcf_valuation(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate DCF valuation using financial data"""
        
        dcf_prompt = f"""
        Calculate a detailed DCF (Discounted Cash Flow) valuation for a company with the following financials:
        
        {json.dumps(financial_data, indent=2)}
        
        Provide:
        1. 5-year revenue projections with growth assumptions
        2. EBITDA margin projections
        3. Free cash flow calculations for each year
        4. Terminal value calculation using perpetual growth model
        5. WACC calculation and assumptions
        6. Present value calculations
        7. Final intrinsic value per share
        8. Sensitivity analysis for key assumptions
        
        Be specific with all calculations and show your work.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial modeling expert specializing in DCF valuations. Provide detailed, step-by-step calculations."},
                    {"role": "user", "content": dcf_prompt}
                ],
                max_tokens=3000,
                temperature=0.1
            )
            
            return {
                "dcf_analysis": response.choices[0].message.content,
                "model_used": self.model,
                "calculation_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating DCF valuation: {str(e)}")
            return {"error": str(e)}
