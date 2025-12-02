# Run Professional Stock Analysis Application
# Launch Script

import subprocess
import sys
import os

def main():
    print("▓ Professional Stock Analytics Platform")
    print("=" * 50)
    print("Starting enterprise-grade financial intelligence application...")
    print("Dark Theme | Geometric Design | Apple-inspired Interface")
    print()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found!")
        print("📝 Creating .env template...")
        
        env_template = """ Professional Stock Analytics - API Configuration Add your API keys below (remove # to activate)

Groq AI API (Required for AI Analysis)
Get free key from: https://console.groq.com
GROQ_API_KEY

Alpha Vantage API (Enhanced Financial Data)
Get free key from: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY

NewsAPI (Market News & Sentiment)
Get free key from: https://newsapi.org/register
NEWS_API_KEY

FRED API (Economic Data - 10Y Treasury)
Get free key from: https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY

# Instructions:
# 1. Remove the # symbol before each API key line
# 2. Replace 'your_xxx_key_here' with your actual API key
# 3. Save this file
# 4. Restart the application
"""
        
        with open('.env', 'w') as f:
            f.write(env_template)
        
        print("✅ Created .env template file")
        print("📖 Please edit .env file and add your API keys")
        print()
    
    print("🌐 Launching Streamlit application...")
    print("💡 The app will open in your default browser")
    print("🔗 Local URL: http://localhost:8501")
    print()
    print("Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "professional_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("💡 Make sure streamlit is installed: pip install streamlit")

if __name__ == "__main__":
    main()
