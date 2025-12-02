# Style Module
# Contains all CSS styling for the dark theme interface

from .config import UIConfig

def get_dark_theme_css():
    """Returns the complete CSS for dark theme styling"""
    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Variables */
    :root {{
        --primary-bg: {UIConfig.COLORS['primary_bg']};
        --secondary-bg: {UIConfig.COLORS['secondary_bg']};
        --tertiary-bg: {UIConfig.COLORS['tertiary_bg']};
        --card-bg: {UIConfig.COLORS['card_bg']};
        --border-color: {UIConfig.COLORS['border_color']};
        --text-primary: {UIConfig.COLORS['text_primary']};
        --text-secondary: {UIConfig.COLORS['text_secondary']};
        --accent-blue: {UIConfig.COLORS['accent_blue']};
        --accent-green: {UIConfig.COLORS['accent_green']};
        --accent-red: {UIConfig.COLORS['accent_red']};
        --accent-orange: {UIConfig.COLORS['accent_orange']};
        --surface: {UIConfig.COLORS['surface']};
        --hover: {UIConfig.COLORS['hover']};
    }}
    
    /* Base Styling */
    .stApp {{
        background-color: var(--primary-bg);
        color: var(--text-primary);
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
    }}
    
    /* Hide Streamlit Elements */
    .stDeployButton {{ display: none; }}
    header[data-testid="stHeader"] {{ display: none; }}
    .stMainMenu {{ display: none; }}
    footer {{ display: none; }}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: var(--secondary-bg);
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb {{
        background: var(--border-color);
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--text-secondary);
    }}
    
    /* Main Header */
    .main-header {{
        background: var(--secondary-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 32px;
        text-align: center;
        backdrop-filter: blur(20px);
    }}
    
    .main-title {{
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 8px;
        color: var(--text-primary);
        letter-spacing: -0.025em;
    }}
    
    .main-subtitle {{
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        font-size: 1.1rem;
        font-weight: 400;
        color: var(--text-secondary);
        letter-spacing: -0.01em;
    }}
    
    /* Section Headers */
    .section-header {{
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        padding: 16px 24px;
        border-radius: {UIConfig.LAYOUT['border_radius']};
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        font-size: 1.1rem;
        font-weight: 600;
        margin: 24px 0 16px 0;
        text-align: left;
        letter-spacing: -0.01em;
    }}
    
    /* Chart Container */
    .chart-container {{
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: {UIConfig.LAYOUT['card_padding']};
        margin: 16px 0;
    }}
    
    /* AI Analysis */
    .ai-analysis {{
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: {UIConfig.LAYOUT['card_padding']};
        margin: 16px 0;
        position: relative;
    }}
    
    .ai-analysis::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-green));
        border-radius: 16px 16px 0 0;
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background: var(--secondary-bg);
        border-right: 1px solid var(--border-color);
    }}
    
    /* Input Fields */
    .stTextInput > div > div > input {{
        background: var(--tertiary-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
    }}
    
    .stSelectbox > div > div > select {{
        background: var(--tertiary-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
    }}
    
    /* Buttons */
    .stButton > button {{
        background: var(--accent-blue);
        border: none;
        border-radius: 8px;
        color: white;
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        font-weight: 500;
        padding: 12px 24px;
        transition: all 0.2s ease;
        width: 100%;
    }}
    
    .stButton > button:hover {{
        background: #0056d6;
        transform: translateY(-1px);
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: var(--secondary-bg);
        border-radius: {UIConfig.LAYOUT['border_radius']};
        padding: 4px;
        border: 1px solid var(--border-color);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 8px;
        color: var(--text-secondary);
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        font-weight: 500;
        padding: 12px 16px;
        transition: all 0.2s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: var(--accent-blue);
        color: white;
    }}
    
    /* Metrics */
    [data-testid="metric-container"] {{
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: {UIConfig.LAYOUT['border_radius']};
        padding: 16px;
    }}
    
    [data-testid="metric-container"] [data-testid="metric-label"] {{
        color: var(--text-secondary);
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        font-size: 0.9rem;
        font-weight: 500;
    }}
    
    [data-testid="metric-container"] [data-testid="metric-value"] {{
        color: var(--text-primary);
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        font-size: 1.5rem;
        font-weight: 600;
    }}
    
    /* Progress Bar */
    .stProgress .st-bo {{
        background: var(--tertiary-bg);
        border-radius: 8px;
    }}
    
    .stProgress .st-bp {{
        background: var(--accent-blue);
        border-radius: 8px;
    }}
    
    /* Custom Typography */
    h1, h2, h3, h4, h5, h6 {{
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        color: var(--text-primary);
        letter-spacing: -0.025em;
    }}
    
    p, span, div {{
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        color: var(--text-primary);
    }}
    
    /* Status Indicators */
    .status-active {{
        color: var(--accent-green);
        font-weight: 600;
    }}
    
    .status-inactive {{
        color: var(--accent-red);
        font-weight: 600;
    }}
    
    /* Footer */
    .footer {{
        background: var(--secondary-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: {UIConfig.LAYOUT['card_padding']};
        margin-top: {UIConfig.LAYOUT['section_spacing']};
        text-align: center;
    }}
    
    .footer-title {{
        color: var(--text-primary);
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }}
    
    .footer-subtitle {{
        color: var(--text-secondary);
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        font-size: 0.9rem;
    }}
    
    /* Info Boxes */
    .info-box {{
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: {UIConfig.LAYOUT['border_radius']};
        padding: 16px;
        margin: 8px 0;
    }}
    
    .info-title {{
        color: var(--text-primary);
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        font-weight: 600;
        margin-bottom: 8px;
    }}
    
    .info-content {{
        color: var(--text-secondary);
        font-family: '{UIConfig.FONTS['primary']}', {UIConfig.FONTS['system']};
        font-size: 0.9rem;
    }}
</style>
"""
