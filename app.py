"""Main Streamlit application for Roast My Activity Data.

This is the entry point for the activity analytics dashboard.
Run with: streamlit run app.py
"""

import pandas as pd
import streamlit as st
from datetime import datetime

from src.config import (
    APP_TITLE, CUSTOM_CSS, DEFAULT_DAYS_BACK, 
    MIN_DAYS_BACK, MAX_DAYS_BACK, DATA_FILE_PATH,
    PLOTLY_LIGHT_THEME, PLOTLY_DARK_THEME, VERSION,
    ACTIVITY_GROUP_MAP
)
from src.data_loader import (
    load_strava_data, filter_by_activities, 
    filter_by_date_range, get_quarterly_stats, get_monthly_trends,
    get_aggregated_trends, get_stacked_activity_data,
    get_time_of_day_stats, get_hourly_activity_distribution, get_day_hour_heatmap_data
)
from src.utils import (
    calculate_fun_metrics, calculate_cheeky_metrics, get_personal_records, 
    calculate_summary_stats, format_metric_display, calculate_exercise_obsession_score,
    get_races, get_best_race_times, is_race
)
from src.visualizations_altair import (
    create_distance_timeline, create_activity_type_pie,
    create_duration_histogram, create_cumulative_distance_chart,
    create_activity_trends_chart, create_stacked_activity_chart,
    create_activity_heatmap, create_exercise_obsession_gauge,
    create_time_of_day_pie, create_hourly_activity_chart,
    create_day_hour_heatmap, create_time_performance_chart
)


def setup_page():
    """Configure Streamlit page settings and custom styling."""
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Inject JavaScript to detect system dark mode preference
    st.markdown("""
        <script>
            const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            const streamlitDoc = window.parent.document;
            
            function updateDarkModeIndicator(isDark) {
                // Store in localStorage so we can detect it
                localStorage.setItem('prefersDarkMode', isDark ? 'true' : 'false');
                // Add a class to body for CSS detection
                if (isDark) {
                    streamlitDoc.body.classList.add('system-dark-mode');
                } else {
                    streamlitDoc.body.classList.remove('system-dark-mode');
                }
            }
            
            // Initial check
            updateDarkModeIndicator(darkModeMediaQuery.matches);
            
            // Listen for changes
            darkModeMediaQuery.addEventListener('change', (e) => {
                updateDarkModeIndicator(e.matches);
            });
        </script>
    """, unsafe_allow_html=True)
    
    st.title(APP_TITLE)


def detect_dark_mode():
    """Detect if user has dark mode enabled.
    
    Returns:
        Dict containing theme colors for plotly charts.
    """
    # Check if dark mode query param exists or use default detection
    query_params = st.query_params
    
    # Use JavaScript to detect system preference (fallback to light mode)
    dark_mode_js = """
    <script>
        const darkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (darkMode) {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
        }
    </script>
    """
    
    # For simplicity, check session state or default to light
    # Users can toggle via browser dark mode settings
    if 'theme' not in st.session_state:
        st.session_state.theme = PLOTLY_LIGHT_THEME
    
    return st.session_state.theme


