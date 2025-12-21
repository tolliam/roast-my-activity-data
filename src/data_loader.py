"""Data loading and preprocessing utilities for activity data.

This module provides functions to load, clean, and transform activity
data from CSV files into a format suitable for analysis and visualization.
"""

import pandas as pd
from typing import Optional
import streamlit as st

from src.config import ACTIVITY_GROUP_MAP, DATA_FILE_PATH, MTB_KEYWORDS, ROAD_CYCLING_KEYWORDS


def detect_cycling_subtype(row: pd.Series) -> str:
    """Detect cycling subtype (Mountain Biking, Road Cycling, or generic Cycling).
    
    Analyzes activity name and description for keywords to determine
    if a ride is mountain biking, road cycling, or generic cycling.
    
    Args:
        row: DataFrame row containing 'Activity Name' and 'Activity Description'
        
    Returns:
        String indicating the cycling subtype: 'Mountain Biking', 'Road Cycling', or 'Cycling'
        
    Examples:
        >>> row = pd.Series({'Activity Name': 'MTB trail ride', 'Activity Description': 'Fun ride'})
        >>> detect_cycling_subtype(row)
        'Mountain Biking'
    """
    # Combine name and description for keyword search
    text = f"{str(row.get('Activity Name', ''))} {str(row.get('Activity Description', ''))}".lower()
    
    # Check for MTB keywords first (more specific)
    for keyword in MTB_KEYWORDS:
        if keyword in text:
            return "Mountain Biking"
    
    # Check for road cycling keywords
    for keyword in ROAD_CYCLING_KEYWORDS:
        if keyword in text:
            return "Road Cycling"
    
    # Default to generic cycling
    return "Cycling"


@st.cache_data
def load_strava_data(file_path=None) -> pd.DataFrame:
    """Load and preprocess Strava activities from CSV file or uploaded file.
    
    This function reads the Strava activities CSV, converts data types,
    calculates derived metrics, and maps activity types to groups.
    
    Args:
        file_path: Path to the CSV file or UploadedFile object from Streamlit.
                  If None, uses the default path from config.
    
    Returns:
        A pandas DataFrame containing preprocessed activity data with columns:
        - Activity Date: datetime of activity
        - Distance (km): activity distance in kilometers
        - Duration (min): activity duration in minutes
        - Elevation (m): elevation gain in meters
        - Average Speed (km/h): average speed in km/h
        - Activity Type: specific activity type
        - Activity Group: grouped activity category
        
    Raises:
        FileNotFoundError: If the CSV file cannot be found.
        ValueError: If required columns are missing from the CSV.
        
    Examples:
        >>> df = load_strava_data()
        >>> print(df.head())
        >>> df_custom = load_strava_data("path/to/activities.csv")
    """
    if file_path is None:
        file_path = DATA_FILE_PATH
    
    # Load CSV - handle both file paths (strings) and UploadedFile objects
    df = pd.read_csv(file_path)
    
    # Convert Activity Date to datetime
    df["Activity Date"] = pd.to_datetime(df["Activity Date"])
    
    # Remove commas from numeric columns (sometimes present in swimming distances)
    df["Distance"] = df["Distance"].astype(str).str.replace(',', '')
    
    # Convert numeric columns to float, handling any non-numeric values
    df["Distance"] = pd.to_numeric(df["Distance"], errors='coerce')
    df["Elapsed Time"] = pd.to_numeric(df["Elapsed Time"], errors='coerce')
    df["Elevation Gain"] = pd.to_numeric(df["Elevation Gain"], errors='coerce')
    df["Average Speed"] = pd.to_numeric(df["Average Speed"], errors='coerce')
    
    # Handle activity types first (needed for swim and rowing distance conversion)
    df["Activity Type"] = df["Activity Type"].fillna("Unknown")
    df["Activity Group"] = df["Activity Type"].map(ACTIVITY_GROUP_MAP)
    
    # Detect cycling subtypes for rides
    # Apply detect_cycling_subtype to all rows where Activity Type is 'Ride'
    ride_mask = df["Activity Type"] == "Ride"
    if ride_mask.any():
        df.loc[ride_mask, "Activity Group"] = df.loc[ride_mask].apply(detect_cycling_subtype, axis=1)
    
    # Create derived columns
    # Swimming and Rowing distances in Strava CSV are in meters, convert to km
    df["Distance (km)"] = df["Distance"].copy()
    df.loc[df["Activity Type"] == "Swim", "Distance (km)"] = df.loc[df["Activity Type"] == "Swim", "Distance"] / 1000
    df.loc[df["Activity Type"] == "Rowing", "Distance (km)"] = df.loc[df["Activity Type"] == "Rowing", "Distance"] / 1000
    
    df["Duration (min)"] = df["Elapsed Time"] / 60
    df["Elevation (m)"] = df["Elevation Gain"]
    
    # Calculate average speed from distance and time (more reliable than CSV value)
    # Convert to km/h: (distance in km) / (time in hours)
    df["Average Speed (km/h)"] = df["Distance (km)"] / (df["Duration (min)"] / 60)
    
    # Replace infinite or very high speeds (likely errors) with NaN
    df.loc[df["Average Speed (km/h)"] > 100, "Average Speed (km/h)"] = pd.NA
    df.loc[df["Average Speed (km/h)"] <= 0, "Average Speed (km/h)"] = pd.NA
    
    # Drop rows with missing values in key columns
    df = df.dropna(subset=["Distance (km)", "Duration (min)"])
    
    return df.sort_values("Activity Date", ascending=False)


