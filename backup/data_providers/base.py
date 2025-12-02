from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import pandas as pd
from datetime import datetime, timedelta

class DataProvider(ABC):
    """Abstract base class for data providers"""
    
    @abstractmethod
    async def get_stock_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Get historical stock data"""
        pass
    
    @abstractmethod
    async def get_real_time_price(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock price"""
        pass
    
    @abstractmethod
    async def get_financial_statements(self, symbol: str) -> Dict[str, Any]:
        """Get financial statements"""
        pass
    
    @abstractmethod
    async def get_key_metrics(self, symbol: str) -> Dict[str, Any]:
        """Get key financial metrics"""
        pass
