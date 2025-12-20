import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(page_title="Roast My Strava", layout="wide")

# Custom CSS for professional styling
st.markdown("""
    <style>
        /* Widen sidebar */
        section[data-testid="stSidebar"] {
            width: 250px !important;
        }
        
        /* Multiselect to show all 6 options */
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
    """, unsafe_allow_html=True)

# Title
st.title("🔥 Roast My Strava")

# Sidebar for sample data generation
st.sidebar.header("Settings")
days_back = st.sidebar.slider("Show activities from last N days", 1, 90, 30)

# Load actual Strava data from CSV
@st.cache_data
def load_strava_data():
    """Load Strava activities from CSV"""
    df = pd.read_csv("activities.csv")
    # Convert Activity Date to datetime
    df["Activity Date"] = pd.to_datetime(df["Activity Date"])
    # Convert numeric columns to float, handling any non-numeric values
    df["Distance"] = pd.to_numeric(df["Distance"], errors='coerce')
    df["Elapsed Time"] = pd.to_numeric(df["Elapsed Time"], errors='coerce')
    df["Elevation Gain"] = pd.to_numeric(df["Elevation Gain"], errors='coerce')
    df["Average Speed"] = pd.to_numeric(df["Average Speed"], errors='coerce')
    
    # Distance is already in km
    df["Distance (km)"] = df["Distance"]
    # Convert Elapsed Time to minutes
    df["Duration (min)"] = df["Elapsed Time"] / 60
    # Elevation Gain in meters
    df["Elevation (m)"] = df["Elevation Gain"]
    # Average Speed is already in km/h
    df["Average Speed (km/h)"] = df["Average Speed"]
    
    # Use Activity Type column directly from CSV
    df["Activity Type"] = df["Activity Type"].fillna("Unknown")
    
    # Create activity groupings
    activity_group_map = {
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
    df["Activity Group"] = df["Activity Type"].map(activity_group_map)
    
    # Drop rows with missing values in key columns
    df = df.dropna(subset=["Distance (km)", "Duration (min)"])
    
    return df.sort_values("Activity Date", ascending=False)

# Load data
df = load_strava_data()

# Activity type filter in sidebar
available_activity_groups = sorted(df["Activity Group"].unique())
selected_activities = st.sidebar.multiselect(
    "Filter by Activity Type",
    options=available_activity_groups,
    default=available_activity_groups,
    max_selections=6
)

# Apply activity type filter
df = df[df["Activity Group"].isin(selected_activities)]

# Filter by date range
df_filtered = df[df["Activity Date"] >= (datetime.now() - timedelta(days=days_back))]

# Create tabs for Recent and All-Time views
tab_recent, tab_alltime = st.tabs(["📊 Recent Activity", "🏆 All-Time Analysis"])

# ============================================================================
# RECENT ACTIVITY TAB
# ============================================================================
with tab_recent:
    st.subheader(f"Last {days_back} Days")

    # Metrics for recent period
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Activities", f"{len(df_filtered):,}")

    with col2:
        st.metric("Total Distance", f"{df_filtered['Distance (km)'].sum():,.1f} km")

    with col3:
        st.metric("Total Duration", f"{df_filtered['Duration (min)'].sum() / 60:,.1f} hrs")

    with col4:
        st.metric("Total Elevation", f"{int(df_filtered['Elevation (m)'].sum()):,} m")

    # Charts section for recent activity
    col1, col2 = st.columns(2)

    with col1:
        # Distance over time
        fig_distance = px.line(
            df_filtered.sort_values("Activity Date"),
            x="Activity Date",
            y="Distance (km)",
            title="Distance Per Activity",
            markers=True
        )
        st.plotly_chart(fig_distance, width='stretch')

    with col2:
        # Activity type distribution
        activity_counts = df_filtered["Activity Group"].value_counts()
        
        # UK Government Analysis Function accessible palette
        color_map = {
            "Running": "#12436D",        # Dark blue
            "Cycling": "#28A197",        # Turquoise
            "Swimming": "#801650",       # Dark pink
            "Walking": "#F46A25",        # Orange
            "Strength": "#A285D1",       # Light purple
            "Other": "#3D3D3D"           # Dark grey
        }
        
        fig_type = px.pie(
            values=activity_counts.values,
            names=activity_counts.index,
            title="Activities by Type",
            color=activity_counts.index,
            color_discrete_map=color_map
        )
        st.plotly_chart(fig_type, width='stretch')

    # Activity duration distribution
    fig_duration = px.histogram(
        df_filtered,
        x="Duration (min)",
        title="Duration Distribution",
        nbins=15
    )
    st.plotly_chart(fig_duration, width='stretch')

    # Recent Activities Data Table
    st.subheader("Recent Activities")
    st.dataframe(
        df_filtered.sort_values("Activity Date", ascending=False)[
            ["Activity Date", "Activity Type", "Distance (km)", "Duration (min)", "Elevation (m)", "Average Speed (km/h)"]
        ],
        width='stretch',
        hide_index=True
    )

# ============================================================================
# ALL-TIME ANALYSIS TAB
# ============================================================================
with tab_alltime:
    st.markdown("*Showing data from all your activities*")
    
    # All-time metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Activities", f"{len(df):,}")

    with col2:
        st.metric("Total Distance", f"{int(df['Distance (km)'].sum()):,} km")

    with col3:
        st.metric("Total Duration", f"{int(df['Duration (min)'].sum() / 60):,} hrs")

    with col4:
        st.metric("Total Elevation", f"{int(df['Elevation (m)'].sum()):,} m")
    
    # Fun metrics: Put your stats in context
    earth_circumference_km = 40075
    everest_height_m = 8849
    total_distance = df['Distance (km)'].sum()
    total_elevation = df['Elevation (m)'].sum()
    total_hours = df['Duration (min)'].sum() / 60
    total_activities = len(df)
    
    times_around_world = total_distance / earth_circumference_km
    times_up_everest = total_elevation / everest_height_m
    days_active = total_hours / 24
    activities_per_week = total_activities / 52  # Roughly per year
    
    st.markdown("")  # Spacing
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📅 Activities/Week", f"{activities_per_week:.1f}", 
                 help=f"Based on {total_activities:,} total activities")
    
    with col2:
        if times_around_world >= 1:
            st.metric("🌍 Around Earth", f"{times_around_world:.2f}x", 
                     help=f"Based on {earth_circumference_km:,} km circumference")
        else:
            percentage = times_around_world * 100
            st.metric("🌍 Around Earth", f"{percentage:.1f}%", 
                     help=f"{int(total_distance):,} km of {earth_circumference_km:,} km")
    
    with col3:
        if days_active >= 365:
            years = days_active / 365
            st.metric("⏱️ Time Active", f"{years:.1f} years", 
                     help=f"That's {int(total_hours):,} hours of activity!")
        else:
            st.metric("⏱️ Time Active", f"{int(days_active)} days", 
                     help=f"That's {int(total_hours):,} hours of activity!")
    
    with col4:
        if times_up_everest >= 1:
            st.metric("🏔️ Up Mt Everest", f"{times_up_everest:.1f}x", 
                     help=f"Based on Everest's {everest_height_m:,}m height")
        else:
            percentage = times_up_everest * 100
            st.metric("🏔️ Up Mt Everest", f"{percentage:.0f}%", 
                     help=f"{int(total_elevation):,}m of {everest_height_m:,}m")
    
    st.markdown("---")

    # Prepare data for time series
    df_timeline = df.copy()
    df_timeline["Date"] = df_timeline["Activity Date"].dt.date
    df_timeline["Quarter"] = df_timeline["Activity Date"].dt.to_period("Q").astype(str)

    # Quarterly aggregated data
    monthly_data = df_timeline.groupby("Quarter").agg({
        "Distance (km)": "sum",
        "Duration (min)": "sum",
        "Activity Group": "count"
    }).reset_index()
    monthly_data.columns = ["Quarter", "Distance", "Duration", "Activity Count"]
    monthly_data["Duration (hours)"] = (monthly_data["Duration"] / 60).round(1)
    monthly_data = monthly_data.sort_values("Quarter")

    # Cumulative distance over time
    monthly_data["Cumulative Distance"] = monthly_data["Distance"].cumsum()

    # Plot 1: Cumulative Distance Over Time
    fig_cumulative = px.line(
        monthly_data,
        x="Quarter",
        y="Cumulative Distance",
        title="Cumulative Distance Over Time",
        markers=True,
        labels={"Cumulative Distance": "Total Distance (km)", "Quarter": "Quarter"}
    )
    fig_cumulative.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_cumulative, width='stretch')

    # Plot 2: Quarterly Activity Trends - Multiple metrics
    fig_trends = px.line(
        monthly_data,
        x="Quarter",
        y=["Distance", "Activity Count"],
        title="Quarterly Activity Trends",
        labels={"value": "Value", "variable": "Metric"},
        markers=True
    )
    fig_trends.update_xaxes(tickangle=-45)
    fig_trends.update_yaxes(secondary_y=False)
    st.plotly_chart(fig_trends, width='stretch')

    # Plot 3: Activity Type Distribution Over Time
    activity_by_quarter = df.groupby([df["Activity Date"].dt.to_period("Q").astype(str), "Activity Group"]).size().reset_index(name="Count")
    activity_by_quarter.columns = ["Quarter", "Activity Group", "Count"]
    activity_by_quarter = activity_by_quarter.sort_values("Quarter")

    if len(activity_by_quarter) > 0:
        # UK Government Analysis Function accessible palette
        color_map = {
            "Running": "#12436D",        # Dark blue
            "Cycling": "#28A197",        # Turquoise
            "Swimming": "#801650",       # Dark pink
            "Walking": "#F46A25",        # Orange
            "Strength": "#A285D1",       # Light purple
            "Other": "#3D3D3D"           # Dark grey
        }
        
        fig_stacked = px.bar(
            activity_by_quarter,
            x="Quarter",
            y="Count",
            color="Activity Group",
            title="Activity Type Composition Over Time",
            labels={"Count": "Number of Activities", "Quarter": "Quarter"},
            color_discrete_map=color_map,
            barmode="stack"
        )
        fig_stacked.update_xaxes(tickangle=-45)
        fig_stacked.update_layout(
            hovermode="x unified",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02
            )
        )
        st.plotly_chart(fig_stacked, width='stretch', use_container_width=True)
    else:
        st.warning("No activity type data available")

    # Plot 4: Rolling Average (smooth trends)
    monthly_data["Rolling Avg Distance"] = monthly_data["Distance"].rolling(window=2).mean()

    fig_rolling = px.line(
        monthly_data,
        x="Quarter",
        y="Rolling Avg Distance",
        title="Rolling Average Distance (Shows Long-term Trends)",
        markers=True,
        labels={"Rolling Avg Distance": "Distance (km)", "Quarter": "Quarter"}
    )
    fig_rolling.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_rolling, width='stretch')

    # Plot 5: Year-over-Year Comparison
    df_timeline["Year"] = df_timeline["Activity Date"].dt.year
    df_timeline["Month"] = df_timeline["Activity Date"].dt.month

    yearly_monthly = df_timeline.groupby(["Year", "Month"]).agg({
        "Distance (km)": "sum"
    }).reset_index()
    yearly_monthly["Month Name"] = pd.to_datetime(yearly_monthly["Month"], format='%m').dt.month_name()
    yearly_monthly["Year"] = yearly_monthly["Year"].astype(str)

    fig_yoy = px.line(
        yearly_monthly,
        x="Month",
        y="Distance (km)",
        color="Year",
        title="Year-over-Year Comparison (Monthly Distance by Year)",
        markers=True,
        labels={"Distance (km)": "Distance (km)"}
    )
    st.plotly_chart(fig_yoy, width='stretch')

    # Personal Records Section
    st.header("🏆 Personal Records")
    pr_col1, pr_col2, pr_col3, pr_col4 = st.columns(4)

    with pr_col1:
        longest_distance = df["Distance (km)"].max()
        st.metric("Longest Distance", f"{int(longest_distance)} km")

    with pr_col2:
        longest_duration = df["Duration (min)"].max()
        st.metric("Longest Duration", f"{int(longest_duration)} min")

    with pr_col3:
        most_elevation = df["Elevation (m)"].max()
        st.metric("Most Elevation", f"{int(most_elevation):,} m")

    with pr_col4:
        fastest_speed = df["Average Speed (km/h)"].max()
        st.metric("Fastest Speed", f"{int(fastest_speed)} km/h")

    # Quarterly Summary Section
    st.header("📊 Quarterly Summary")
    df_quarterly = df.copy()
    df_quarterly["Quarter"] = df_quarterly["Activity Date"].dt.to_period("Q")
    quarterly_stats = df_quarterly.groupby("Quarter").agg({
        "Distance (km)": "sum",
        "Duration (min)": "sum",
        "Elevation (m)": "sum",
        "Activity Type": "count"
    }).reset_index()
    quarterly_stats.columns = ["Quarter", "Total Distance (km)", "Total Duration (min)", "Total Elevation (m)", "Activity Count"]
    quarterly_stats["Total Duration (hours)"] = (quarterly_stats["Total Duration (min)"] / 60).round(1)
    quarterly_stats["Quarter"] = quarterly_stats["Quarter"].astype(str)
    quarterly_stats = quarterly_stats.sort_values("Quarter", ascending=False)

    # Quarterly Distance Bar Chart
    fig_quarterly_distance = px.bar(
        quarterly_stats.sort_values("Quarter"),
        x="Quarter",
        y="Total Distance (km)",
        title="Quarterly Distance Total",
        text="Total Distance (km)"
    )
    fig_quarterly_distance.update_traces(textposition='outside')
    st.plotly_chart(fig_quarterly_distance, width='stretch')

    # Quarterly Stats Table
    st.subheader("Quarterly Statistics")
    st.dataframe(
        quarterly_stats[[
            "Quarter", "Activity Count", "Total Distance (km)", 
            "Total Duration (hours)", "Total Elevation (m)"
        ]].rename(columns={"Quarter": "Quarter"}),
        width='stretch',
        hide_index=True
    )

    # Calendar Heatmap Section
    st.header("📅 Activity Calendar")
    df_calendar = df.copy()
    df_calendar["Date"] = df_calendar["Activity Date"].dt.date
    df_calendar["Week"] = df_calendar["Activity Date"].dt.isocalendar().week
    df_calendar["Day of Week"] = df_calendar["Activity Date"].dt.day_name()
    df_calendar["Year"] = df_calendar["Activity Date"].dt.year

    # Get current year
    current_year = df_calendar["Year"].max()

    # Create daily activity count
    daily_activities = df_calendar[df_calendar["Year"] == current_year].groupby("Date").agg({
        "Distance (km)": "sum",
        "Activity Type": "count"
    }).reset_index()
    daily_activities.columns = ["Date", "Distance (km)", "Activity Count"]

    # Create calendar data for heatmap
    df_cal_heatmap = df_calendar[df_calendar["Year"] == current_year].copy()
    df_cal_heatmap["Week"] = df_cal_heatmap["Activity Date"].dt.isocalendar().week
    df_cal_heatmap["Day"] = df_cal_heatmap["Activity Date"].dt.day_name()

    activity_by_week_day = df_cal_heatmap.groupby(["Week", "Day"]).size().reset_index(name="Activities")

    # Map day names to numbers for proper ordering
    day_order = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
    activity_by_week_day["Day Num"] = activity_by_week_day["Day"].map(day_order)
    activity_by_week_day = activity_by_week_day.sort_values(["Week", "Day Num"])

    # Create heatmap
    fig_heatmap = px.density_heatmap(
        df_cal_heatmap,
        x=df_cal_heatmap["Activity Date"].dt.isocalendar().week,
        y=df_cal_heatmap["Activity Date"].dt.day_name(),
        title=f"Activity Heatmap - {current_year}",
        nbinsx=53,
        color_continuous_scale="Greens",
        labels={"x": "Week of Year", "y": "Day of Week"}
    )
    st.plotly_chart(fig_heatmap, width='stretch')
