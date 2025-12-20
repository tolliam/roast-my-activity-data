"""Main Streamlit application for Roast My Activity Data.

This is the entry point for the activity analytics dashboard.
Run with: streamlit run app.py
"""

import streamlit as st
from datetime import datetime

from src.config import (
    APP_TITLE, CUSTOM_CSS, DEFAULT_DAYS_BACK, 
    MIN_DAYS_BACK, MAX_DAYS_BACK, DATA_FILE_PATH
)
from src.data_loader import (
    load_strava_data, filter_by_activities, 
    filter_by_date_range, get_quarterly_stats, get_monthly_trends
)
from src.utils import (
    calculate_fun_metrics, calculate_cheeky_metrics, get_personal_records, 
    calculate_summary_stats, format_metric_display, calculate_exercise_obsession_score
)
from src.visualizations import (
    create_distance_timeline, create_activity_type_pie,
    create_duration_histogram, create_cumulative_distance_chart,
    create_quarterly_trends_chart, create_stacked_activity_chart,
    create_quarterly_bar_chart, create_activity_heatmap, create_exercise_obsession_gauge
)


def setup_page():
    """Configure Streamlit page settings and custom styling."""
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.title(APP_TITLE)


def create_sidebar(df):
    """Create sidebar with filters and settings.
    
    Args:
        df: DataFrame containing activity data.
        
    Returns:
        Tuple of (days_back, selected_activities) filter values.
    """
    st.sidebar.header("Settings")
    
    # Date range slider
    days_back = st.sidebar.slider(
        "Show activities from last N days",
        MIN_DAYS_BACK,
        MAX_DAYS_BACK,
        DEFAULT_DAYS_BACK
    )
    
    # Activity type filter
    available_activity_groups = sorted(df["Activity Group"].unique())
    selected_activities = st.sidebar.multiselect(
        "Filter by Activity Type",
        options=available_activity_groups,
        default=available_activity_groups,
        max_selections=6
    )
    
    return days_back, selected_activities


