"""
Test script for the updated AI Analyzer with current Groq models
Run this to verify AI functionality before using the main app
"""

import os
import sys
sys.path.append('.')

from modules.ai_analyzer import AIAnalyzer

def test_ai_analyzer():
    """Test the AI analyzer with current models"""
    
    print("🧪 Testing AI Analyzer...")
    print("=" * 50)
    
    try:
        # Initialize analyzer
        analyzer = AIAnalyzer()
        
        # Check model status
        status = analyzer.get_model_status()
        print(f"✅ API Key Configured: {status['api_key_configured']}")
        print(f"✅ Client Initialized: {status['client_initialized']}")
        print(f"✅ Current Model: {status['current_model']}")
        print(f"✅ Available Models: {status['available_models']}")
        print(f"✅ Is Available: {status['is_available']}")
        
        if not status['is_available']:
            if not status['api_key_configured']:
                print("\n❌ ERROR: GROQ_API_KEY not found in environment")
                print("💡 Add GROQ_API_KEY to your .env file")
            elif not status['current_model']:
                print("\n❌ ERROR: No Groq models are currently available")
                print("💡 All models may be temporarily unavailable")
            return False
        
        print(f"\n🤖 Testing with model: {status['current_model']}")
        print("-" * 50)
        
        # Test with sample data
        sample_data = {
            'current_price': 150.0,
            'market_cap': 2.5e12,
            'pe_ratio': 25.5,
            'peg_ratio': 1.2,
            'roe': 0.25,
            'debt_to_equity': 0.3,
            'current_ratio': 1.5,
            'profit_margin': 0.15,
            'revenue_growth': 0.08,
            'beta': 1.1,
            'volatility': 0.22
        }
        
        sample_news = [
            {'title': 'Company reports strong quarterly earnings beat'},
            {'title': 'New AI product launch receives positive reviews'}
        ]
        
        print("📊 Generating test analysis for AAPL...")
        analysis = analyzer.create_enhanced_ai_analysis("AAPL", sample_data, sample_news)
        
        if analysis and not analysis.startswith("❌"):
            print("✅ AI Analysis Generation: SUCCESS!")
            print(f"📝 Analysis length: {len(analysis)} characters")
            print("\n📋 Sample Output (first 200 chars):")
            print("-" * 50)
            print(analysis[:200] + "..." if len(analysis) > 200 else analysis)
        else:
            print(f"❌ AI Analysis Generation: FAILED")
            print(f"Error: {analysis}")
            return False
        
        # Test sentiment analysis
        print("\n🎯 Testing sentiment analysis...")
        headlines = ['Strong earnings beat expectations', 'New AI chip announcement drives optimism']
        sentiment = analyzer.get_quick_sentiment("AAPL", headlines)
        print(f"📊 Sentiment Result: {sentiment}")
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! AI Analyzer is ready for use.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        print(f"💡 Error type: {type(e).__name__}")
        return False

def check_env_setup():
    """Check if environment is properly configured"""
    print("🔧 Checking environment setup...")
    print("-" * 30)
    
    # Check for .env file
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        print("💡 Create .env file with your API keys")
    
    # Check for API key
    groq_key = os.getenv('GROQ_API_KEY')
    if groq_key:
        print(f"✅ GROQ_API_KEY configured (starts with: {groq_key[:10]}...)")
    else:
        print("❌ GROQ_API_KEY not found")
        print("💡 Add GROQ_API_KEY=your_key_here to .env file")
    
    print()

if __name__ == "__main__":
    print("🚀 AI Analyzer Test Suite")
    print("=" * 50)
    
    # Check environment
    check_env_setup()
    
    # Run tests
    success = test_ai_analyzer()
    
    if success:
        print("\n🎯 READY TO USE: Launch your app with:")
        print("   streamlit run professional_app_modular.py")
    else:
        print("\n🔧 SETUP REQUIRED: Fix the issues above before using AI features")
