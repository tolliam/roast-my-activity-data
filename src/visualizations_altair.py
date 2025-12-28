"""Altair-based visualization functions for mobile-optimized charts.

This module contains all Altair-based visualization functions used to
display activity data in various chart formats with better mobile support.
"""

import altair as alt
import pandas as pd
from typing import Optional, Dict

from src.config import ACTIVITY_COLORS

# Configure Altair for better mobile rendering
alt.data_transformers.disable_max_rows()


def get_altair_theme(theme: Dict = None) -> Dict:
    """Get Altair theme configuration based on light/dark mode.
    
    Args:
        theme: Dict containing theme colors from config.
        
    Returns:
        Dict with Altair-compatible theme settings.
    """
    from src.config import PLOTLY_LIGHT_THEME
    if theme is None:
        theme = PLOTLY_LIGHT_THEME
    
    is_dark = theme.get('paper_bgcolor', 'white') != 'white'
    
    # Primary chart color - lighter for dark mode, darker for light mode
    primary_color = '#28A197' if is_dark else '#12436D'  # Turquoise for dark, dark blue for light
    secondary_color = '#F46A25'  # Orange works in both modes
    accent_color = '#28A197'  # Turquoise
    
    return {
        'background': theme['paper_bgcolor'],
        'font_color': theme['font_color'],
        'grid_color': theme['grid_color'],
        'title_color': theme['title_color'],
        'is_dark': is_dark,
        'primary_color': primary_color,
        'secondary_color': secondary_color,
        'accent_color': accent_color
    }


def create_distance_timeline(df: pd.DataFrame, title: str = "Distance Per Activity", 
                            theme: Dict = None) -> alt.Chart:
    """Create a line chart showing distance over time.
    
    Args:
        df: DataFrame with 'Activity Date' and 'Distance (km)' columns.
        title: Chart title.
        theme: Dict containing theme colors.
        
    Returns:
        Altair chart displaying distance timeline.
    """
    t = get_altair_theme(theme)
    
    df_sorted = df.sort_values("Activity Date").copy()
    
    base = alt.Chart(df_sorted).encode(
        x=alt.X('Activity Date:T', title='Date', axis=alt.Axis(format='%b %d')),
        y=alt.Y('Distance (km):Q', title='Distance (km)')
    )
    
    line = base.mark_line(color=t['primary_color'], strokeWidth=2)
    points = base.mark_circle(color=t['primary_color'], size=50)
    
    chart = (line + points).properties(
        title=title,
        height=300
    ).configure(
        background=t['background']
    ).configure_axis(
        labelColor=t['font_color'],
        titleColor=t['font_color'],
        gridColor=t['grid_color'],
        domainColor=t['grid_color']
    ).configure_title(
        color=t['title_color'],
        fontSize=16
    )
    
    return chart


def create_activity_type_pie(df: pd.DataFrame, title: str = "Activities by Type",
                            theme: Dict = None) -> alt.Chart:
    """Create a donut chart showing activity type distribution.
    
    Args:
        df: DataFrame with 'Activity Group' column.
        title: Chart title.
        theme: Dict containing theme colors.
        
    Returns:
        Altair chart displaying activity type distribution.
    """
    t = get_altair_theme(theme)
    
    activity_counts = df["Activity Group"].value_counts().reset_index()
    activity_counts.columns = ["Activity Group", "Count"]
    
    # Create color domain and range from ACTIVITY_COLORS
    color_domain = list(ACTIVITY_COLORS.keys())
    color_range = list(ACTIVITY_COLORS.values())
    
    chart = alt.Chart(activity_counts).mark_arc(innerRadius=50, outerRadius=100).encode(
        theta=alt.Theta('Count:Q'),
        color=alt.Color('Activity Group:N', 
                       scale=alt.Scale(domain=color_domain, range=color_range),
                       legend=alt.Legend(title="Activity Type")),
        tooltip=['Activity Group:N', 'Count:Q']
    ).properties(
        title=title,
        height=300
    ).configure(
        background=t['background']
    ).configure_legend(
        labelColor=t['font_color'],
        titleColor=t['font_color']
    ).configure_title(
        color=t['title_color'],
        fontSize=16
    )
    
    return chart