def create_sidebar_filters(df):
    """Create sidebar filters for data analysis.
    
    Args:
        df: DataFrame containing activity data.
        
    Returns:
        Tuple of (days_back, selected_activities, time_interval, theme) filter values.
    """
    # Date range slider
    days_back = st.sidebar.slider(
        "Last N Days for Recent Activity Stats",
        MIN_DAYS_BACK,
        MAX_DAYS_BACK,
        DEFAULT_DAYS_BACK
    )
    
    # Initialize preset state
    if 'activity_preset' not in st.session_state:
        st.session_state.activity_preset = "jackofall"
    
    # Activity mode selector
    mode_options = {
        "🎯 All Rounder": "jackofall",
        "🏃 Runner": "runner",
        "🥾 Hiker": "hiker",
        "🚴 Cyclist": "cyclist",
        "🏊 Swimmer": "swimmer",
        "🏋️ Gym Rat": "gym",
        "🏅 Triathlete": "triathlete",
        "❄️ Snowflake": "snowflake",
        "⚽ Team Player": "teamplayer"
    }
    
    selected_mode = st.sidebar.selectbox(
        "Activity Profile",
        options=list(mode_options.keys()),
        index=0  # Default to Jack of All
    )
    
    st.session_state.activity_preset = mode_options[selected_mode]
    
    # Preset mappings
    presets = {
        "runner": ["Running"],
        "hiker": ["Hiking", "Walking"],
        "cyclist": ["Cycling"],
        "swimmer": ["Swimming"],
        "gym": ["Strength"],
        "triathlete": ["Running", "Cycling", "Swimming"],
        "snowflake": ["Winter Sports"],
        "teamplayer": ["Team Sports"],
        "jackofall": None  # None means all activities
    }
    
    # Activity type filter with expander
    available_activity_groups = sorted(df["Activity Group"].unique())
    
    # Determine selected activities based on preset
    if st.session_state.activity_preset and st.session_state.activity_preset in presets:
        preset_activities = presets[st.session_state.activity_preset]
        if preset_activities is None:  # Jack of All
            selected_activities = available_activity_groups
        else:
            selected_activities = [act for act in preset_activities if act in available_activity_groups]
            if not selected_activities:
                selected_activities = available_activity_groups
    else:
        selected_activities = available_activity_groups
    
    # Time series interval selector
    time_interval = st.sidebar.selectbox(
        "Time Series Interval",
        options=["monthly", "quarterly", "annual", "alltime"],
        format_func=lambda x: {
            "monthly": "Monthly",
            "quarterly": "Quarterly", 
            "annual": "Annual",
            "alltime": "All Time"
        }[x],
        index=1,  # Default to quarterly
        help="Choose how to group activities in time series charts"
    )
    
    # Theme selector - try to detect Streamlit's theme or URL param
    # Check URL param first (e.g., ?dark=1)
    query_params = st.query_params
    url_dark = query_params.get("dark", "0") == "1"
    
    # Then check Streamlit's theme config
    try:
        streamlit_theme = st.get_option("theme.base")
        config_dark = streamlit_theme == "dark"
    except:
        config_dark = False
    
    # Default to URL param, then config, then False
    default_dark = url_dark or config_dark
    
    # Initialize session state for dark mode if not set
    if "use_dark_mode" not in st.session_state:
        st.session_state.use_dark_mode = default_dark
    
    use_dark_mode = st.sidebar.checkbox(
        "🌙 Dark Mode", 
        value=st.session_state.use_dark_mode, 
        help="Toggle dark mode for charts. Tip: Add ?dark=1 to URL for auto dark mode",
        key="dark_mode_toggle"
    )
    st.session_state.use_dark_mode = use_dark_mode
    
    theme = PLOTLY_DARK_THEME if use_dark_mode else PLOTLY_LIGHT_THEME
    st.session_state.theme = theme
    
    return days_back, selected_activities, time_interval, theme


def render_summary_metrics(stats, col_config=None, round_to_whole=False):
    """Render summary metrics in columns.
    
    Args:
        stats: Dictionary of statistics to display.
        col_config: Optional list of (label, key, format) tuples.
        round_to_whole: If True, rounds distance and duration to whole numbers instead of 1 decimal place.
    """
    if col_config is None:
        col_config = [
            ("Total Activities", "total_activities", ","),
            ("Total Distance", "total_distance", ",.1f"),
            ("Total Duration", "total_duration", ",.1f"),
            ("Total Elevation", "total_elevation", ",")
        ]
    
    cols = st.columns(len(col_config))
    for col, (label, key, fmt) in zip(cols, col_config):
        with col:
            if key in stats:
                value = stats[key]
                if fmt == ",":
                    # Add unit for elevation metrics
                    unit = " m" if "Elevation" in label else ""
                    st.metric(label, f"{int(value):,}{unit}")
                elif fmt == ",.1f":
                    # Determine unit based on label
                    unit = "hrs" if "Duration" in label else "km"
                    
                    if round_to_whole:
                        # Round to whole number with comma separator for thousands
                        st.metric(label, f"{int(round(value)):,} {unit}")
                    else:
                        # Keep 1 decimal place
                        st.metric(label, f"{value:.1f} {unit}")
                else:
                    st.metric(label, f"{int(value):,} m")


