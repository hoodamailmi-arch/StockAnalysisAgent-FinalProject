import os
from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings"""
    
    # API Keys
    GROQ_API_KEY: str = ""
    ALPHA_VANTAGE_API_KEY: str = ""
    NEWS_API_KEY: str = ""
    FRED_API_KEY: str = ""
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://localhost:5432/stock_analysis"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Application Settings
    APP_NAME: str = "Stock Analysis AI Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    ENVIRONMENT: str = "development"  # Added this field
    
    # LLM Configuration
    DEFAULT_MODEL: str = "llama-3.1-70b-versatile"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.1
    
    # Data Refresh Intervals (in minutes)
    STOCK_DATA_REFRESH: int = 5
    NEWS_REFRESH: int = 15
    ECONOMIC_DATA_REFRESH: int = 60
    
    # Analysis Parameters
    LOOKBACK_DAYS: int = 252  # 1 year of trading days
    RISK_FREE_RATE: float = 0.045  # Current risk-free rate
    MARKET_RETURN: float = 0.10  # Expected market return
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from .env file
        extra = "allow"  # Allow extra fields from .env file
        extra = "allow"  # Allow extra fields from .env

# Global settings instance
settings = Settings()
