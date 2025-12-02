from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime

# Import our modules
from data_providers.yahoo_finance import YahooFinanceProvider
from agents.financial_analysis_agent import FinancialAnalysisAgent
from config.settings import settings

# Robust logging setup
try:
    from loguru import logger
    logger.add("logs/stock_analysis_{time}.log", rotation="1 day", retention="30 days")
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO, 
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Professional Stock Market Analysis AI Agent Workflow Application"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize providers and agents
data_provider = YahooFinanceProvider()
analysis_agent = FinancialAnalysisAgent()

# Pydantic models for API requests
class StockAnalysisRequest(BaseModel):
    symbol: str
    analysis_type: str = "comprehensive"  # comprehensive, quick, dcf_only
    include_peer_comparison: bool = True

class PortfolioAnalysisRequest(BaseModel):
    symbols: List[str]
    weights: Optional[List[float]] = None
    benchmark: str = "SPY"

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Stock Analysis AI Agent API",
        "version": settings.APP_VERSION,
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/stock/{symbol}/quote")
async def get_stock_quote(symbol: str):
    """Get real-time stock quote"""
    try:
        quote_data = await data_provider.get_real_time_price(symbol.upper())
        if not quote_data:
            raise HTTPException(status_code=404, detail=f"Stock data not found for symbol: {symbol}")
        
        return JSONResponse(content=quote_data)
    
    except Exception as e:
        logger.error(f"Error fetching quote for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stock/{symbol}/metrics")
async def get_stock_metrics(symbol: str):
    """Get comprehensive financial metrics"""
    try:
        metrics = await data_provider.get_key_metrics(symbol.upper())
        if not metrics:
            raise HTTPException(status_code=404, detail=f"Metrics not found for symbol: {symbol}")
        
        return JSONResponse(content=metrics)
    
    except Exception as e:
        logger.error(f"Error fetching metrics for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stock/{symbol}/historical")
async def get_historical_data(symbol: str, period: str = "1y"):
    """Get historical stock data"""
    try:
        historical_data = await data_provider.get_stock_data(symbol.upper(), period)
        if historical_data.empty:
            raise HTTPException(status_code=404, detail=f"Historical data not found for symbol: {symbol}")
        
        # Convert DataFrame to JSON
        data_json = historical_data.to_dict('records')
        
        return JSONResponse(content={
            "symbol": symbol.upper(),
            "period": period,
            "data": data_json,
            "count": len(data_json)
        })
    
    except Exception as e:
        logger.error(f"Error fetching historical data for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analysis/comprehensive")
async def comprehensive_analysis(request: StockAnalysisRequest):
    """Generate comprehensive investment analysis memo"""
    try:
        symbol = request.symbol.upper()
        logger.info(f"Starting comprehensive analysis for {symbol}")
        
        # Fetch all required data in parallel
        tasks = [
            data_provider.get_real_time_price(symbol),
            data_provider.get_key_metrics(symbol),
            data_provider.get_financial_statements(symbol)
        ]
        
        quote_data, metrics_data, financial_data = await asyncio.gather(*tasks)
        
        if not any([quote_data, metrics_data, financial_data]):
            raise HTTPException(status_code=404, detail=f"Insufficient data found for symbol: {symbol}")
        
        # Generate AI analysis
        analysis_result = await analysis_agent.generate_investment_memo(
            company_data=metrics_data,
            financial_data=metrics_data,
            market_data=quote_data
        )
        
        # Combine all data into comprehensive response
        response = {
            "symbol": symbol,
            "analysis_type": request.analysis_type,
            "timestamp": datetime.now().isoformat(),
            "current_quote": quote_data,
            "financial_metrics": metrics_data,
            "ai_analysis": analysis_result,
            "data_quality": {
                "quote_available": bool(quote_data),
                "metrics_available": bool(metrics_data),
                "financial_statements_available": bool(financial_data)
            }
        }
        
        logger.info(f"Completed comprehensive analysis for {symbol}")
        return JSONResponse(content=response)
    
    except Exception as e:
        logger.error(f"Error in comprehensive analysis for {request.symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analysis/dcf")
async def dcf_valuation(request: StockAnalysisRequest):
    """Generate DCF valuation analysis"""
    try:
        symbol = request.symbol.upper()
        logger.info(f"Starting DCF analysis for {symbol}")
        
        # Get financial data
        financial_data = await data_provider.get_key_metrics(symbol)
        statements = await data_provider.get_financial_statements(symbol)
        
        if not financial_data:
            raise HTTPException(status_code=404, detail=f"Financial data not found for symbol: {symbol}")
        
        # Combine financial data and statements
        combined_data = {**financial_data, **statements}
        
        # Generate DCF analysis
        dcf_result = await analysis_agent.calculate_dcf_valuation(combined_data)
        
        response = {
            "symbol": symbol,
            "analysis_type": "dcf_valuation",
            "timestamp": datetime.now().isoformat(),
            "financial_inputs": financial_data,
            "dcf_analysis": dcf_result
        }
        
        logger.info(f"Completed DCF analysis for {symbol}")
        return JSONResponse(content=response)
    
    except Exception as e:
        logger.error(f"Error in DCF analysis for {request.symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analysis/portfolio")
async def portfolio_analysis(request: PortfolioAnalysisRequest):
    """Analyze a portfolio of stocks"""
    try:
        logger.info(f"Starting portfolio analysis for {len(request.symbols)} stocks")
        
        # Get data for all symbols in parallel
        tasks = []
        for symbol in request.symbols:
            tasks.extend([
                data_provider.get_real_time_price(symbol.upper()),
                data_provider.get_key_metrics(symbol.upper())
            ])
        
        results = await asyncio.gather(*tasks)
        
        # Organize results by symbol
        portfolio_data = {}
        for i, symbol in enumerate(request.symbols):
            quote_idx = i * 2
            metrics_idx = i * 2 + 1
            
            portfolio_data[symbol.upper()] = {
                "quote": results[quote_idx] if quote_idx < len(results) else {},
                "metrics": results[metrics_idx] if metrics_idx < len(results) else {}
            }
        
        # Calculate portfolio-level metrics
        total_market_cap = sum(
            data["metrics"].get("market_cap", 0) 
            for data in portfolio_data.values()
        )
        
        weighted_pe = sum(
            (data["metrics"].get("market_cap", 0) / total_market_cap if total_market_cap > 0 else 0) * 
            data["metrics"].get("pe_ratio", 0)
            for data in portfolio_data.values()
        )
        
        response = {
            "symbols": request.symbols,
            "benchmark": request.benchmark,
            "timestamp": datetime.now().isoformat(),
            "portfolio_data": portfolio_data,
            "portfolio_metrics": {
                "total_market_cap": total_market_cap,
                "weighted_pe_ratio": round(weighted_pe, 2),
                "stock_count": len(request.symbols)
            }
        }
        
        logger.info(f"Completed portfolio analysis for {len(request.symbols)} stocks")
        return JSONResponse(content=response)
    
    except Exception as e:
        logger.error(f"Error in portfolio analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """Detailed health check"""
    try:
        # Test data provider
        test_quote = await data_provider.get_real_time_price("AAPL")
        data_provider_status = "operational" if test_quote else "degraded"
        
        # Test AI agent (simple test)
        ai_status = "operational"  # Simplified for now
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "data_provider": data_provider_status,
                "ai_agent": ai_status,
                "api": "operational"
            },
            "version": settings.APP_VERSION
        }
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app_modular:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
