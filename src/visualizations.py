"""Visualization functions for creating charts and graphs.

This module contains all Plotly-based visualization functions used to
display activity data in various chart formats.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional

from src.config import ACTIVITY_COLORS


def create_exercise_obsession_gauge(score: int, level: str, theme: dict = None) -> go.Figure:
    """Create a gauge chart showing exercise obsession level.
    
    Args:
        score: Obsession score (0-100).
        level: Level name (e.g., "Fitness Fanatic").
        theme: Dict containing theme colors.
        
    Returns:
        Plotly gauge figure showing the obsession meter.
        
    Examples:
        >>> fig = create_exercise_obsession_gauge(75, "Fitness Fanatic")
        >>> st.plotly_chart(fig)
    """
    from src.config import PLOTLY_LIGHT_THEME
    if theme is None:
        theme = PLOTLY_LIGHT_THEME
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': f"<b>{level}</b>", 'font': {'size': 24}},
        number={'suffix': "/100", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#12436D"},
            'bar': {'color': "#F46A25"},  # UK Gov orange
            'bgcolor': "white",
            'borderwidth': 3,
            'bordercolor': "#12436D",
            'steps': [
                {'range': [0, 25], 'color': '#E8EDEE'},  # Light grey
                {'range': [25, 50], 'color': '#BFD4DB'},  # Light blue
                {'range': [50, 75], 'color': '#28A197'},  # Turquoise
                {'range': [75, 100], 'color': '#12436D'},  # Dark blue
            ],
            'threshold': {
                'line': {'color': "#801650", 'width': 4},  # Dark pink
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor=theme['paper_bgcolor'],
        font={'color': theme['font_color'], 'family': "Arial"}
    )
    
    return fig


def create_distance_timeline(df: pd.DataFrame, title: str = "Distance Per Activity", theme: dict = None) -> go.Figure:
    """Create a line chart showing distance over time.
    
    Args:
        df: DataFrame with 'Activity Date' and 'Distance (km)' columns.
        title: Chart title.
        theme: Dict containing theme colors.
        
    Returns:
        Plotly figure object displaying distance timeline.
        
    Examples:
        >>> fig = create_distance_timeline(recent_activities)
        >>> st.plotly_chart(fig)
    """
    from src.config import PLOTLY_LIGHT_THEME
    if theme is None:
        theme = PLOTLY_LIGHT_THEME
    fig = px.line(
        df.sort_values("Activity Date"),
        x="Activity Date",
        y="Distance (km)",
        title=title,
        markers=True
    )
    fig.update_traces(
        line_color='#12436D',  # UK Gov dark blue
        marker=dict(size=6, line=dict(width=1, color='white'))
    )
    fig.update_layout(
        plot_bgcolor=theme['plot_bgcolor'],
        paper_bgcolor=theme['paper_bgcolor'],
        font=dict(family="Arial, sans-serif", size=12, color=theme['font_color']),
        title_font=dict(size=16, color=theme['title_color']),
        xaxis=dict(showgrid=True, gridcolor=theme['grid_color'], zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=theme['grid_color'], zeroline=False)
    )
    return fig


def create_activity_type_pie(df: pd.DataFrame, title: str = "Activities by Type", theme: dict = None) -> go.Figure:
    """Create a pie chart showing activity type distribution.
    
    Args:
        df: DataFrame with 'Activity Group' column.
        title: Chart title.
        
    Returns:
        Plotly figure object displaying activity type distribution.
        
    Examples:
        >>> fig = create_activity_type_pie(df)
        >>> st.plotly_chart(fig)
    """
    activity_counts = df["Activity Group"].value_counts()
    
    fig = px.pie(
        values=activity_counts.values,
        names=activity_counts.index,
        title=title,
        color=activity_counts.index,
        color_discrete_map=ACTIVITY_COLORS
    )
    return fig


def create_duration_histogram(df: pd.DataFrame, title: str = "Duration Distribution", 
                              nbins: int = 15, theme: dict = None) -> go.Figure:
    """Create a histogram showing activity duration distribution.
    
    Args:
        df: DataFrame with 'Duration (min)' column.
        title: Chart title.
        nbins: Number of bins for the histogram.
        theme: Dict containing theme colors.
        
    Returns:
        Plotly figure object displaying duration distribution.
        
    Examples:
        >>> fig = create_duration_histogram(df, nbins=20)
        >>> st.plotly_chart(fig)
    """
    from src.config import PLOTLY_LIGHT_THEME
    if theme is None:
        theme = PLOTLY_LIGHT_THEME
    # Create bins for smoother distribution
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df["Duration (min)"],
        nbinsx=nbins,
        marker_color='#12436D',  # UK Gov dark blue
        marker_line_color='white',
        marker_line_width=1,
        opacity=0.85
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Duration (min)",
        yaxis_title="Count",
        plot_bgcolor=theme['plot_bgcolor'],
        paper_bgcolor=theme['paper_bgcolor'],
        font=dict(family="Arial, sans-serif", size=12, color=theme['font_color']),
        title_font=dict(size=16, color=theme['title_color']),
        xaxis=dict(showgrid=True, gridcolor=theme['grid_color'], zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=theme['grid_color'], zeroline=False),
        bargap=0.05
    )
    return fig


def create_cumulative_distance_chart(period_data: pd.DataFrame, 
                                    title: str = "Cumulative Distance Over Time",
                                    interval: str = "quarterly",
                                    theme: dict = None) -> go.Figure:
    """Create a line chart showing cumulative distance over time.
    
    Args:
        period_data: DataFrame with 'Period' and 'Cumulative Distance' columns.
        title: Chart title.
        interval: Time interval for x-axis tick formatting.
        theme: Dict containing theme colors.
        
    Returns:
        Plotly figure object displaying cumulative distance.
        
    Examples:
        >>> fig = create_cumulative_distance_chart(monthly_stats, interval="monthly")
        >>> st.plotly_chart(fig)
    """
    from src.config import PLOTLY_LIGHT_THEME
    if theme is None:
        theme = PLOTLY_LIGHT_THEME
        
    # Skip chart if only one data point (alltime)
    if len(period_data) <= 1:
        return None
        
    fig = px.line(
        period_data,
        x="Period",
        y="Cumulative Distance",
        title=title,
        markers=True,
        labels={"Cumulative Distance": "Total Distance (km)", "Period": "Period"}
    )
    fig.update_traces(
        line_color='#28A197',  # UK Gov turquoise
        marker=dict(size=8, line=dict(width=1, color='white')),
        line_width=3
    )
    fig.update_layout(
        plot_bgcolor=theme['plot_bgcolor'],
        paper_bgcolor=theme['paper_bgcolor'],
        font=dict(family="Arial, sans-serif", size=12, color=theme['font_color']),
        title_font=dict(size=16, color=theme['title_color']),
        xaxis=dict(showgrid=True, gridcolor=theme['grid_color'], zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=theme['grid_color'], zeroline=False)
    )
    
    # Adjust tick frequency based on interval
    if interval == "quarterly":
        fig.update_xaxes(tickangle=0, dtick=4)  # Show every 4 quarters (yearly)
    elif interval == "monthly":
        fig.update_xaxes(tickangle=45, dtick=6)  # Show every 6 months
    elif interval == "annual":
        fig.update_xaxes(tickangle=0, dtick=1)  # Show every year
        
    return fig


def create_quarterly_trends_chart(period_data: pd.DataFrame, 
                                 title: str = "Activity Trends Over Time",
                                 interval: str = "quarterly",
                                 theme: dict = None) -> go.Figure:
    """Create a multi-line chart showing activity trends over time.
    
    Args:
        period_data: DataFrame with 'Period', 'Distance', and 'Activity Count' columns.
        title: Chart title.
        interval: Time interval for x-axis tick formatting.
        theme: Dict containing theme colors.
        
    Returns:
        Plotly figure object displaying trends.
        
    Examples:
        >>> fig = create_quarterly_trends_chart(trends_data, interval="monthly")
        >>> st.plotly_chart(fig)
    """
    from src.config import PLOTLY_LIGHT_THEME
    if theme is None:
        theme = PLOTLY_LIGHT_THEME
        
    # Skip chart if only one data point (alltime)
    if len(period_data) <= 1:
        return None
        
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add Distance trace on primary y-axis
    fig.add_trace(go.Scatter(
        x=period_data["Period"],
        y=period_data["Distance"],
        name="Distance (km)",
        mode='lines+markers',
        line=dict(color='#12436D', width=2.5),
        marker=dict(size=7, line=dict(width=1, color='white'))
    ))
    
    # Add Activity Count trace on secondary y-axis
    fig.add_trace(go.Scatter(
        x=period_data["Period"],
        y=period_data["Activity Count"],
        name="Activity Count",
        mode='lines+markers',
        line=dict(color='#F46A25', width=2.5),
        marker=dict(size=7, line=dict(width=1, color='white')),
        yaxis="y2"
    ))
    
    fig.update_layout(
        title=title,
        plot_bgcolor=theme['plot_bgcolor'],
        paper_bgcolor=theme['paper_bgcolor'],
        font=dict(family="Arial, sans-serif", size=12, color=theme['font_color']),
        title_font=dict(size=16, color=theme['title_color']),
        xaxis=dict(showgrid=True, gridcolor=theme['grid_color'], zeroline=False),
        yaxis=dict(
            title="Distance (km)",
            showgrid=True, 
            gridcolor=theme['grid_color'], 
            zeroline=False
        ),
        yaxis2=dict(
            title="Activity Count",
            overlaying="y",
            side="right",
            showgrid=False,
            zeroline=False
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Adjust tick frequency based on interval
    if interval == "quarterly":
        fig.update_xaxes(tickangle=0, dtick=4)  # Show every 4 quarters (yearly)
    elif interval == "monthly":
        fig.update_xaxes(tickangle=45, dtick=6)  # Show every 6 months
    elif interval == "annual":
        fig.update_xaxes(tickangle=0, dtick=1)  # Show every year
        
    return fig


def create_stacked_activity_chart(activity_data: pd.DataFrame, 
                                  title: str = "Activity Type Composition Over Time",
                                  interval: str = "quarterly",
                                  theme: dict = None) -> Optional[go.Figure]:
    """Create a stacked bar chart showing activity type distribution over time.
    
    Args:
        activity_data: DataFrame with 'Period', 'Activity Group', and 'Count' columns.
        title: Chart title.
        interval: Time interval for x-axis tick formatting.
        theme: Dict containing theme colors.
        
    Returns:
        Plotly figure object or None if no data available.
        
    Examples:
        >>> fig = create_stacked_activity_chart(activity_data, interval="monthly")
        >>> if fig:
        >>>     st.plotly_chart(fig)
    """
    from src.config import PLOTLY_LIGHT_THEME
    if theme is None:
        theme = PLOTLY_LIGHT_THEME
        
    if len(activity_data) == 0:
        return None
    
    # Skip chart if only one period (alltime)
    if len(activity_data["Period"].unique()) <= 1:
        return None
    
    fig = px.bar(
        activity_data,
        x="Period",
        y="Count",
        color="Activity Group",
        title=title,
        labels={"Count": "Number of Activities", "Period": "Period"},
        color_discrete_map=ACTIVITY_COLORS,
        barmode="stack"
    )
    fig.update_traces(marker_line_color='white', marker_line_width=0.5)
    
    # Adjust tick frequency based on interval
    if interval == "quarterly":
        fig.update_xaxes(tickangle=0, dtick=4)  # Show every 4 quarters (yearly)
    elif interval == "monthly":
        fig.update_xaxes(tickangle=45, dtick=6)  # Show every 6 months
    elif interval == "annual":
        fig.update_xaxes(tickangle=0, dtick=1)  # Show every year
        
    fig.update_layout(
        plot_bgcolor=theme['plot_bgcolor'],
        paper_bgcolor=theme['paper_bgcolor'],
        font=dict(family="Arial, sans-serif", size=12, color=theme['font_color']),
        title_font=dict(size=16, color=theme['title_color']),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=theme['grid_color'], zeroline=False),
        hovermode="x unified",
        legend=dict(
            title="Activity Type",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02
        )
    )
    return fig


def create_rolling_average_chart(monthly_data: pd.DataFrame, 
                                 title: str = "Rolling Average Distance") -> go.Figure:
    """Create a line chart showing rolling average distance.
    
    Args:
        monthly_data: DataFrame with 'Quarter' and 'Rolling Avg Distance' columns.
        title: Chart title.
        
    Returns:
        Plotly figure object displaying rolling average.
        
    Examples:
        >>> fig = create_rolling_average_chart(monthly_data)
        >>> st.plotly_chart(fig)
    """
    fig = px.line(
        monthly_data,
        x="Quarter",
        y="Rolling Avg Distance",
        title=title,
        markers=True,
        labels={"Rolling Avg Distance": "Distance (km)", "Quarter": "Quarter"}
    )
    fig.update_traces(
        line_color='#A285D1',  # UK Gov light purple
        marker=dict(size=7, line=dict(width=1, color='white')),
        line_width=3
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12, color="#2c3e50"),
        title_font=dict(size=16, color="#2c3e50"),
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', zeroline=False)
    )
    fig.update_xaxes(tickangle=0, dtick=4)  # Show every 4 quarters (yearly)
    return fig


def create_year_over_year_chart(df: pd.DataFrame, 
                                title: str = "Year-over-Year Comparison") -> go.Figure:
    """Create a line chart comparing activity across years by month.
    
    Args:
        df: DataFrame containing activity data.
        title: Chart title.
        
    Returns:
        Plotly figure object displaying year-over-year comparison.
        
    Examples:
        >>> fig = create_year_over_year_chart(df)
        >>> st.plotly_chart(fig)
    """
    df_timeline = df.copy()
    df_timeline["Year"] = df_timeline["Activity Date"].dt.year
    df_timeline["Month"] = df_timeline["Activity Date"].dt.month
    
    yearly_monthly = df_timeline.groupby(["Year", "Month"]).agg({
        "Distance (km)": "sum"
    }).reset_index()
    yearly_monthly["Month Name"] = pd.to_datetime(
        yearly_monthly["Month"], format='%m'
    ).dt.month_name()
    yearly_monthly["Year"] = yearly_monthly["Year"].astype(str)
    
    fig = px.line(
        yearly_monthly,
        x="Month",
        y="Distance (km)",
        color="Year",
        title=title,
        markers=True,
        labels={"Distance (km)": "Distance (km)"}
    )
    return fig


def create_quarterly_bar_chart(quarterly_stats: pd.DataFrame, 
                               title: str = "Quarterly Distance Total",
                               theme: dict = None) -> go.Figure:
    """Create a bar chart showing quarterly distance totals.
    
    Args:
        quarterly_stats: DataFrame with 'Quarter' and 'Total Distance (km)' columns.
        title: Chart title.
        theme: Dict containing theme colors.
        
    Returns:
        Plotly figure object displaying quarterly bars.
        
    Examples:
        >>> fig = create_quarterly_bar_chart(stats)
        >>> st.plotly_chart(fig)
    """
    from src.config import PLOTLY_LIGHT_THEME
    if theme is None:
        theme = PLOTLY_LIGHT_THEME
        
    fig = px.bar(
        quarterly_stats.sort_values("Quarter"),
        x="Quarter",
        y="Total Distance (km)",
        title=title,
        text="Total Distance (km)"
    )
    fig.update_traces(
        marker_color='#12436D',  # UK Gov dark blue
        marker_line_color='white',
        marker_line_width=1,
        textposition='outside',
        texttemplate='%{text:.1f}'
    )
    fig.update_layout(
        plot_bgcolor=theme['plot_bgcolor'],
        paper_bgcolor=theme['paper_bgcolor'],
        font=dict(family="Arial, sans-serif", size=12, color=theme['font_color']),
        title_font=dict(size=16, color=theme['title_color']),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=theme['grid_color'], zeroline=False)
    )
    return fig


def create_activity_heatmap(df: pd.DataFrame, current_year: int, 
                            title: Optional[str] = None) -> go.Figure:
    """Create a calendar heatmap showing activity frequency.
    
    Args:
        df: DataFrame containing activity data for the specified year.
        current_year: Year to display in heatmap.
        title: Chart title. If None, defaults to "Activity Heatmap - {year}".
        
    Returns:
        Plotly figure object displaying activity heatmap.
        
    Examples:
        >>> fig = create_activity_heatmap(df, 2025)
        >>> st.plotly_chart(fig)
    """
    if title is None:
        title = f"Activity Heatmap - {current_year}"
    
    df_year = df[df["Activity Date"].dt.year == current_year].copy()
    
    fig = px.density_heatmap(
        df_year,
        x=df_year["Activity Date"].dt.isocalendar().week,
        y=df_year["Activity Date"].dt.day_name(),
        title=title,
        nbinsx=53,
        color_continuous_scale="Greens",
        labels={"x": "Week of Year", "y": "Day of Week"}
    )
    return fig