def create_duration_histogram(df: pd.DataFrame, title: str = "Duration Distribution",
                             theme: Dict = None) -> alt.Chart:
    """Create a histogram showing activity duration distribution.
    
    Args:
        df: DataFrame with 'Duration (min)' column.
        title: Chart title.
        theme: Dict containing theme colors.
        
    Returns:
        Altair chart displaying duration distribution.
    """
    t = get_altair_theme(theme)
    
    chart = alt.Chart(df).mark_bar(color=t['primary_color'], opacity=0.85).encode(
        x=alt.X('Duration (min):Q', bin=alt.Bin(maxbins=15), title='Duration (min)'),
        y=alt.Y('count():Q', title='Count'),
        tooltip=[alt.Tooltip('Duration (min):Q', bin=alt.Bin(maxbins=15)), 'count():Q']
    ).properties(
        title=title,
        height=300
    ).configure(
        background=t['background']
    ).configure_axis(
        labelColor=t['font_color'],
        titleColor=t['font_color'],
        gridColor=t['grid_color'],
        domainColor=t['grid_color']
    ).configure_title(
        color=t['title_color'],
        fontSize=16
    )
    
    return chart


def create_cumulative_distance_chart(period_data: pd.DataFrame,
                                    title: str = "Cumulative Distance Over Time",
                                    interval: str = "quarterly",
                                    theme: Dict = None) -> Optional[alt.Chart]:
    """Create a line chart showing cumulative distance over time.
    
    Args:
        period_data: DataFrame with 'Period' and 'Cumulative Distance' columns.
        title: Chart title.
        interval: Time interval for x-axis tick formatting.
        theme: Dict containing theme colors.
        
    Returns:
        Altair chart or None if insufficient data.
    """
    t = get_altair_theme(theme)
    
    if len(period_data) <= 1:
        return None
    
    base = alt.Chart(period_data).encode(
        x=alt.X('Period:N', title='Period', axis=alt.Axis(labelAngle=-45 if interval == 'monthly' else 0)),
        y=alt.Y('Cumulative Distance:Q', title='Total Distance (km)')
    )
    
    line = base.mark_line(color=t['accent_color'], strokeWidth=3)
    points = base.mark_circle(color=t['accent_color'], size=60)
    
    chart = (line + points).properties(
        title=title,
        height=300
    ).configure(
        background=t['background']
    ).configure_axis(
        labelColor=t['font_color'],
        titleColor=t['font_color'],
        gridColor=t['grid_color'],
        domainColor=t['grid_color']
    ).configure_title(
        color=t['title_color'],
        fontSize=16
    )
    
    return chart


def create_activity_trends_chart(period_data: pd.DataFrame,
                                title: str = "Activity Trends Over Time",
                                interval: str = "quarterly",
                                theme: Dict = None) -> Optional[alt.Chart]:
    """Create a dual-axis chart showing distance and activity count trends.
    
    Args:
        period_data: DataFrame with 'Period', 'Distance', and 'Activity Count' columns.
        title: Chart title.
        interval: Time interval for x-axis formatting.
        theme: Dict containing theme colors.
        
    Returns:
        Altair chart or None if insufficient data.
    """
    t = get_altair_theme(theme)
    
    if len(period_data) <= 1:
        return None
    
    # Create base encoding
    base = alt.Chart(period_data).encode(
        x=alt.X('Period:N', title='Period', axis=alt.Axis(labelAngle=-45 if interval == 'monthly' else 0))
    )
    
    # Distance line (left axis)
    distance_line = base.mark_line(color=t['primary_color'], strokeWidth=2.5).encode(
        y=alt.Y('Distance:Q', title='Distance (km)', axis=alt.Axis(titleColor=t['primary_color']))
    )
    distance_points = base.mark_circle(color=t['primary_color'], size=50).encode(
        y=alt.Y('Distance:Q')
    )
    
    # Activity count line (right axis) 
    count_line = base.mark_line(color=t['secondary_color'], strokeWidth=2.5, strokeDash=[5, 3]).encode(
        y=alt.Y('Activity Count:Q', title='Activity Count', axis=alt.Axis(titleColor=t['secondary_color']))
    )
    count_points = base.mark_circle(color=t['secondary_color'], size=50).encode(
        y=alt.Y('Activity Count:Q')
    )
    
    # Layer with independent y scales
    distance_chart = (distance_line + distance_points)
    count_chart = (count_line + count_points).encode(
        y=alt.Y('Activity Count:Q', title='Activity Count', 
                axis=alt.Axis(titleColor=t['secondary_color'], orient='right'))
    )
    
    chart = alt.layer(distance_chart, count_chart).resolve_scale(
        y='independent'
    ).properties(
        title=title,
        height=300
    ).configure(
        background=t['background']
    ).configure_axis(
        labelColor=t['font_color'],
        gridColor=t['grid_color'],
        domainColor=t['grid_color']
    ).configure_title(
        color=t['title_color'],
        fontSize=16
    )
    
    return chart