def render_recent_activity_tab(df_filtered, days_back, theme):
    """Render the Recent Activity tab content.
    
    Args:
        df_filtered: Filtered DataFrame for recent period.
        days_back: Number of days in the filter.
        theme: Dict containing theme colors for charts.
    """
    st.subheader(f"Last {days_back} Days")
    
    # Summary metrics
    stats = calculate_summary_stats(df_filtered)
    render_summary_metrics(stats)
    
    # Races count
    races = get_races(df_filtered)
    if len(races) > 0:
        st.metric("🏁 Races in Period", f"{len(races):,}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_distance = create_distance_timeline(df_filtered, theme=theme)
        st.altair_chart(fig_distance, width='stretch')
    
    with col2:
        fig_type = create_activity_type_pie(df_filtered, theme=theme)
        st.altair_chart(fig_type, width='stretch')
    
    # Duration distribution
    fig_duration = create_duration_histogram(df_filtered, theme=theme)
    st.altair_chart(fig_duration, width='stretch')
    
    # Recent activities table
    st.subheader("Recent Activities")
    
    # Create formatted dataframe for display
    temp_df = df_filtered.sort_values("Activity Date", ascending=False)[[
        "Activity Date", "Activity Type", "Activity Group", "Distance (km)", 
        "Duration (min)", "Elevation (m)", "Average Speed (km/h)"
    ]].copy()
    
    # Calculate pace/speed based on activity type
    def format_pace_speed(row):
        activity_group = row["Activity Group"]
        speed_kmh = row["Average Speed (km/h)"]
        
        # Use pace for Running and Hiking
        if activity_group in ["Running", "Hiking"] and speed_kmh > 0:
            pace_min_per_km = 60 / speed_kmh
            mins = int(pace_min_per_km)
            secs = int((pace_min_per_km - mins) * 60)
            return f"{mins}:{secs:02d} /km"
        # Use speed for other activities
        elif speed_kmh > 0:
            return f"{speed_kmh:.1f} km/h"
        else:
            return "-"
    
    temp_df["Pace/Speed"] = temp_df.apply(format_pace_speed, axis=1)
    
    # Select and reorder columns for display
    display_df = temp_df[[
        "Activity Date", "Activity Type", "Distance (km)", 
        "Duration (min)", "Elevation (m)", "Pace/Speed"
    ]].copy()
    
    # Format numeric columns
    display_df["Distance (km)"] = display_df["Distance (km)"].apply(lambda x: f"{x:,.1f}")
    display_df["Duration (min)"] = display_df["Duration (min)"].apply(lambda x: f"{x:,.0f}")
    display_df["Elevation (m)"] = display_df["Elevation (m)"].apply(lambda x: f"{x:,.0f}")
    
    st.dataframe(
        display_df,
        width='stretch',
        hide_index=True
    )
    
    # Time of Day Analysis
    st.markdown("---")
    st.subheader("⏰ Time of Day Analysis")
    
    # Check if time of day data is available
    if "Time of Day" in df_filtered.columns and "Hour of Day" in df_filtered.columns:
        time_stats = get_time_of_day_stats(df_filtered)
        
        if time_stats and time_stats.get('counts'):
            # Time of day metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "🌅 Most Active Time",
                    time_stats['most_active'],
                    help="Time of day when you do the most activities"
                )
            
            with col2:
                morning_count = time_stats['counts'].get('Morning', 0)
                st.metric(
                    "🌄 Morning Activities",
                    f"{morning_count}",
                    help="Activities between 5am-12pm"
                )
            
            with col3:
                evening_count = time_stats['counts'].get('Evening', 0)
                st.metric(
                    "🌆 Evening Activities",
                    f"{evening_count}",
                    help="Activities between 5pm-9pm"
                )
            
            # Time of day visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                fig_time_pie = create_time_of_day_pie(df_filtered, theme=theme)
                if fig_time_pie:
                    st.altair_chart(fig_time_pie, width='stretch')
            
            with col2:
                fig_performance = create_time_performance_chart(df_filtered, theme=theme)
                if fig_performance:
                    st.altair_chart(fig_performance, width='stretch')
            
            # Hourly distribution
            hourly_data = get_hourly_activity_distribution(df_filtered)
            if len(hourly_data) > 0:
                fig_hourly = create_hourly_activity_chart(hourly_data, theme=theme)
                if fig_hourly:
                    st.altair_chart(fig_hourly, width='stretch')
            
            # Day-hour heatmap
            heatmap_data = get_day_hour_heatmap_data(df_filtered)
            if len(heatmap_data) > 0:
                fig_heatmap = create_day_hour_heatmap(heatmap_data, theme=theme)
                if fig_heatmap:
                    st.altair_chart(fig_heatmap, width='stretch')
        else:
            st.info("Time of day data not available for these activities.")
    else:
        st.info("Time of day data not available. Make sure your activity data includes 'Start Time' information.")
    
    # Races table
    st.markdown("---")
    st.subheader("🏁 Races")
    races = get_races(df_filtered)
    
    if len(races) > 0:
        # Show race count
        st.metric("Total Races", f"{len(races)}")
        
        # Format the display
        races_display = races.copy()
        races_display["Date"] = races_display["Date"].dt.strftime("%Y-%m-%d")
        races_display["Distance (km)"] = races_display["Distance (km)"].apply(lambda x: f"{x:,.1f}")
        
        st.dataframe(
            races_display,
            width='stretch',
            hide_index=True
        )
    else:
        st.info("No races found in this time period.")


