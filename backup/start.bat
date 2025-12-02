@echo off
echo 🚀 Starting Quantum Trading Analytics...
echo.
echo Activating Python environment...
call "C:\Projects\Stock-Analysis-AI-Agents\.venv\Scripts\activate.bat"

echo.
echo Starting professional trading platform...
echo 📊 Access your platform at: http://localhost:8501
echo.

C:\Projects\Stock-Analysis-AI-Agents\.venv\Scripts\streamlit.exe run professional_app.py --server.port 8501

pause