def create_stacked_activity_chart(activity_data: pd.DataFrame,
                                 title: str = "Activity Type Composition Over Time",
                                 interval: str = "quarterly",
                                 theme: Dict = None) -> Optional[alt.Chart]:
    """Create a stacked bar chart showing activity type distribution over time.
    
    Args:
        activity_data: DataFrame with 'Period', 'Activity Group', and 'Count' columns.
        title: Chart title.
        interval: Time interval for x-axis formatting.
        theme: Dict containing theme colors.
        
    Returns:
        Altair chart or None if insufficient data.
    """
    t = get_altair_theme(theme)
    
    if len(activity_data) == 0:
        return None
    
    if len(activity_data["Period"].unique()) <= 1:
        return None
    
    # Create color domain and range from ACTIVITY_COLORS
    color_domain = list(ACTIVITY_COLORS.keys())
    color_range = list(ACTIVITY_COLORS.values())
    
    chart = alt.Chart(activity_data).mark_bar().encode(
        x=alt.X('Period:N', title='Period', axis=alt.Axis(labelAngle=-45 if interval == 'monthly' else 0)),
        y=alt.Y('Count:Q', title='Number of Activities', stack='zero'),
        color=alt.Color('Activity Group:N',
                       scale=alt.Scale(domain=color_domain, range=color_range),
                       legend=alt.Legend(title="Activity Type")),
        tooltip=['Period:N', 'Activity Group:N', 'Count:Q']
    ).properties(
        title=title,
        height=300
    ).configure(
        background=t['background']
    ).configure_axis(
        labelColor=t['font_color'],
        titleColor=t['font_color'],
        gridColor=t['grid_color'],
        domainColor=t['grid_color']
    ).configure_legend(
        labelColor=t['font_color'],
        titleColor=t['font_color']
    ).configure_title(
        color=t['title_color'],
        fontSize=16
    )
    
    return chart


def create_activity_heatmap(df: pd.DataFrame, current_year: int,
                           title: Optional[str] = None,
                           theme: Dict = None) -> alt.Chart:
    """Create a calendar heatmap showing activity frequency.
    
    Args:
        df: DataFrame containing activity data.
        current_year: Year to display in heatmap.
        title: Chart title.
        theme: Dict containing theme colors.
        
    Returns:
        Altair chart displaying activity heatmap.
    """
    t = get_altair_theme(theme)
    
    if title is None:
        title = f"Activity Heatmap - {current_year}"
    
    df_year = df[df["Activity Date"].dt.year == current_year].copy()
    df_year["Week"] = df_year["Activity Date"].dt.isocalendar().week.astype(int)
    df_year["DayNum"] = df_year["Activity Date"].dt.dayofweek  # 0=Monday, 6=Sunday
    
    # Create complete grid of all weeks and days
    all_weeks = list(range(1, 54))
    all_days = list(range(7))
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    # Create full grid
    full_grid = pd.DataFrame([(w, d) for w in all_weeks for d in all_days], 
                             columns=["Week", "DayNum"])
    
    # Aggregate actual activity data
    activity_counts = df_year.groupby(["Week", "DayNum"]).size().reset_index(name="Count")
    
    # Merge to get full grid with counts (0 for empty days)
    heatmap_data = full_grid.merge(activity_counts, on=["Week", "DayNum"], how="left")
    heatmap_data["Count"] = heatmap_data["Count"].fillna(0).astype(int)
    heatmap_data["Day"] = heatmap_data["DayNum"].map(lambda x: day_names[x])
    
    chart = alt.Chart(heatmap_data).mark_rect(cornerRadius=2, stroke='white', strokeWidth=1).encode(
        x=alt.X('Week:O', title='Week', axis=alt.Axis(labelAngle=0, values=[1, 10, 20, 30, 40, 50])),
        y=alt.Y('Day:N', title='', sort=day_names, axis=alt.Axis(labelAngle=0)),
        color=alt.Color('Count:Q', 
                       scale=alt.Scale(scheme='greens', domain=[0, max(heatmap_data["Count"].max(), 1)]),
                       legend=alt.Legend(title="Activities", gradientLength=100, gradientThickness=10)),
        tooltip=['Week:O', 'Day:N', 'Count:Q']
    ).properties(
        title=title,
        width=450,
        height=280
    ).configure(
        background=t['background']
    ).configure_axis(
        labelColor=t['font_color'],
        titleColor=t['font_color'],
        domainColor=t['grid_color']
    ).configure_legend(
        labelColor=t['font_color'],
        titleColor=t['font_color']
    ).configure_title(
        color=t['title_color'],
        fontSize=16
    )
    
    return chart