def render_fun_metrics(metrics):
    """Render fun comparative metrics.
    
    Args:
        metrics: Dictionary of fun metrics from calculate_fun_metrics.
    """
    st.markdown("")  # Spacing
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "📅 Activities/Week",
            f"{metrics['activities_per_week']:.1f}",
            help=f"Average per week across your entire activity history ({int(metrics['total_activities']):,} activities)"
        )
    
    with col2:
        display, help_text = format_metric_display(metrics['days_active'], 'time')
        st.metric("⏱️ Time Active", display, help=help_text)


def render_cheeky_metrics(cheeky):
    """Render cheeky alternative datapoints.
    
    Args:
        cheeky: Dictionary of cheeky metrics from calculate_cheeky_metrics.
    """
    st.markdown("---")
    st.subheader("📏 In Perspective")
    
    # Distance achievements
    st.markdown("#### 🏃 Distance Hall of Fame")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🍌 In Bananas",
            f"{cheeky['bananas']:,.0f}",
            help="If you laid 18cm bananas end to end (USDA)"
        )
    
    with col2:
        st.metric(
            "⚽ Football Pitches",
            f"{cheeky['football_pitches']:,.0f}",
            help="Standard pitch length: 105m (FIFA/Premier League)"
        )
    
    with col3:
        st.metric(
            "🏃‍♂️ Marathons",
            f"{cheeky['marathons']:,.0f}",
            help="Official marathon distance: 42.195 km (IAAF)"
        )
    
    with col4:
        if cheeky['faster_than_sloth'] >= 1:
            st.metric(
                "🦥 vs Sloth Speed",
                f"{cheeky['faster_than_sloth']:,.0f}x faster",
                help="A sloth would take this many times longer to cover your distance (Nat Geo: 0.24 km/h)"
            )
        else:
            st.metric(
                "⚡ Bolt Speed",
                f"{cheeky['percent_of_bolt']:.1f}%",
                help="Your avg speed vs Usain Bolt's 100m WR pace (IAAF: 44.72 km/h)"
            )
    
    # Elevation achievements
    st.markdown("#### 🗼 Climbing the Leaderboard")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🗼 Eiffel Towers",
            f"{cheeky['eiffel_towers']:,.0f}",
            help="330m to the tip (Paris official height)"
        )
    
    with col2:
        st.metric(
            "🏙️ Empire States",
            f"{cheeky['empire_states']:,.0f}",
            help="443m to roof (ESB official)"
        )
    
    with col3:
        st.metric(
            "🏗️ Burj Khalifas",
            f"{cheeky['burj_khalifas']:,.0f}",
            help="828m - World's tallest building (Emaar)"
        )
    
    # Food
    st.markdown("#### 🍕 You Earned It")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🍔 Big Macs",
            f"{cheeky['big_macs']:,.0f}",
            help="Calories burned (~50 cal/km) ÷ Big Mac calories (McDonald's: 563 cal)"
        )
    
    with col2:
        st.metric(
            "🍕 Pizza Slices",
            f"{cheeky['pizza_slices']:,.0f}",
            help="Large pepperoni, 1/8 pizza (USDA: 285 cal/slice)"
        )
    
    with col3:
        st.metric(
            "🍺 Beers",
            f"{cheeky['beers']:,.0f}",
            help="Standard 12oz beers (USDA avg: 150 cal)"
        )
    
    # Entertainment
    st.markdown("#### 🎬 Entertainment Equivalents")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "📺 Friends Episodes",
            f"{cheeky['friends_episodes']:,.0f}",
            help="22-min episodes you could've watched instead (NBC avg runtime)"
        )
    
    with col2:
        if cheeky['lotr_trilogies'] >= 1:
            st.metric(
                "🧙‍♂️ LOTR Extended Trilogies",
                f"{cheeky['lotr_trilogies']:,.0f}",
                help="558 min total for extended trilogy (New Line Cinema)"
            )
        else:
            pct = cheeky['lotr_trilogies'] * 100
            st.metric(
                "🧙‍♂️ Through LOTR Trilogy",
                f"{pct:.0f}%",
                help="Progress through extended trilogy"
            )


def render_fun_tab(df, theme=None):
    """Render the Just for Fun tab content.
    
    Args:
        df: Full DataFrame containing all activity data.
        theme: Dict containing theme colors for charts.
    """
    if theme is None:
        theme = PLOTLY_LIGHT_THEME
    
    # Exercise obsession meter
    st.header("🔥 Exercise-oholic Meter")
    obsession_score, obsession_level, obsession_desc = calculate_exercise_obsession_score(df)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        fig_gauge = create_exercise_obsession_gauge(obsession_score, obsession_level, theme=theme)
        st.altair_chart(fig_gauge, width='stretch')
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"### Your Diagnosis")
        st.markdown(f"**Score:** {obsession_score}/100")
        st.markdown(f"**Level:** {obsession_level}")
        st.markdown(f"*{obsession_desc}*")
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("📊 Based on frequency, volume, consistency, variety, and dedication")
    
    # Cheeky alternative metrics
    st.markdown("---")
    cheeky_metrics = calculate_cheeky_metrics(df)
    render_cheeky_metrics(cheeky_metrics)