def render_summary_metrics(stats, col_config=None):
    """Render summary metrics in columns.
    
    Args:
        stats: Dictionary of statistics to display.
        col_config: Optional list of (label, key, format) tuples.
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
                    st.metric(label, f"{int(value):,}")
                elif fmt == ",.1f":
                    if "Duration" in label:
                        st.metric(label, f"{value:.1f} hrs")
                    else:
                        st.metric(label, f"{value:.1f} km")
                else:
                    st.metric(label, f"{int(value):,} m")


def render_recent_activity_tab(df_filtered, days_back):
    """Render the Recent Activity tab content.
    
    Args:
        df_filtered: Filtered DataFrame for recent period.
        days_back: Number of days in the filter.
    """
    st.subheader(f"Last {days_back} Days")
    
    # Summary metrics
    stats = calculate_summary_stats(df_filtered)
    render_summary_metrics(stats)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_distance = create_distance_timeline(df_filtered)
        st.plotly_chart(fig_distance, use_container_width=True)
    
    with col2:
        fig_type = create_activity_type_pie(df_filtered)
        st.plotly_chart(fig_type, use_container_width=True)
    
    # Duration distribution
    fig_duration = create_duration_histogram(df_filtered)
    st.plotly_chart(fig_duration, use_container_width=True)
    
    # Recent activities table
    st.subheader("Recent Activities")
    
    # Create formatted dataframe for display
    display_df = df_filtered.sort_values("Activity Date", ascending=False)[[
        "Activity Date", "Activity Type", "Distance (km)", 
        "Duration (min)", "Elevation (m)", "Average Speed (km/h)"
    ]].copy()
    
    # Format numeric columns
    display_df["Distance (km)"] = display_df["Distance (km)"].apply(lambda x: f"{x:,.1f}")
    display_df["Duration (min)"] = display_df["Duration (min)"].apply(lambda x: f"{x:,.0f}")
    display_df["Elevation (m)"] = display_df["Elevation (m)"].apply(lambda x: f"{x:,.0f}")
    display_df["Average Speed (km/h)"] = display_df["Average Speed (km/h)"].apply(lambda x: f"{x:,.1f}")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


def render_fun_metrics(metrics):
    """Render fun comparative metrics.
    
    Args:
        metrics: Dictionary of fun metrics from calculate_fun_metrics.
    """
    st.markdown("")  # Spacing
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📅 Activities/Week",
            f"{metrics['activities_per_week']:.1f}",
            help=f"Average per week across your entire activity history ({int(metrics['total_activities']):,} activities)"
        )
    
    with col2:
        display, help_text = format_metric_display(metrics['times_around_world'], 'earth')
        st.metric("🌍 Around Earth", display, help=help_text)
    
    with col3:
        display, help_text = format_metric_display(metrics['days_active'], 'time')
        st.metric("⏱️ Time Active", display, help=help_text)
    
    with col4:
        display, help_text = format_metric_display(metrics['times_up_everest'], 'everest')
        st.metric("🏔️ Up Mt Everest", display, help=help_text)


def render_cheeky_metrics(cheeky):
    """Render cheeky alternative datapoints.
    
    Args:
        cheeky: Dictionary of cheeky metrics from calculate_cheeky_metrics.
    """
    st.markdown("---")
    st.subheader("🤪 Alternative Reality Check")
    st.markdown("*Because serious stats are boring...*")
    
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
            "🏈 Football Fields",
            f"{cheeky['football_fields']:,.0f}",
            help="NFL official fields (91.44m each)"
        )
    
    with col3:
        st.metric(
            "🏃‍♂️ Marathons",
            f"{cheeky['marathons']:.1f}",
            help="Official marathon distance: 42.195 km (IAAF)"
        )
    
    with col4:
        if cheeky['faster_than_sloth'] >= 1:
            st.metric(
                "🦥 vs Sloth Speed",
                f"{cheeky['faster_than_sloth']:.0f}x faster",
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
            f"{cheeky['eiffel_towers']:.1f}",
            help="330m to the tip (Paris official height)"
        )
    
    with col2:
        st.metric(
            "🏙️ Empire States",
            f"{cheeky['empire_states']:.1f}",
            help="443m to roof (ESB official)"
        )
    
    with col3:
        st.metric(
            "🏗️ Burj Khalifas",
            f"{cheeky['burj_khalifas']:.2f}",
            help="828m - World's tallest building (Emaar)"
        )
    
    # Food & Entertainment
    st.markdown("#### 🍕 You Earned It")
    col1, col2, col3, col4 = st.columns(4)
    
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
    
    with col4:
        st.metric(
            "📺 Friends Episodes",
            f"{cheeky['friends_episodes']:,.0f}",
            help="22-min episodes you could've watched instead (NBC avg runtime)"
        )
    
    # Bottom row fun facts
    col1, col2 = st.columns(2)
    
    with col1:
        if cheeky['lotr_trilogies'] >= 1:
            st.metric(
                "🧙‍♂️ LOTR Extended Trilogies",
                f"{cheeky['lotr_trilogies']:.1f}",
                help="558 min total for extended trilogy (New Line Cinema)"
            )
        else:
            pct = cheeky['lotr_trilogies'] * 100
            st.metric(
                "🧙‍♂️ Through LOTR Trilogy",
                f"{pct:.0f}%",
                help="Progress through extended trilogy"
            )
    
    with col2:
        # Cheeky summary
        if cheeky['big_macs'] > 1000:
            verdict = "🎉 That's a LOT of Big Macs!"
        elif cheeky['marathons'] > 100:
            verdict = "🏆 Ultra marathon legend!"
        elif cheeky['friends_episodes'] > 1000:
            verdict = "📺 You chose sweat over sitcoms!"
        else:
            verdict = "💪 Keep crushing it!"
        
        st.metric(
            "🎯 Verdict",
            verdict,
            help="Our totally scientific assessment"
        )


def render_alltime_tab(df):
    """Render the All-Time Analysis tab content.
    
    Args:
        df: Full DataFrame containing all activity data.
    """
    st.markdown("*Showing data from all your activities*")
    
    # All-time summary metrics
    stats = calculate_summary_stats(df)
    render_summary_metrics(stats)
    
    # Fun comparative metrics
    fun_metrics = calculate_fun_metrics(df)
    render_fun_metrics(fun_metrics)
    
    # Exercise obsession meter
    st.markdown("---")
    st.header("🔥 Exercise-oholic Meter")
    obsession_score, obsession_level, obsession_desc = calculate_exercise_obsession_score(df)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        fig_gauge = create_exercise_obsession_gauge(obsession_score, obsession_level)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
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
    
    st.markdown("---")
    
    # Get trend data
    monthly_data = get_monthly_trends(df)
    
    # Time series charts
    fig_cumulative = create_cumulative_distance_chart(monthly_data)
    st.plotly_chart(fig_cumulative, use_container_width=True)
    
    fig_trends = create_quarterly_trends_chart(monthly_data)
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # Stacked activity chart
    fig_stacked = create_stacked_activity_chart(df)
    if fig_stacked:
        st.plotly_chart(fig_stacked, use_container_width=True)
    else:
        st.warning("No activity type data available")
    
    # Personal records
    st.header("🏆 Personal Records")
    prs = get_personal_records(df)
    pr_cols = st.columns(4)
    
    with pr_cols[0]:
        st.metric("Longest Distance", f"{int(prs['longest_distance'])} km")
    with pr_cols[1]:
        st.metric("Longest Duration", f"{int(prs['longest_duration'])} min")
    with pr_cols[2]:
        st.metric("Most Elevation", f"{int(prs['most_elevation']):,} m")
    with pr_cols[3]:
        st.metric("Fastest Speed", f"{int(prs['fastest_speed'])} km/h")
    
    # Quarterly summary
    st.header("📊 Quarterly Summary")
    quarterly_stats = get_quarterly_stats(df)
    
    fig_quarterly = create_quarterly_bar_chart(quarterly_stats)
    st.plotly_chart(fig_quarterly, use_container_width=True)
    
    st.subheader("Quarterly Statistics")
    
    # Create formatted dataframe for display
    display_quarterly = quarterly_stats[[
        "Quarter", "Activity Count", "Total Distance (km)",
        "Total Duration (hours)", "Total Elevation (m)"
    ]].copy()
    
    # Format numeric columns
    display_quarterly["Activity Count"] = display_quarterly["Activity Count"].apply(lambda x: f"{int(x):,}")
    display_quarterly["Total Distance (km)"] = display_quarterly["Total Distance (km)"].apply(lambda x: f"{x:,.1f}")
    display_quarterly["Total Duration (hours)"] = display_quarterly["Total Duration (hours)"].apply(lambda x: f"{x:,.1f}")
    display_quarterly["Total Elevation (m)"] = display_quarterly["Total Elevation (m)"].apply(lambda x: f"{x:,.0f}")
    
    st.dataframe(
        display_quarterly,
        use_container_width=True,
        hide_index=True
    )
    
    # Calendar heatmap
    st.header("📅 Activity Calendar")
    current_year = df["Activity Date"].dt.year.max()
    fig_heatmap = create_activity_heatmap(df, current_year)
    st.plotly_chart(fig_heatmap, use_container_width=True)


def main():
    """Main application entry point."""
    # Setup page
    setup_page()
    
    # Load data
    try:
        df = load_strava_data(DATA_FILE_PATH)
    except FileNotFoundError:
        st.error(f"Data file not found: {DATA_FILE_PATH}")
        st.info("Please ensure your activities.csv file is in the data/ directory")
        return
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # Create sidebar filters
    days_back, selected_activities = create_sidebar(df)
    
    # Apply filters
    df = filter_by_activities(df, selected_activities)
    df_filtered = filter_by_date_range(df, days_back)
    
    # Create tabs
    tab_recent, tab_alltime = st.tabs(["📊 Recent Activity", "🏆 All-Time Analysis"])
    
    with tab_recent:
        render_recent_activity_tab(df_filtered, days_back)
    
    with tab_alltime:
        render_alltime_tab(df)


if __name__ == "__main__":
    main()