def create_exercise_obsession_gauge(score: int, level: str, theme: Dict = None) -> alt.Chart:
    """Create a gauge-like visualization for exercise obsession score.
    
    Uses a radial bar chart to simulate a gauge since Altair doesn't have native gauges.
    
    Args:
        score: Obsession score (0-100).
        level: Level name (e.g., "Fitness Fanatic").
        theme: Dict containing theme colors.
        
    Returns:
        Altair chart displaying the obsession gauge.
    """
    t = get_altair_theme(theme)
    
    # Create data for arc segments - use theme-aware background for remaining
    remaining_color = t['grid_color'] if t['is_dark'] else '#E8EDEE'
    
    data = pd.DataFrame({
        'category': ['Score', 'Remaining'],
        'value': [score, 100 - score],
        'color': [t['secondary_color'], remaining_color]
    })
    
    # Create the arc chart
    arc = alt.Chart(data).mark_arc(innerRadius=60, outerRadius=100).encode(
        theta=alt.Theta('value:Q', stack=True),
        color=alt.Color('color:N', scale=None, legend=None),
        order=alt.Order('category:N', sort='ascending')
    )
    
    # Add center text
    text_score = alt.Chart(pd.DataFrame({'text': [f'{score}']})).mark_text(
        fontSize=36,
        fontWeight='bold',
        color=t['font_color']
    ).encode(
        text='text:N'
    )
    
    text_label = alt.Chart(pd.DataFrame({'text': [level]})).mark_text(
        fontSize=14,
        dy=25,
        color=t['font_color']
    ).encode(
        text='text:N'
    )
    
    chart = (arc + text_score + text_label).properties(
        height=250,
        title=""
    ).configure(
        background=t['background']
    ).configure_title(
        color=t['title_color']
    )
    
    return chart


def create_time_of_day_pie(df: pd.DataFrame, title: str = "Activities by Time of Day",
                           theme: Dict = None) -> Optional[alt.Chart]:
    """Create a pie chart showing distribution of activities by time of day.
    
    Args:
        df: Activity DataFrame with 'Time of Day' column.
        title: Chart title.
        theme: Dict containing theme colors.
        
    Returns:
        Altair pie chart or None if data is insufficient.
    """
    if "Time of Day" not in df.columns or len(df) == 0:
        return None
    
    t = get_altair_theme(theme)
    
    # Count activities by time of day
    time_counts = df["Time of Day"].value_counts().reset_index()
    time_counts.columns = ["Time of Day", "Count"]
    
    # Define colors for time of day periods - using consistent palette
    time_colors = {
        "Morning": "#12436D",    # Dark blue
        "Afternoon": "#28A197",  # Turquoise
        "Evening": "#F46A25",    # Orange
        "Night": "#801650",      # Purple
        "Unknown": "#BDBDBD"     # Gray for unknown
    }
    
    # Order categories logically
    time_order = ["Morning", "Afternoon", "Evening", "Night", "Unknown"]
    time_counts["Time of Day"] = pd.Categorical(
        time_counts["Time of Day"], 
        categories=time_order, 
        ordered=True
    )
    time_counts = time_counts.sort_values("Time of Day")
    
    # Create the pie chart
    chart = alt.Chart(time_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta('Count:Q'),
        color=alt.Color(
            'Time of Day:N',
            scale=alt.Scale(
                domain=list(time_colors.keys()),
                range=list(time_colors.values())
            ),
            legend=alt.Legend(
                title="Time of Day",
                titleColor=t['title_color'],
                labelColor=t['font_color'],
                orient='bottom'
            )
        ),
        tooltip=[
            alt.Tooltip('Time of Day:N', title='Period'),
            alt.Tooltip('Count:Q', title='Activities')
        ]
    ).properties(
        title=alt.TitleParams(text=title, color=t['title_color'], fontSize=16),
        height=300
    ).configure(
        background=t['background']
    )
    
    return chart


def create_hourly_activity_chart(df: pd.DataFrame, title: str = "Activity Distribution by Hour",
                                 theme: Dict = None) -> Optional[alt.Chart]:
    """Create a bar chart showing activity count by hour of day.
    
    Args:
        df: DataFrame with 'Hour' and 'Activity Count' columns.
        title: Chart title.
        theme: Dict containing theme colors.
        
    Returns:
        Altair bar chart or None if data is insufficient.
    """
    if len(df) == 0 or "Hour" not in df.columns:
        return None
    
    t = get_altair_theme(theme)
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Hour:O', title='Hour of Day', axis=alt.Axis(labelColor=t['font_color'])),
        y=alt.Y('Activity Count:Q', title='Number of Activities', axis=alt.Axis(labelColor=t['font_color'])),
        color=alt.value('#12436D'),
        tooltip=[
            alt.Tooltip('Hour:O', title='Hour'),
            alt.Tooltip('Activity Count:Q', title='Activities')
        ]
    ).properties(
        title=alt.TitleParams(text=title, color=t['title_color'], fontSize=16),
        height=300
    ).configure(
        background=t['background']
    ).configure_axis(
        gridColor=t['grid_color'],
        titleColor=t['title_color']
    )
    
    return chart