def render_help_tab():
    """Render the Help/Instructions tab content."""
    st.header("❓ Help & Instructions")
    
    # Introduction
    st.markdown("""
    Welcome to the Roast My Activity Data dashboard! This page explains how your activities 
    are categorized and provides helpful information about using the app.
    """)
    
    st.markdown("---")
    
    # Activity Type Mapping Section
    st.subheader("🏃 Activity Type Mapping")
    
    st.markdown("""
    Your activity data from Strava contains specific activity types (like "Run", "Ride", "Swim", etc.). 
    This app groups these into broader categories for easier analysis and visualization.
    
    Below is the complete mapping showing how each Strava activity type is categorized:
    """)
    
    # Create a structured display of the mapping
    # Group by Activity Group for better organization
    grouped_mapping = {}
    for activity_type, group in ACTIVITY_GROUP_MAP.items():
        if group not in grouped_mapping:
            grouped_mapping[group] = []
        grouped_mapping[group].append(activity_type)
    
    # Display each group with its mappings - first 3 expanded, rest collapsed for better UX
    sorted_groups = sorted(grouped_mapping.keys())
    for idx, group in enumerate(sorted_groups):
        with st.expander(f"**{group}**", expanded=(idx < 3)):
            activities = sorted(grouped_mapping[group])
            st.markdown("**Includes:**")
            for activity in activities:
                st.markdown(f"- {activity}")
    
    st.markdown("---")
    
    # Activity Profile Explanation
    st.subheader("🎯 Activity Profiles")
    
    st.markdown("""
    Activity Profiles help you quickly filter and analyze specific types of activities. Choose a profile from the sidebar to focus your analysis:
    
    - **🎯 All Rounder**: View all your activities across every sport (default)
    - **🏃 Runner**: Focus on running activities only
    - **🥾 Hiker**: Analyze hiking and walking activities
    - **🚴 Cyclist**: See cycling-specific metrics and stats
    - **🏊 Swimmer**: Filter to swimming activities
    - **🏋️ Gym Rat**: Focus on strength training and workouts
    - **🏅 Triathlete**: View running, cycling, and swimming combined
    - **❄️ Snowflake**: Analyze winter sports (skiing, snowboarding)
    - **⚽ Team Player**: Focus on team sports activities
    
    Each profile automatically filters your activities to show relevant data and optimizes the dashboard for that sport type.
    """)
    
    st.markdown("---")
    
    # Quick Tips Section
    st.subheader("💡 Quick Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Filtering Activities**
        - Use the sidebar to select which activity groups to include
        - Uncheck groups you want to exclude from your analysis
        - Changes apply to all tabs instantly
        
        **Time Ranges**
        - The "Recent Activity" tab uses the date slider
        - The "All-Time Analysis" tab shows your complete history
        - Adjust the slider to focus on specific periods
        """)
    
    with col2:
        st.markdown("""
        **Understanding Charts**
        - Hover over chart elements for detailed information
        - Click legend items to show/hide specific categories
        - Most charts are interactive and zoomable
        
        **Data Privacy**
        - All data stays in your browser session
        - Nothing is stored on servers
        - Your activities remain completely private
        """)
    
    st.markdown("---")
    
    # Getting Started Section
    st.subheader("🚀 Getting Started")
    
    st.markdown("""
    **How to use this app:**
    
    1. **Upload Your Data**: Use the file uploader to load your Strava `activities.csv` file
    2. **Explore Tabs**: Navigate between Recent Activity, All-Time Analysis, and Just for Fun
    3. **Filter & Analyze**: Use sidebar controls to customize your view
    4. **Discover Insights**: Check out your personal records, trends, and fun metrics!
    
    **Need your Strava data?**
    1. Go to [Strava.com](https://www.strava.com/) → Settings → My Account
    2. Click "Download or Delete Your Account"
    3. Request your data export
    4. Wait for email (usually arrives within a few hours)
    5. Extract the ZIP file and upload `activities.csv` to this app
    """)
    
    st.markdown("---")
    
    # Additional Resources
    st.subheader("📚 Additional Resources")
    
    st.markdown("""
    - **Full Documentation**: Check out the [USAGE.md](https://github.com/tolliam/roast-my-activity-data/blob/main/docs/USAGE.md) guide for detailed instructions
    - **Report Issues**: Found a bug? [Open an issue on GitHub](https://github.com/tolliam/roast-my-activity-data/issues)
    - **Contribute**: Want to help improve the app? See our [Contributing Guide](https://github.com/tolliam/roast-my-activity-data/blob/main/CONTRIBUTING.md)
    """)


def render_alltime_tab(df, time_interval="quarterly", theme=None):
    """Render the All-Time Analysis tab content.
    
    Args:
        df: Full DataFrame containing all activity data.
        time_interval: Time interval for aggregating time series data.
        theme: Dict containing theme colors for charts.
    """
    if theme is None:
        theme = PLOTLY_LIGHT_THEME
    
    # All-time summary metrics
    stats = calculate_summary_stats(df)
    render_summary_metrics(stats, round_to_whole=True)
    
    # Epic achievement metrics
    st.markdown("")
    fun_metrics = calculate_fun_metrics(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📅 Activities/Week",
            f"{fun_metrics['activities_per_week']:.1f}",
            help=f"Average per week across your entire activity history ({int(fun_metrics['total_activities']):,} activities)"
        )
    
    with col2:
        display, help_text = format_metric_display(fun_metrics['times_around_world'], 'earth')
        st.metric("🌍 Around Earth", display, help=help_text)
    
    with col3:
        display, help_text = format_metric_display(fun_metrics['days_active'], 'time')
        st.metric("⏱️ Time Active", display, help=help_text)
    
    with col4:
        display, help_text = format_metric_display(fun_metrics['times_up_everest'], 'everest')
        st.metric("🏔️ Up Mt Everest", display, help=help_text)
    
    st.markdown("---")
    
    # Get trend data based on selected interval
    period_data = get_aggregated_trends(df, time_interval)
    stacked_data = get_stacked_activity_data(df, time_interval)
    
    # Time series charts - only show if not alltime single point
    if time_interval != "alltime":
        # Cumulative distance chart
        fig_cumulative = create_cumulative_distance_chart(period_data, interval=time_interval, theme=theme)
        if fig_cumulative:
            st.altair_chart(fig_cumulative, width='stretch')
        
        # Trends chart
        fig_trends = create_activity_trends_chart(period_data, interval=time_interval, theme=theme)
        if fig_trends:
            st.altair_chart(fig_trends, width='stretch')
        
        # Stacked activity chart
        fig_stacked = create_stacked_activity_chart(stacked_data, interval=time_interval, theme=theme)
        if fig_stacked:
            st.altair_chart(fig_stacked, width='stretch')
        else:
            st.info("Activity composition chart requires multiple time periods")
    else:
        st.info("📊 Select a time interval (Monthly, Quarterly, or Annual) from the sidebar to view time series charts")
    
    # Personal records
    st.header("🏆 Personal Records")
    prs = get_personal_records(df)
    pr_cols = st.columns(4)
    
    with pr_cols[0]:
        distance = prs['longest_distance']
        st.metric("Longest Distance", f"{int(distance) if not pd.isna(distance) else 0} km")
    with pr_cols[1]:
        duration = prs['longest_duration']
        if not pd.isna(duration):
            hours = int(duration // 60)
            mins = int(duration % 60)
            st.metric("Longest Duration", f"{hours}h {mins}m")
        else:
            st.metric("Longest Duration", "0h 0m")
    with pr_cols[2]:
        elevation = prs['most_elevation']
        st.metric("Most Elevation", f"{int(elevation) if not pd.isna(elevation) else 0:,} m")
    with pr_cols[3]:
        speed = prs['fastest_speed']
        st.metric("Fastest Speed", f"{int(speed) if not pd.isna(speed) else 0} km/h")
    
    # Show best race times for runner mode
    if 'activity_preset' in st.session_state and st.session_state.activity_preset == "runner":
        st.markdown("")
        st.subheader("🏃 Best Race Times")
        best_times = get_best_race_times(df)
        
        race_cols = st.columns(4)
        
        with race_cols[0]:
            if best_times['5k']:
                st.metric("5K", best_times['5k']['time_formatted'], 
                         help=f"{best_times['5k']['name']} on {best_times['5k']['date'].strftime('%Y-%m-%d')}")
            else:
                st.metric("5K", "N/A", help="No 5K races found")
        
        with race_cols[1]:
            if best_times['10k']:
                st.metric("10K", best_times['10k']['time_formatted'],
                         help=f"{best_times['10k']['name']} on {best_times['10k']['date'].strftime('%Y-%m-%d')}")
            else:
                st.metric("10K", "N/A", help="No 10K races found")
        
        with race_cols[2]:
            if best_times['half']:
                st.metric("Half Marathon", best_times['half']['time_formatted'],
                         help=f"{best_times['half']['name']} on {best_times['half']['date'].strftime('%Y-%m-%d')}")
            else:
                st.metric("Half Marathon", "N/A", help="No half marathon races found")
        
        with race_cols[3]:
            if best_times['marathon']:
                st.metric("Marathon", best_times['marathon']['time_formatted'],
                         help=f"{best_times['marathon']['name']} on {best_times['marathon']['date'].strftime('%Y-%m-%d')}")
            else:
                st.metric("Marathon", "N/A", help="No marathon races found")
    
    # Time of Day Analysis (All-Time)
    st.markdown("---")
    st.header("⏰ Time of Day Patterns")
    
    if "Time of Day" in df.columns and "Hour of Day" in df.columns:
        time_stats = get_time_of_day_stats(df)
        
        if time_stats and time_stats.get('counts'):
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "🌅 Most Active Time",
                    time_stats['most_active'],
                    help="Time of day when you do the most activities"
                )
            
            with col2:
                morning_count = time_stats['counts'].get('Morning', 0)
                morning_pct = (morning_count / len(df) * 100) if len(df) > 0 else 0
                st.metric(
                    "🌄 Morning Activities",
                    f"{morning_count}",
                    delta=f"{morning_pct:.1f}%",
                    help="Activities between 5am-12pm"
                )
            
            with col3:
                afternoon_count = time_stats['counts'].get('Afternoon', 0)
                afternoon_pct = (afternoon_count / len(df) * 100) if len(df) > 0 else 0
                st.metric(
                    "☀️ Afternoon Activities",
                    f"{afternoon_count}",
                    delta=f"{afternoon_pct:.1f}%",
                    help="Activities between 12pm-5pm"
                )
            
            with col4:
                evening_count = time_stats['counts'].get('Evening', 0)
                evening_pct = (evening_count / len(df) * 100) if len(df) > 0 else 0
                st.metric(
                    "🌆 Evening Activities",
                    f"{evening_count}",
                    delta=f"{evening_pct:.1f}%",
                    help="Activities between 5pm-9pm"
                )
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                fig_time_pie = create_time_of_day_pie(df, title="All-Time Activity Distribution by Time of Day", theme=theme)
                if fig_time_pie:
                    st.altair_chart(fig_time_pie, width='stretch')
            
            with col2:
                fig_performance = create_time_performance_chart(df, title="Average Performance by Time of Day", theme=theme)
                if fig_performance:
                    st.altair_chart(fig_performance, width='stretch')
            
            # Hourly distribution
            hourly_data = get_hourly_activity_distribution(df)
            if len(hourly_data) > 0:
                fig_hourly = create_hourly_activity_chart(hourly_data, title="All-Time Hourly Activity Distribution", theme=theme)
                if fig_hourly:
                    st.altair_chart(fig_hourly, width='stretch')
            
            # Day-hour heatmap
            heatmap_data = get_day_hour_heatmap_data(df)
            if len(heatmap_data) > 0:
                fig_heatmap = create_day_hour_heatmap(heatmap_data, title="Weekly Activity Pattern: When Do You Work Out?", theme=theme)
                if fig_heatmap:
                    st.altair_chart(fig_heatmap, width='stretch')
        else:
            st.info("Time of day data not available.")
    else:
        st.info("Time of day data not available. Make sure your activity data includes 'Start Time' information.")
    
    # Calendar heatmap
    st.markdown("---")
    st.header("📅 Activity Calendar")
    
    # Get all years with data
    available_years = sorted(df["Activity Date"].dt.year.unique(), reverse=True)
    
    # Year selector with toggle buttons
    selected_year = st.radio(
        "Select year",
        options=available_years,
        horizontal=True,
        label_visibility="collapsed"
    )
    
    fig_heatmap = create_activity_heatmap(df, selected_year, theme=theme)
    st.altair_chart(fig_heatmap, width='stretch')
    
    # Races table
    st.header("🏁 Races")
    races = get_races(df)
    
    if len(races) > 0:
        # Show race count above table
        st.metric("Total Races", f"{len(races):,}")
        
        # Format the display based on mode
        races_display = races.copy()
        races_display["Date"] = races_display["Date"].dt.strftime("%Y-%m-%d")
        races_display["Distance (km)"] = races_display["Distance (km)"].apply(lambda x: f"{x:,.1f}")
        
        # Add pace or speed based on mode
        if 'activity_preset' in st.session_state and st.session_state.activity_preset == "runner":
            # Calculate pace in min/km for runners
            # Get the original data to calculate pace
            races_with_data = df[df.apply(
                lambda row: is_race(row.get('Activity Name', ''), row.get('Activity Description', '')),
                axis=1
            )].copy()
            
            if len(races_with_data) > 0:
                # Calculate pace: time in seconds / distance in km = seconds per km, then convert to min/km
                time_col = 'Elapsed Time' if 'Elapsed Time' in races_with_data.columns else 'Time'
                races_with_data['Pace (min/km)'] = races_with_data[time_col] / races_with_data['Distance (km)'] / 60
                
                # Format pace as MM:SS
                def format_pace(pace_mins):
                    if pd.isna(pace_mins) or pace_mins <= 0:
                        return "N/A"
                    minutes = int(pace_mins)
                    seconds = int((pace_mins - minutes) * 60)
                    return f"{minutes}:{seconds:02d}"
                
                races_display['Pace'] = races_with_data['Pace (min/km)'].apply(format_pace).values
        elif 'activity_preset' in st.session_state and st.session_state.activity_preset == "cyclist":
            # Show speed in km/h for cyclists
            races_with_data = df[df.apply(
                lambda row: is_race(row.get('Activity Name', ''), row.get('Activity Description', '')),
                axis=1
            )].copy()
            
            if len(races_with_data) > 0 and 'Average Speed (km/h)' in races_with_data.columns:
                races_display['Speed (km/h)'] = races_with_data['Average Speed (km/h)'].apply(lambda x: f"{x:,.1f}").values
        
        st.dataframe(
            races_display,
            width='stretch',
            hide_index=True
        )
    else:
        st.info("No races found in your activity history.")


def main():
    """Main application entry point."""
    # Setup page
    setup_page()
    
    # Initialize session state for data
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    
    # Show data source selection if data not loaded
    if not st.session_state.data_loaded:
        st.markdown("### Welcome! Let's get started with your activity data")
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📁 Upload Your Data")
            st.markdown("Upload your Strava activities CSV file")
            uploaded_file = st.file_uploader(
                "Choose a CSV file",
                type=['csv'],
                help="Export your activities from Strava and upload the CSV file here",
                label_visibility="collapsed"
            )
            
            if uploaded_file is not None:
                with st.spinner("Loading your data..."):
                    try:
                        st.session_state.df = load_strava_data(uploaded_file)
                        st.session_state.data_loaded = True
                    except Exception as e:
                        st.error(f"Error loading uploaded file: {str(e)}")
                        st.info("Please ensure your CSV has the required columns")
                        return
            
            st.markdown("""
            **How to get your Strava data:**
            1. Go to [Strava.com](https://www.strava.com/) → Settings → My Account
            2. Scroll to **"Download or Delete Your Account"** section
            3. Click **"Get Started"** under "Request Your Archive"
            4. Confirm by clicking **"Request Your Archive"**
            5. Wait for email (can take a few hours to 7 days)
            6. Download and extract the ZIP file from the email
            7. Upload the **activities.csv** file here
            """)
        
        with col2:
            st.markdown("#### 📊 Use Demo Data")
            st.markdown("Try the app with sample data")
            if st.button("Load Demo Data", width='stretch', type="primary"):
                with st.spinner("Loading demo data..."):
                    try:
                        st.session_state.df = load_strava_data(DATA_FILE_PATH)
                        st.session_state.data_loaded = True
                    except FileNotFoundError:
                        st.error(f"Demo data file not found: {DATA_FILE_PATH}")
                        st.info("Please upload your own CSV file using the option on the left")
                    except Exception as e:
                        st.error(f"Error loading demo data: {str(e)}")
        
        # If data was just loaded, rerun to show the dashboard
        if st.session_state.data_loaded:
            st.rerun()
        
        return
    
    # Data is loaded, show the main app
    df = st.session_state.df
    
    # Add button to change data source in sidebar
    with st.sidebar:
        st.title("⚙️ Settings")
        if st.button("📁 Change Data", width='stretch'):
            st.session_state.data_loaded = False
            st.session_state.df = None
            st.rerun()
    
    # Create sidebar filters
    days_back, selected_activities, time_interval, theme = create_sidebar_filters(df)
    
    # Apply filters
    df = filter_by_activities(df, selected_activities)
    df_filtered = filter_by_date_range(df, days_back)
    
    # Create tabs
    tab_recent, tab_alltime, tab_fun, tab_help = st.tabs(["📊 Recent Activity", "🏆 All-Time Analysis", "🎉 Just for Fun", "❓ Help"])
    
    with tab_recent:
        render_recent_activity_tab(df_filtered, days_back, theme)
    
    with tab_alltime:
        render_alltime_tab(df, time_interval, theme)
    
    with tab_fun:
        render_fun_tab(df, theme)
    
    with tab_help:
        render_help_tab()
    
    # Footer bar with version
    st.markdown("---")
    st.markdown(f"<div style='text-align: center; padding: 10px; font-size: 0.8rem;'>v{VERSION}</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
