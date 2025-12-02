# ======================================
# QUANTUM TRADING ANALYTICS - TEST SUITE
# ======================================

import sys
import os
sys.path.append('.')

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    try:
        import streamlit as st
        import pandas as pd
        import plotly.graph_objects as go
        import yfinance as yf
        import numpy as np
        from groq import Groq
        print("✅ All core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_yahoo_finance():
    """Test Yahoo Finance connectivity"""
    print("📊 Testing Yahoo Finance connectivity...")
    try:
        import yfinance as yf
        
        # Test popular symbols
        symbols = ['AAPL', 'HDFCBANK.NS', 'GOOGL']
        
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            current_price = info.get('currentPrice', 0)
            
            if current_price > 0:
                print(f"✅ {symbol}: ${current_price:.2f}")
            else:
                hist = ticker.history(period="1d")
                if not hist.empty:
                    price = hist['Close'].iloc[-1]
                    print(f"✅ {symbol}: ${price:.2f} (from history)")
                else:
                    print(f"⚠️ {symbol}: No data available")
        
        return True
    except Exception as e:
        print(f"❌ Yahoo Finance error: {e}")
        return False

def test_groq_setup():
    """Test Groq API setup"""
    print("🤖 Testing Groq API setup...")
    try:
        from groq import Groq
        
        # Check if API key is set
        api_key = os.getenv('GROQ_API_KEY')
        
        if not api_key or api_key == 'your_groq_api_key_here':
            print("⚠️ Groq API key not configured")
            print("   Get your free key from: https://console.groq.com")
            print("   Add to .env file: GROQ_API_KEY=your_key_here")
            return False
        
        # Test API connection
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": "Test connection. Reply with 'OK'."}],
            max_tokens=10,
            temperature=0
        )
        
        if "OK" in response.choices[0].message.content:
            print("✅ Groq API connection successful")
            return True
        else:
            print("⚠️ Groq API responded but unexpected response")
            return False
            
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return False

def test_comprehensive_analysis():
    """Test comprehensive stock analysis"""
    print("🔬 Testing comprehensive analysis functions...")
    try:
        # Import our professional app functions
        from professional_app import (
            get_stock_data, 
            get_comprehensive_metrics,
            get_technical_indicators,
            calculate_volatility,
            calculate_rsi
        )
        
        # Test with AAPL
        print("   Testing with AAPL...")
        stock_data = get_stock_data('AAPL', '1mo')
        
        if stock_data.get('success'):
            info = stock_data['info']
            historical = stock_data['historical']
            
            # Test comprehensive metrics
            metrics = get_comprehensive_metrics(info, historical)
            if metrics:
                print(f"   ✅ Comprehensive metrics: {len(metrics)} indicators")
            
            # Test technical indicators
            technical = get_technical_indicators(historical)
            if technical:
                print(f"   ✅ Technical indicators: {len(technical)} indicators")
            
            # Test volatility calculation
            volatility = calculate_volatility(historical)
            print(f"   ✅ Volatility: {volatility:.2f}%")
            
            # Test RSI calculation
            rsi = calculate_rsi(historical['Close'])
            print(f"   ✅ RSI: {rsi:.2f}")
            
            print("✅ Comprehensive analysis test passed")
            return True
        else:
            print("❌ Failed to fetch stock data")
            return False
            
    except Exception as e:
        print(f"❌ Comprehensive analysis error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 QUANTUM TRADING ANALYTICS - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_yahoo_finance,
        test_groq_setup,
        test_comprehensive_analysis
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your application is ready to use.")
        print()
        print("🚀 To start the application:")
        print("   streamlit run professional_app.py")
        print()
        print("📋 Next steps:")
        print("   1. Get Groq API key from: https://console.groq.com")
        print("   2. Add to .env file for AI analysis")
        print("   3. Test with symbols like AAPL, HDFCBANK.NS, GOOGL")
    else:
        print(f"⚠️ {total - passed} tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    main()