def create_day_hour_heatmap(df: pd.DataFrame, title: str = "Activity Patterns: Day & Hour",
                            theme: Dict = None) -> Optional[alt.Chart]:
    """Create a heatmap showing activity patterns by day of week and hour.
    
    Args:
        df: DataFrame with 'Day', 'Hour', and 'Count' columns.
        title: Chart title.
        theme: Dict containing theme colors.
        
    Returns:
        Altair heatmap or None if data is insufficient.
    """
    if len(df) == 0 or not all(col in df.columns for col in ["Day", "Hour", "Count"]):
        return None
    
    t = get_altair_theme(theme)
    
    # Ensure proper day ordering
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    chart = alt.Chart(df).mark_rect().encode(
        x=alt.X('Hour:O', title='Hour of Day', axis=alt.Axis(labelColor=t['font_color'])),
        y=alt.Y('Day:N', title='Day of Week', sort=day_order, axis=alt.Axis(labelColor=t['font_color'])),
        color=alt.Color(
            'Count:Q',
            scale=alt.Scale(scheme='blues'),
            legend=alt.Legend(
                title="Activities",
                titleColor=t['title_color'],
                labelColor=t['font_color']
            )
        ),
        tooltip=[
            alt.Tooltip('Day:N', title='Day'),
            alt.Tooltip('Hour:O', title='Hour'),
            alt.Tooltip('Count:Q', title='Activities')
        ]
    ).properties(
        title=alt.TitleParams(text=title, color=t['title_color'], fontSize=16),
        height=300
    ).configure(
        background=t['background']
    ).configure_axis(
        gridColor=t['grid_color'],
        titleColor=t['title_color']
    )
    
    return chart


def create_time_performance_chart(df: pd.DataFrame, title: str = "Average Performance by Time of Day",
                                  theme: Dict = None) -> Optional[alt.Chart]:
    """Create a chart comparing average distance and speed by time of day.
    
    Args:
        df: Activity DataFrame with 'Time of Day', 'Distance (km)', and 'Average Speed (km/h)' columns.
        title: Chart title.
        theme: Dict containing theme colors.
        
    Returns:
        Altair chart or None if data is insufficient.
    """
    if "Time of Day" not in df.columns or len(df) == 0:
        return None
    
    t = get_altair_theme(theme)
    
    # Calculate average metrics by time of day
    time_stats = df.groupby("Time of Day").agg({
        "Distance (km)": "mean",
        "Duration (min)": "mean",
        "Average Speed (km/h)": "mean"
    }).reset_index()
    
    # Order categories logically
    time_order = ["Morning", "Afternoon", "Evening", "Night", "Unknown"]
    time_stats["Time of Day"] = pd.Categorical(
        time_stats["Time of Day"], 
        categories=time_order, 
        ordered=True
    )
    time_stats = time_stats.sort_values("Time of Day")
    
    # Round for display
    time_stats["Avg Distance"] = time_stats["Distance (km)"].round(2)
    time_stats["Avg Duration"] = time_stats["Duration (min)"].round(1)
    time_stats["Avg Speed"] = time_stats["Average Speed (km/h)"].round(2)
    
    # Create distance chart
    chart = alt.Chart(time_stats).mark_bar().encode(
        x=alt.X('Time of Day:N', title='Time of Day', axis=alt.Axis(labelColor=t['font_color'])),
        y=alt.Y('Avg Distance:Q', title='Average Distance (km)', axis=alt.Axis(labelColor=t['font_color'])),
        color=alt.value('#12436D'),
        tooltip=[
            alt.Tooltip('Time of Day:N', title='Period'),
            alt.Tooltip('Avg Distance:Q', title='Avg Distance (km)'),
            alt.Tooltip('Avg Duration:Q', title='Avg Duration (min)'),
            alt.Tooltip('Avg Speed:Q', title='Avg Speed (km/h)')
        ]
    ).properties(
        title=alt.TitleParams(text=title, color=t['title_color'], fontSize=16),
        height=300
    ).configure(
        background=t['background']
    ).configure_axis(
        gridColor=t['grid_color'],
        titleColor=t['title_color']
    )
    
    return chart
