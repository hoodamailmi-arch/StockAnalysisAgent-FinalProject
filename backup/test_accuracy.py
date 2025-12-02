import yfinance as yf
import asyncio
import sys
sys.path.append('.')
from data_providers.yahoo_finance import YahooFinanceProvider

# Test both methods
symbol = 'HDFCBANK.NS'
print('=== TESTING REAL-TIME ACCURACY ===')
print(f'Symbol: {symbol}')
print()

# Method 1: professional_app.py approach (direct yfinance)
print('METHOD 1: professional_app.py (Direct yfinance)')
ticker = yf.Ticker(symbol)
info = ticker.info
current_price_direct = info.get('currentPrice', 0)
print(f'Current Price (direct): Rs.{current_price_direct}')
print(f'Previous Close: Rs.{info.get("previousClose", 0)}')
print(f'Market State: {info.get("marketState", "Unknown")}')
print()

# Method 2: app_modular.py approach (via YahooFinanceProvider)
print('METHOD 2: app_modular.py (YahooFinanceProvider)')
provider = YahooFinanceProvider()

async def test_provider():
    data = await provider.get_real_time_price(symbol)
    print(f'Current Price (provider): Rs.{data.get("current_price", 0)}')
    print(f'Previous Close: Rs.{data.get("previous_close", 0)}')
    print(f'Change: Rs.{data.get("change", 0):.2f}')
    print(f'Change %: {data.get("change_percent", 0):.2f}%')
    return data

result = asyncio.run(test_provider())
print()
print('=== COMPARISON ===')
print(f'Direct method price: Rs.{current_price_direct}')
print(f'Provider method price: Rs.{result.get("current_price", 0)}')
print(f'Both use same Yahoo Finance API: {current_price_direct == result.get("current_price", 0)}')
