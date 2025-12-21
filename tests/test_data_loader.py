"""Unit tests for data_loader module."""

import pytest
import pandas as pd
from datetime import datetime
from io import StringIO
from src.data_loader import load_strava_data, filter_by_activities, filter_by_date_range


def test_swimming_and_rowing_distance_conversion():
    """Test that swimming and rowing distances are correctly converted from meters to km."""
    # Create minimal CSV data with only the columns needed for testing
    # Swimming and Rowing distances are in meters in the CSV, other activities are in km
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"Jan 1, 2024, 10:00:00 AM",Swim,1800,1000,2.0,10
"Jan 2, 2024, 10:00:00 AM",Rowing,600,2000,12.0,5
"Jan 3, 2024, 10:00:00 AM",Ride,3600,25.5,25.5,100
"Jan 4, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50"""
    
    # Create a StringIO object to simulate a file
    csv_file = StringIO(csv_data)
    
    # Load the data
    df = load_strava_data(csv_file)
    
    # Test swimming distance conversion (1000m -> 1.0 km)
    swim_dist = df[df['Activity Type'] == 'Swim']['Distance (km)'].iloc[0]
    assert swim_dist == 1.0, f"Swimming distance should be 1.0 km, got {swim_dist}"
    
    # Test rowing distance conversion (2000m -> 2.0 km)
    row_dist = df[df['Activity Type'] == 'Rowing']['Distance (km)'].iloc[0]
    assert row_dist == 2.0, f"Rowing distance should be 2.0 km, got {row_dist}"
    
    # Test that cycling distance is not converted (already in km)
    ride_dist = df[df['Activity Type'] == 'Ride']['Distance (km)'].iloc[0]
    assert ride_dist == 25.5, f"Ride distance should remain 25.5 km, got {ride_dist}"
    
    # Test that running distance is not converted (already in km)
    run_dist = df[df['Activity Type'] == 'Run']['Distance (km)'].iloc[0]
    assert run_dist == 5.0, f"Run distance should remain 5.0 km, got {run_dist}"


def test_filter_by_activities():
    """Test filtering by activity groups."""
    # Create sample data with various activity types
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"Jan 1, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50
"Jan 2, 2024, 10:00:00 AM",Ride,3600,25.5,25.5,100
"Jan 3, 2024, 10:00:00 AM",Swim,1800,1000,2.0,10
"Jan 4, 2024, 10:00:00 AM",Walk,2400,4.0,6.0,30"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Test filtering for only Running
    filtered = filter_by_activities(df, ["Running"])
    assert len(filtered) == 1, f"Expected 1 Running activity, got {len(filtered)}"
    assert filtered.iloc[0]["Activity Type"] == "Run"
    
    # Test filtering for multiple activity groups
    filtered = filter_by_activities(df, ["Running", "Cycling"])
    assert len(filtered) == 2, f"Expected 2 activities (Running, Cycling), got {len(filtered)}"
    
    # Test filtering with no matches
    filtered = filter_by_activities(df, ["Skiing"])
    assert len(filtered) == 0, f"Expected 0 activities, got {len(filtered)}"
    
    # Test filtering with all activities
    all_groups = df["Activity Group"].unique()
    filtered = filter_by_activities(df, all_groups)
    assert len(filtered) == len(df), f"Expected {len(df)} activities, got {len(filtered)}"


def test_filter_by_date_range():
    """Test date range filtering."""
    from datetime import datetime, timedelta
    
    # Create sample data with dates spread over 60 days
    today = datetime.now()
    csv_data = f"""Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"{(today - timedelta(days=5)).strftime('%b %d, %Y, %I:%M:%S %p')}",Run,1800,5.0,10.0,50
"{(today - timedelta(days=15)).strftime('%b %d, %Y, %I:%M:%S %p')}",Ride,3600,25.5,25.5,100
"{(today - timedelta(days=35)).strftime('%b %d, %Y, %I:%M:%S %p')}",Run,1800,5.0,10.0,50
"{(today - timedelta(days=50)).strftime('%b %d, %Y, %I:%M:%S %p')}",Walk,2400,4.0,6.0,30"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Test 10 days back (should get 1 activity)
    filtered = filter_by_date_range(df, 10)
    assert len(filtered) == 1, f"Expected 1 activity in last 10 days, got {len(filtered)}"
    
    # Test 30 days back (should get 2 activities)
    filtered = filter_by_date_range(df, 30)
    assert len(filtered) == 2, f"Expected 2 activities in last 30 days, got {len(filtered)}"
    
    # Test 60 days back (should get 4 activities)
    filtered = filter_by_date_range(df, 60)
    assert len(filtered) == 4, f"Expected 4 activities in last 60 days, got {len(filtered)}"
    
    # Test 1 day back (should get 0 activities)
    filtered = filter_by_date_range(df, 1)
    assert len(filtered) == 0, f"Expected 0 activities in last 1 day, got {len(filtered)}"


def test_load_strava_data():
    """Test data loading and preprocessing."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"Jan 1, 2024, 10:00:00 AM",Run,3600,10.0,10.0,100
"Jan 2, 2024, 10:00:00 AM",Ride,7200,50.0,25.0,200"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Test that data is loaded
    assert len(df) == 2, f"Expected 2 activities, got {len(df)}"
    
    # Test that Activity Date is datetime
    assert pd.api.types.is_datetime64_any_dtype(df["Activity Date"]), "Activity Date should be datetime"
    
    # Test that derived columns are created
    assert "Distance (km)" in df.columns, "Distance (km) column should exist"
    assert "Duration (min)" in df.columns, "Duration (min) column should exist"
    assert "Elevation (m)" in df.columns, "Elevation (m) column should exist"
    assert "Average Speed (km/h)" in df.columns, "Average Speed (km/h) column should exist"
    assert "Activity Group" in df.columns, "Activity Group column should exist"
    
    # Test that Duration is correctly calculated (3600 seconds = 60 minutes)
    run_duration = df[df["Activity Type"] == "Run"]["Duration (min)"].iloc[0]
    assert run_duration == 60.0, f"Expected 60 minutes, got {run_duration}"
    
    # Test that Activity Group mapping works
    run_group = df[df["Activity Type"] == "Run"]["Activity Group"].iloc[0]
    assert run_group == "Running", f"Expected 'Running' group, got {run_group}"
    
    ride_group = df[df["Activity Type"] == "Ride"]["Activity Group"].iloc[0]
    assert ride_group == "Cycling", f"Expected 'Cycling' group, got {ride_group}"
    
    # Test that data is sorted by date (descending)
    assert df["Activity Date"].is_monotonic_decreasing, "Data should be sorted by date descending"
