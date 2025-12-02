#!/usr/bin/env python3
"""
Setup script for Stock Analysis AI Agent application
Handles environment setup, dependency installation, and initial configuration
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header():
    """Print setup header"""
    print("=" * 60)
    print("🚀 STOCK ANALYSIS AI AGENT SETUP")
    print("=" * 60)
    print("Professional-Grade Financial Analysis with AI")
    print("")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Error: Python 3.9 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version: {sys.version.split()[0]} (Compatible)")

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        sys.exit(1)

def setup_environment():
    """Setup environment file"""
    print("\n🔧 Setting up environment...")
    
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from template")
        else:
            create_basic_env()
    else:
        print("ℹ️  .env file already exists")
    
    print("\n📝 Please edit .env file with your API keys:")
    print("   - GROQ_API_KEY (Required for AI analysis)")
    print("   - ALPHA_VANTAGE_API_KEY (Optional, for premium data)")
    print("   - NEWS_API_KEY (Optional, for sentiment analysis)")

def create_basic_env():
    """Create basic .env file"""
    env_content = """# Stock Analysis AI Agent Environment Configuration

# =============================================================================
# API KEYS - Replace with your actual API keys
# =============================================================================

# Groq API for LLM inference (Free tier available)
GROQ_API_KEY=your_groq_api_key_here

# Alpha Vantage for stock data (Optional - Free: 25 calls/day)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# NewsAPI for sentiment analysis (Optional - Free: 1000 requests/day)
NEWS_API_KEY=your_news_api_key_here

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

# Environment
ENVIRONMENT=development
DEBUG=true

# Default model for analysis
DEFAULT_MODEL=llama-3.1-70b-versatile
MAX_TOKENS=4000
TEMPERATURE=0.1
"""
    
    with open(".env", "w") as f:
        f.write(env_content)

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "logs",
        "data",
        "cache",
        "exports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def test_installation():
    """Test if installation is working"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test basic imports
        import fastapi
        import streamlit
        import pandas
        import plotly
        print("✅ Core packages imported successfully")
        
        # Test data provider
        from data_providers.yahoo_finance import YahooFinanceProvider
        print("✅ Data provider module loaded")
        
        # Test configuration
        from config.settings import settings
        print("✅ Configuration loaded")
        
        print("\n🎉 Installation test passed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please check your installation and try again")
        sys.exit(1)

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS")
    print("=" * 60)
    
    print("\n1. 🔑 CONFIGURE API KEYS:")
    print("   Edit the .env file and add your API keys:")
    print("   - Get Groq API key: https://console.groq.com/")
    print("   - Get Alpha Vantage key: https://www.alphavantage.co/support/#api-key")
    
    print("\n2. 🚀 RUN THE APPLICATION:")
    print("   Option A - Streamlit Dashboard (Recommended):")
    print("   streamlit run streamlit_app.py")
    print("")
    print("   Option B - FastAPI Backend:")
    print("   python app_modular.py")
    
    print("\n3. 📖 ACCESS THE APPLICATION:")
    print("   Streamlit: http://localhost:8501")
    print("   FastAPI: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    
    print("\n4. 📊 START ANALYZING:")
    print("   - Enter a stock symbol (e.g., AAPL, GOOGL, MSFT)")
    print("   - Choose analysis type")
    print("   - Get AI-powered investment insights!")
    
    print("\n🆘 NEED HELP?")
    print("   - Check README.md for detailed documentation")
    print("   - Visit our GitHub repository for support")
    print("   - Review the logs/ directory for error details")
    
    print("\n" + "=" * 60)
    print("Happy Analyzing! 📈💰")
    print("=" * 60)

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    setup_environment()
    
    # Create directories
    create_directories()
    
    # Test installation
    test_installation()
    
    # Print usage instructions
    print_usage_instructions()

if __name__ == "__main__":
    main()
