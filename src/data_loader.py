import pandas as pd
from typing import Dict, Any, Union
from datetime import datetime, timedelta
import streamlit as st

# Activity type to group mappings - Updated to match config.py
ACTIVITY_GROUP_MAP = {
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

def load_and_process_data(csv_path: str) -> pd.DataFrame:
    """
    Load and process Strava activity data from CSV.
    
    Args:
        csv_path: Path to the Strava activities CSV file
        
    Returns:
        Processed DataFrame with cleaned and derived columns
    """
    # Load CSV
    df = pd.read_csv(csv_path)
    
    # Check for required columns
    required_columns = ["Activity Date", "Activity Type", "Distance"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"CSV missing required columns: {missing_columns}")
    
    # Parse activity date
    df["Activity Date"] = pd.to_datetime(df["Activity Date"], errors='coerce')
    
    # Drop rows with invalid dates
    df = df.dropna(subset=["Activity Date"])
    
    # Sort by date
    df = df.sort_values("Activity Date")
    
    # Convert numeric columns to float, handling any non-numeric values
    df["Distance"] = pd.to_numeric(df["Distance"], errors='coerce')
    # Load both Moving Time and Elapsed Time if available
    if "Moving Time" in df.columns:
        df["Moving Time"] = pd.to_numeric(df["Moving Time"], errors='coerce')
    if "Elapsed Time" in df.columns:
        df["Elapsed Time"] = pd.to_numeric(df["Elapsed Time"], errors='coerce')
    df["Elevation Gain"] = pd.to_numeric(df["Elevation Gain"], errors='coerce')
    df["Average Speed"] = pd.to_numeric(df["Average Speed"], errors='coerce')
    
    # Handle activity types first (needed for time selection and distance conversion)
    df["Activity Type"] = df["Activity Type"].fillna("Unknown")
    # Map activity types to groups, defaulting to "Other" for unmapped types
    df["Activity Group"] = df["Activity Type"].map(ACTIVITY_GROUP_MAP).fillna("Other")
    
    # Use Elapsed Time for gym/stationary activities (where rest periods are part of workout),
    # Moving Time for movement-based activities (where stops should be excluded)
    stationary_activities = ["Weight Training", "Workout", "Rowing", "Yoga"]
    if "Moving Time" in df.columns and "Elapsed Time" in df.columns:
        # For stationary activities, use Elapsed Time
        df["Time"] = df["Moving Time"]  # Default to Moving Time
        df.loc[df["Activity Type"].isin(stationary_activities), "Time"] = df.loc[df["Activity Type"].isin(stationary_activities), "Elapsed Time"]
    elif "Moving Time" in df.columns:
        df["Time"] = df["Moving Time"]
    elif "Elapsed Time" in df.columns:
        df["Time"] = df["Elapsed Time"]
    else:
        raise ValueError("CSV must contain either 'Moving Time' or 'Elapsed Time' column")
    
    # Create derived columns
    # Swimming and Rowing distances in Strava CSV are in meters, convert to km
    df["Distance (km)"] = df["Distance"].copy()
    df.loc[df["Activity Type"] == "Swim", "Distance (km)"] = df.loc[df["Activity Type"] == "Swim", "Distance"] / 1000
    df.loc[df["Activity Type"] == "Rowing", "Distance (km)"] = df.loc[df["Activity Type"] == "Rowing", "Distance"] / 1000
    
    df["Duration (min)"] = df["Time"] / 60
    
    # Fill NaN values with 0 for numeric columns
    numeric_cols = ["Distance (km)", "Duration (min)", "Elevation Gain", "Average Speed"]
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    return df

def get_summary_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate summary statistics from activity data.
    
    Args:
        df: Processed activity DataFrame
        
    Returns:
        Dictionary of summary statistics
    """
    return {
        "total_activities": len(df),
        "total_distance_km": df["Distance (km)"].sum(),
        "total_duration_hours": df["Duration (min)"].sum() / 60,
        "total_elevation_gain_m": df["Elevation Gain"].sum(),
        "activities_by_type": df["Activity Type"].value_counts().to_dict(),
        "activities_by_group": df["Activity Group"].value_counts().to_dict(),
        "date_range": {
            "start": df["Activity Date"].min(),
            "end": df["Activity Date"].max()
        }
    }


@st.cache_data
def load_strava_data(data_source: Union[str, Any]) -> pd.DataFrame:
    """
    Load and process Strava activity data with caching.
    
    Args:
        data_source: Either a file path (str) or an uploaded file object
        
    Returns:
        Processed DataFrame with cleaned and derived columns
    """
    return load_and_process_data(data_source)


def filter_by_activities(df: pd.DataFrame, selected_activities: list) -> pd.DataFrame:
    """
    Filter DataFrame by selected activity types.
    
    Args:
        df: Activity DataFrame
        selected_activities: List of activity groups to include (e.g., ["Running", "Cycling"])
        
    Returns:
        Filtered DataFrame
    """
    if selected_activities is None or len(selected_activities) == 0:
        return df
    
    return df[df["Activity Group"].isin(selected_activities)].copy()


def filter_by_date_range(df: pd.DataFrame, days_back: int) -> pd.DataFrame:
    """
    Filter DataFrame to include only activities within the specified number of days.
    
    Args:
        df: Activity DataFrame
        days_back: Number of days to look back from today
        
    Returns:
        Filtered DataFrame
    """
    cutoff_date = datetime.now() - timedelta(days=days_back)
    return df[df["Activity Date"] >= cutoff_date].copy()


def get_quarterly_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate activity data by quarter.
    
    Args:
        df: Activity DataFrame
        
    Returns:
        DataFrame with quarterly aggregated statistics
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    df_copy = df.copy()
    df_copy["Quarter"] = df_copy["Activity Date"].dt.to_period("Q").astype(str)
    
    quarterly = df_copy.groupby("Quarter").agg({
        "Distance (km)": "sum",
        "Duration (min)": "sum",
        "Elevation Gain": "sum",
        "Activity Type": "count"
    }).reset_index()
    
    quarterly.columns = ["Quarter", "Distance", "Duration", "Elevation", "Activity Count"]
    quarterly["Duration (hours)"] = (quarterly["Duration"] / 60).round(1)
    
    return quarterly.sort_values("Quarter")


def get_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate activity data by month.
    
    Args:
        df: Activity DataFrame
        
    Returns:
        DataFrame with monthly aggregated statistics
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    df_copy = df.copy()
    df_copy["Month"] = df_copy["Activity Date"].dt.to_period("M").astype(str)
    
    monthly = df_copy.groupby("Month").agg({
        "Distance (km)": "sum",
        "Duration (min)": "sum",
        "Elevation Gain": "sum",
        "Activity Type": "count"
    }).reset_index()
    
    monthly.columns = ["Month", "Distance", "Duration", "Elevation", "Activity Count"]
    monthly["Duration (hours)"] = (monthly["Duration"] / 60).round(1)
    
    return monthly.sort_values("Month")


def get_aggregated_trends(df: pd.DataFrame, time_interval: str = "quarter") -> pd.DataFrame:
    """
    Aggregate activity data by the specified time interval.
    
    Args:
        df: Activity DataFrame
        time_interval: Time interval for aggregation ("month", "quarter", "year", "alltime")
        
    Returns:
        DataFrame with aggregated statistics
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    df_copy = df.copy()
    
    if time_interval == "month":
        df_copy["Period"] = df_copy["Activity Date"].dt.to_period("M").astype(str)
    elif time_interval == "quarter":
        df_copy["Period"] = df_copy["Activity Date"].dt.to_period("Q").astype(str)
    elif time_interval == "year":
        df_copy["Period"] = df_copy["Activity Date"].dt.to_period("Y").astype(str)
    elif time_interval == "alltime":
        # For alltime, aggregate everything into a single period
        df_copy["Period"] = "All Time"
    else:
        # Default to quarter
        df_copy["Period"] = df_copy["Activity Date"].dt.to_period("Q").astype(str)
    
    aggregated = df_copy.groupby("Period").agg({
        "Distance (km)": "sum",
        "Duration (min)": "sum",
        "Elevation Gain": "sum",
        "Activity Type": "count"
    }).reset_index()
    
    aggregated.columns = ["Period", "Distance", "Duration", "Elevation", "Activity Count"]
    aggregated["Duration (hours)"] = (aggregated["Duration"] / 60).round(1)
    
    # Calculate cumulative distance
    aggregated = aggregated.sort_values("Period")
    aggregated["Cumulative Distance"] = aggregated["Distance"].cumsum()
    
    return aggregated


def get_stacked_activity_data(df: pd.DataFrame, time_interval: str = "quarter") -> pd.DataFrame:
    """
    Prepare activity data for stacked charts by activity group and time period.
    
    Args:
        df: Activity DataFrame
        time_interval: Time interval for aggregation ("month", "quarter", "year", "alltime")
        
    Returns:
        DataFrame with activity counts by group and period
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    df_copy = df.copy()
    
    if time_interval == "month":
        df_copy["Period"] = df_copy["Activity Date"].dt.to_period("M").astype(str)
    elif time_interval == "quarter":
        df_copy["Period"] = df_copy["Activity Date"].dt.to_period("Q").astype(str)
    elif time_interval == "year":
        df_copy["Period"] = df_copy["Activity Date"].dt.to_period("Y").astype(str)
    elif time_interval == "alltime":
        # For alltime, aggregate everything into a single period
        df_copy["Period"] = "All Time"
    else:
        # Default to quarter
        df_copy["Period"] = df_copy["Activity Date"].dt.to_period("Q").astype(str)
    
    # Group by period and activity group
    stacked = df_copy.groupby(["Period", "Activity Group"]).agg({
        "Activity Type": "count",
        "Distance (km)": "sum"
    }).reset_index()
    
    stacked.columns = ["Period", "Activity Group", "Count", "Distance"]
    
    return stacked.sort_values("Period")