def filter_by_activities(df: pd.DataFrame, selected_activities: list[str]) -> pd.DataFrame:
    """Filter DataFrame by selected activity groups.
    
    Args:
        df: DataFrame containing activity data with 'Activity Group' column.
        selected_activities: List of activity group names to include.
        
    Returns:
        Filtered DataFrame containing only the selected activity groups.
        
    Examples:
        >>> filtered_df = filter_by_activities(df, ["Running", "Cycling"])
    """
    return df[df["Activity Group"].isin(selected_activities)]


def filter_by_date_range(df: pd.DataFrame, days_back: int) -> pd.DataFrame:
    """Filter DataFrame to include only recent activities.
    
    Args:
        df: DataFrame containing activity data with 'Activity Date' column.
        days_back: Number of days to look back from today.
        
    Returns:
        Filtered DataFrame containing only activities from the last N days.
        
    Examples:
        >>> recent_df = filter_by_date_range(df, 30)  # Last 30 days
    """
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days_back)
    return df[df["Activity Date"] >= cutoff_date]


def get_quarterly_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate activity statistics by quarter.
    
    Args:
        df: DataFrame containing activity data.
        
    Returns:
        DataFrame with quarterly aggregated statistics including:
        - Total Distance (km)
        - Total Duration (hours)
        - Total Elevation (m)
        - Activity Count
        
    Examples:
        >>> quarterly = get_quarterly_stats(df)
        >>> print(quarterly.head())
    """
    df_quarterly = df.copy()
    df_quarterly["Quarter"] = df_quarterly["Activity Date"].dt.to_period("Q")
    
    quarterly_stats = df_quarterly.groupby("Quarter").agg({
        "Distance (km)": "sum",
        "Duration (min)": "sum",
        "Elevation (m)": "sum",
        "Activity Type": "count"
    }).reset_index()
    
    quarterly_stats.columns = [
        "Quarter", "Total Distance (km)", "Total Duration (min)", 
        "Total Elevation (m)", "Activity Count"
    ]
    quarterly_stats["Total Duration (hours)"] = (
        quarterly_stats["Total Duration (min)"] / 60
    ).round(1)
    quarterly_stats["Quarter"] = quarterly_stats["Quarter"].astype(str)
    
    return quarterly_stats.sort_values("Quarter", ascending=False)


def get_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly activity trends.
    
    Args:
        df: DataFrame containing activity data.
        
    Returns:
        DataFrame with monthly aggregated data for trend analysis.
        
    Examples:
        >>> monthly = get_monthly_trends(df)
    """
    df_timeline = df.copy()
    df_timeline["Quarter"] = df_timeline["Activity Date"].dt.to_period("Q").astype(str)
    
    monthly_data = df_timeline.groupby("Quarter").agg({
        "Distance (km)": "sum",
        "Duration (min)": "sum",
        "Activity Group": "count"
    }).reset_index()
    
    monthly_data.columns = ["Quarter", "Distance", "Duration", "Activity Count"]
    monthly_data["Duration (hours)"] = (monthly_data["Duration"] / 60).round(1)
    monthly_data = monthly_data.sort_values("Quarter")
    monthly_data["Cumulative Distance"] = monthly_data["Distance"].cumsum()
    monthly_data["Rolling Avg Distance"] = monthly_data["Distance"].rolling(window=2).mean()
    
    return monthly_data


