"""Configuration settings for the Roast My Activity Data application.

This module contains all configuration constants, color schemes, and styling
settings used throughout the application.
"""

from typing import Dict

# Application Settings
APP_TITLE = "🔥 Roast My Activity Data"
DEFAULT_DAYS_BACK = 30
MIN_DAYS_BACK = 1
MAX_DAYS_BACK = 90

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
    "Walking": "#F46A25",    # Orange
    "Strength": "#A285D1",   # Light purple
    "Other": "#801650"       # Dark pink
}

# Activity Type Mappings
ACTIVITY_GROUP_MAP: Dict[str, str] = {
    "Run": "Running",
    "Virtual Run": "Running",
    "Ride": "Cycling",
    "Walk": "Walking",
    "Hike": "Walking",
    "Weight Training": "Strength",
    "Workout": "Strength",
    "Rowing": "Strength",
    "Swim": "Swimming",
    "Open Water Swim": "Swimming",
    "Alpine Ski": "Other",
    "Water Sport": "Other",
    "Unknown": "Other"
}

# Custom CSS Styling
CUSTOM_CSS = """
    <style>
        /* Sidebar width */
        section[data-testid="stSidebar"] {
            width: 221px !important;
        }
        
        /* Multiselect - remove max height so all options show */
        div[data-baseweb="select"] {
            max-height: none !important;
        }
        
        /* Main background and fonts */
        .main {
            background-color: #f5f7fa;
        }
        
        /* Title styling */
        h1 {
            color: #2c3e50;
            font-weight: 700;
            padding-bottom: 20px;
            border-bottom: 3px solid #3498db;
        }
        
        /* Section headers */
        h2, h3 {
            color: #34495e;
            font-weight: 600;
            margin-top: 30px;
        }
        
        /* Metric cards */
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
        
        /* Tab styling */
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
        
        /* Sidebar styling */
        .css-1d391kg, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        }
        
        .css-1d391kg h2, [data-testid="stSidebar"] h2 {
            color: white !important;
        }
        
        .css-1d391kg label, [data-testid="stSidebar"] label {
            color: #ecf0f1 !important;
            font-weight: 500;
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* Card-like sections */
        div[data-testid="column"] {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        /* Remove default streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
    </style>
"""
