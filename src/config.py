"""Configuration settings for the Roast My Activity Data application.

This module contains all configuration constants, color schemes, and styling
settings used throughout the application.
"""

from typing import Dict

# Version
VERSION = "0.9.3"

# Application Settings
APP_TITLE = "🔥 Roast My Activity Data"
DEFAULT_DAYS_BACK = 30
MIN_DAYS_BACK = 1
MAX_DAYS_BACK = 365

# Data Settings
DATA_FILE_PATH = "data/activities.csv"

# Physical Constants
EARTH_CIRCUMFERENCE_KM = 40075
EVEREST_HEIGHT_M = 8849
WEEKS_PER_YEAR = 52

# UK Government Analysis Function Accessible Color Palette
ACTIVITY_COLORS: Dict[str, str] = {
    "Running": "#12436D",    # Dark blue
    "Cycling": "#28A197",    # Turquoise
    "Swimming": "#4C2C92",   # Bright purple (navy)
    "Hiking": "#D4A01C",     # Dark gold/amber - for hikes and walks
    "Strength": "#A285D1",   # Light purple
    "Winter Sports": "#7DD3FC",  # Sky blue - covers Alpine Ski, Backcountry Ski, Nordic Ski, Snowboard
    "Team Sports": "#D4351C",  # Red - covers Rugby, Football, Netball, Basketball, Soccer
    "Other": "#801650"       # Dark pink
}

# Activity Type Mappings
ACTIVITY_GROUP_MAP: Dict[str, str] = {
    "Run": "Running",
    "Virtual Run": "Running",
    "Ride": "Cycling",
    "Walk": "Hiking",
    "Hike": "Hiking",
    "Weight Training": "Strength",
    "Workout": "Strength",
    "Rowing": "Strength",
    "Swim": "Swimming",
    "Open Water Swim": "Swimming",
    "Alpine Ski": "Winter Sports",
    "Backcountry Ski": "Winter Sports",
    "Nordic Ski": "Winter Sports",
    "Snowboard": "Winter Sports",
    "Rugby": "Team Sports",
    "Football": "Team Sports",
    "Netball": "Team Sports",
    "Basketball": "Team Sports",
    "Soccer": "Team Sports",
    "Water Sport": "Other",
    "Unknown": "Other"
}