def get_aggregated_trends(df: pd.DataFrame, interval: str = "quarterly") -> pd.DataFrame:
    """Aggregate activity trends by specified time interval.
    
    Args:
        df: DataFrame containing activity data.
        interval: Time interval for aggregation. Options:
            - "monthly": Monthly aggregation
            - "quarterly": Quarterly aggregation (default)
            - "annual": Yearly aggregation
            - "alltime": No aggregation, single data point for all time
            
    Returns:
        DataFrame with aggregated data including:
        - Period: Time period label
        - Distance: Total distance in km
        - Duration: Total duration in minutes
        - Activity Count: Number of activities
        - Duration (hours): Total duration in hours
        - Cumulative Distance: Running total distance
        - Rolling Avg Distance: Moving average distance
        
    Examples:
        >>> monthly_trends = get_aggregated_trends(df, "monthly")
        >>> annual_trends = get_aggregated_trends(df, "annual")
    """
    df_timeline = df.copy()
    
    # Map interval to pandas period code
    interval_map = {
        "monthly": "M",
        "quarterly": "Q",
        "annual": "Y"
    }
    
    if interval == "alltime":
        # Single aggregation for all time
        aggregated_data = pd.DataFrame([{
            "Period": "All Time",
            "Distance": df["Distance (km)"].sum(),
            "Duration": df["Duration (min)"].sum(),
            "Activity Count": len(df)
        }])
    else:
        period_code = interval_map.get(interval, "Q")
        df_timeline["Period"] = df_timeline["Activity Date"].dt.to_period(period_code).astype(str)
        
        aggregated_data = df_timeline.groupby("Period").agg({
            "Distance (km)": "sum",
            "Duration (min)": "sum",
            "Activity Group": "count"
        }).reset_index()
        
        aggregated_data.columns = ["Period", "Distance", "Duration", "Activity Count"]
    
    # Add calculated fields
    aggregated_data["Duration (hours)"] = (aggregated_data["Duration"] / 60).round(1)
    aggregated_data = aggregated_data.sort_values("Period")
    aggregated_data["Cumulative Distance"] = aggregated_data["Distance"].cumsum()
    
    # Calculate rolling average (window size depends on interval)
    window_size = 3 if interval == "monthly" else 2
    aggregated_data["Rolling Avg Distance"] = aggregated_data["Distance"].rolling(window=window_size).mean()
    
    return aggregated_data


def get_stacked_activity_data(df: pd.DataFrame, interval: str = "quarterly") -> pd.DataFrame:
    """Aggregate activity type composition by time interval.
    
    Args:
        df: DataFrame containing activity data with 'Activity Date' and 'Activity Group' columns.
        interval: Time interval for aggregation ("monthly", "quarterly", "annual", "alltime").
        
    Returns:
        DataFrame with columns: Period, Activity Group, Count.
        
    Examples:
        >>> stacked_data = get_stacked_activity_data(df, "monthly")
    """
    df_timeline = df.copy()
    
    interval_map = {
        "monthly": "M",
        "quarterly": "Q",
        "annual": "Y"
    }
    
    if interval == "alltime":
        # Single aggregation for all time
        activity_counts = df.groupby("Activity Group").size().reset_index(name="Count")
        activity_counts["Period"] = "All Time"
        return activity_counts[["Period", "Activity Group", "Count"]]
    else:
        period_code = interval_map.get(interval, "Q")
        df_timeline["Period"] = df_timeline["Activity Date"].dt.to_period(period_code).astype(str)
        
        activity_by_period = df_timeline.groupby(["Period", "Activity Group"]).size().reset_index(name="Count")
        return activity_by_period.sort_values("Period")
