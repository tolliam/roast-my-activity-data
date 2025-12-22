import pandas as pd
from typing import Dict, Any

# Activity type to group mappings
ACTIVITY_GROUP_MAP = {
    "Run": "Cardio",
    "Ride": "Cardio",
    "Walk": "Cardio",
    "Hike": "Cardio",
    "Swim": "Cardio",
    "Rowing": "Cardio",
    "EBikeRide": "Cardio",
    "VirtualRide": "Cardio",
    "VirtualRun": "Cardio",
    "Elliptical": "Cardio",
    "Crossfit": "Gym",
    "Weight Training": "Gym",
    "Workout": "Gym",
    "Yoga": "Yoga",
    "Rock Climbing": "Other",
    "Ice Skate": "Other",
    "Alpine Ski": "Other",
    "Backcountry Ski": "Other",
    "Nordic Ski": "Other",
    "Snowboard": "Other",
    "Snowshoe": "Other",
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