# Custom CSS Styling with Dark Mode Support
CUSTOM_CSS = """
    <style>
        /* Compact horizontal radio buttons for year selector */
        .stRadio > div {
            gap: 0.3rem !important;
        }
        
        .stRadio > div > label {
            padding: 0.2rem 0.5rem !important;
            font-size: 12px !important;
            min-height: unset !important;
        }
        
        .stRadio > div > label > div:first-child {
            width: 14px !important;
            height: 14px !important;
        }
        
        .stRadio > div > label p {
            font-size: 12px !important;
        }
        
        /* Mobile responsive adjustments */
        @media (max-width: 768px) {
            section[data-testid="stSidebar"] {
                width: 100% !important;
            }
            
            h1 {
                font-size: 24px !important;
            }
            
            [data-testid="stMetricValue"] {
                font-size: 20px !important;
            }
            
            div[data-testid="column"] {
                padding: 10px !important;
                margin-bottom: 10px;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 40px;
                padding: 0 12px;
                font-size: 14px;
            }
        }
        
        /* Sidebar width for desktop */
        @media (min-width: 769px) {
            section[data-testid="stSidebar"] {
                width: 221px !important;
            }
        }
        
        /* Multiselect - remove max height so all options show */
        div[data-baseweb="select"] {
            max-height: none !important;
        }
        
        /* Multiselect tags - smaller */
        [data-testid="stSidebar"] div[data-baseweb="tag"] {
            font-size: 11px !important;
            padding: 1px 4px !important;
            height: 22px !important;
        }
        
        /* Multiselect tag close button */
        [data-testid="stSidebar"] div[data-baseweb="tag"] button {
            width: 16px !important;
            height: 16px !important;
            min-height: 16px !important;
            padding: 0 !important;
        }
        
        /* Multiselect input */
        [data-testid="stSidebar"] input {
            font-size: 13px !important;
        }
        
        /* Reduce spacing in sidebar */
        [data-testid="stSidebar"] .element-container {
            margin-bottom: 0.5rem !important;
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            margin-bottom: 0.3rem !important;
        }
        
        /* Expander checkboxes - tighter spacing */
        [data-testid="stSidebar"] [data-testid="stExpander"] .stCheckbox {
            margin-bottom: 0 !important;
            margin-top: 0 !important;
            padding: 0 !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stExpander"] .element-container {
            margin-bottom: 0 !important;
            margin-top: 0 !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stExpander"] label {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            font-size: 12px !important;
            line-height: 1.3 !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stExpander"] label p {
            font-size: 12px !important;
            margin: 0 !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stExpander"] .stCheckbox label {
            font-size: 12px !important;
        }
        
        /* Expander header text */
        [data-testid="stSidebar"] [data-testid="stExpander"] summary {
            color: #2c3e50 !important;
            background-color: #ecf0f1 !important;
            border-radius: 4px !important;
            padding: 0.3rem 0.4rem !important;
            font-size: 12px !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
            background-color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stExpander"] summary p {
            color: #2c3e50 !important;
            font-size: 12px !important;
        }
        
        /* All sidebar controls text sizing */
        [data-testid="stSidebar"] .stRadio label,
        [data-testid="stSidebar"] .stRadio label p,
        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stSlider label p,
        [data-testid="stSidebar"] .stCheckbox label,
        [data-testid="stSidebar"] .stCheckbox label p,
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stSelectbox label p {
            font-size: 12px !important;
            margin: 0 !important;
        }
        
        /* Selectbox dropdown text */
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
            font-size: 12px !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox {
            font-size: 12px !important;
        }
        
        /* Dropdown menu options */
        div[data-baseweb="popover"] ul li,
        div[data-baseweb="popover"] ul li div,
        div[data-baseweb="popover"] ul li span {
            font-size: 12px !important;
        }
        
        /* Sidebar heading */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            font-size: 14px !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Light mode (default) */
        .main {
            background-color: #f5f7fa;
            padding-top: 1rem !important;
        }
        
        .block-container {
            padding-top: 1rem !important;
        }
        
        h1 {
            color: #2c3e50;
            font-weight: 700;
            padding-bottom: 20px;
            margin-top: 0 !important;
            border-bottom: 3px solid #3498db;
        }
        
        h2, h3 {
            color: #34495e;
            font-weight: 600;
            margin-top: 30px;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: 700;
            color: #2c3e50;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 16px;
            color: #7f8c8d;
            font-weight: 500;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background-color: #ecf0f1;
            border-radius: 8px;
            padding: 0 24px;
            font-weight: 600;
            color: #34495e;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        div[data-testid="column"] {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        /* Dark mode overrides */
        @media (prefers-color-scheme: dark) {
            .main {
                background-color: #0e1117;
            }
            
            h1 {
                color: #fafafa;
                border-bottom: 3px solid #5584ff;
            }
            
            h2, h3 {
                color: #fafafa;
            }
            
            [data-testid="stMetricValue"] {
                color: #fafafa;
            }
            
            [data-testid="stMetricLabel"] {
                color: #a3a8b4;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                background-color: #262730;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: #1e1f26;
                color: #fafafa;
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #5584ff 0%, #7b3ff2 100%);
                color: white;
            }
            
            div[data-testid="column"] {
                background-color: #262730;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            }
            
            .dataframe {
                background-color: #1e1f26;
                color: #fafafa;
            }
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        }
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p {
            color: #ecf0f1 !important;
        }
        
        /* Sidebar title */
        [data-testid="stSidebar"] h1 {
            font-size: 20px !important;
            color: #ffffff !important;
            border-bottom: none !important;
            padding-bottom: 5px !important;
            margin-top: 0 !important;
            padding-top: 0.5rem !important;
        }
        
        /* Sidebar labels - smaller text */
        [data-testid="stSidebar"] label {
            font-size: 13px !important;
        }
        
        /* Sidebar subheaders */
        [data-testid="stSidebar"] h3 {
            font-size: 14px !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.3rem !important;
        }
        
        /* Sidebar buttons */
        [data-testid="stSidebar"] button {
            color: #2c3e50 !important;
            background-color: #ecf0f1 !important;
            border: 1px solid #bdc3c7 !important;
            font-size: 12px !important;
            padding: 0.35rem 0.5rem !important;
            min-height: 32px !important;
        }
        
        [data-testid="stSidebar"] button:hover {
            background-color: #ffffff !important;
            border-color: #95a5a6 !important;
        }
        
        [data-testid="stSidebar"] button p {
            color: #2c3e50 !important;
            font-size: 12px !important;
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* Remove default streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
    </style>
"""


# Plotly theme colors
PLOTLY_LIGHT_THEME = {
    "plot_bgcolor": "white",
    "paper_bgcolor": "white",
    "font_color": "#2c3e50",
    "grid_color": "#f0f0f0",
    "title_color": "#2c3e50"
}

PLOTLY_DARK_THEME = {
    "plot_bgcolor": "#1e1f26",
    "paper_bgcolor": "#262730",
    "font_color": "#fafafa",
    "grid_color": "#3e4148",
    "title_color": "#fafafa"
}
