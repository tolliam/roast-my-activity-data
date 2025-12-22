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
    csv_data = """Activity Date,Activity Type,Moving Time,Distance,Average Speed,Elevation Gain
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


# Placeholder tests - implement with actual test data
def test_filter_by_activities():
    """Test filtering by activity groups."""
    # TODO: Implement with sample data
    pass


def test_filter_by_date_range():
    """Test date range filtering."""
    # TODO: Implement with sample data
    pass


def test_load_strava_data():
    """Test data loading and preprocessing."""
    # TODO: Implement with sample CSV
    pass


def test_unknown_activity_types_map_to_other():
    """Test that unmapped activity types default to 'Other' group."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"Jan 1, 2024, 10:00:00 AM",Kayaking,3600,10.0,10.0,50
"Jan 2, 2024, 10:00:00 AM",Rock Climbing,7200,0.5,0.25,500
"Jan 3, 2024, 10:00:00 AM",Yoga,1800,2.0,4.0,0"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # All unknown types should map to "Other"
    assert len(df) == 3, "Expected 3 rows with unknown activity types"
    assert (df["Activity Group"] == "Other").all(), "All unknown activity types should map to 'Other'"
    
    # Verify the specific activity types are present
    assert "Kayaking" in df["Activity Type"].values
    assert "Rock Climbing" in df["Activity Type"].values
    assert "Yoga" in df["Activity Type"].values


def test_known_activity_types_map_correctly():
    """Test that known activity types map to their correct groups."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"Jan 1, 2024, 10:00:00 AM",Run,3600,10.0,10.0,50
"Jan 2, 2024, 10:00:00 AM",Virtual Run,1800,5.0,10.0,25
"Jan 3, 2024, 10:00:00 AM",Ride,7200,50.0,25.0,200
"Jan 4, 2024, 10:00:00 AM",Swim,1800,1000,2.0,0
"Jan 5, 2024, 10:00:00 AM",Open Water Swim,3600,2.0,2.0,0
"Jan 6, 2024, 10:00:00 AM",Alpine Ski,5400,15.0,10.0,800
"Jan 7, 2024, 10:00:00 AM",Backcountry Ski,7200,12.0,6.0,1200
"Jan 8, 2024, 10:00:00 AM",Nordic Ski,5400,20.0,13.3,300
"Jan 9, 2024, 10:00:00 AM",Snowboard,3600,10.0,10.0,600
"Jan 10, 2024, 10:00:00 AM",Rugby,5400,5.0,3.33,10
"Jan 11, 2024, 10:00:00 AM",Football,5400,7.0,4.67,15
"Jan 12, 2024, 10:00:00 AM",Soccer,5400,8.0,5.33,20
"Jan 13, 2024, 10:00:00 AM",Basketball,3600,4.0,4.0,5
"Jan 14, 2024, 10:00:00 AM",Netball,3600,3.0,3.0,5"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Test Running activities
    running_activities = df[df["Activity Type"].isin(["Run", "Virtual Run"])]
    assert len(running_activities) == 2
    assert (running_activities["Activity Group"] == "Running").all()
    
    # Test Cycling activities
    cycling_activities = df[df["Activity Type"] == "Ride"]
    assert len(cycling_activities) == 1
    assert (cycling_activities["Activity Group"] == "Cycling").all()
    
    # Test Swimming activities
    swimming_activities = df[df["Activity Type"].isin(["Swim", "Open Water Swim"])]
    assert len(swimming_activities) == 2
    assert (swimming_activities["Activity Group"] == "Swimming").all()
    # Also verify Swim distance conversion (meters to km)
    swim_activity = df[df["Activity Type"] == "Swim"]
    assert len(swim_activity) == 1
    assert swim_activity["Distance (km)"].iloc[0] == 1.0  # 1000m -> 1.0km
    
    # Test Winter Sports activities
    winter_activities = df[df["Activity Type"].isin(["Alpine Ski", "Backcountry Ski", "Nordic Ski", "Snowboard"])]
    assert len(winter_activities) == 4
    assert (winter_activities["Activity Group"] == "Winter Sports").all()
    
    # Test Team Sports activities
    team_activities = df[df["Activity Type"].isin(["Rugby", "Football", "Soccer", "Basketball", "Netball"])]
    assert len(team_activities) == 5
    assert (team_activities["Activity Group"] == "Team Sports").all()


def test_null_missing_activity_types_handled():
    """Test that null/missing activity types are handled correctly."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"Jan 1, 2024, 10:00:00 AM",,3600,10.0,10.0,50
"Jan 2, 2024, 10:00:00 AM",Run,1800,5.0,10.0,25
"Jan 3, 2024, 10:00:00 AM",,7200,20.0,10.0,100"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Check that missing activity types are filled with "Unknown"
    unknown_activities = df[df["Activity Type"] == "Unknown"]
    assert len(unknown_activities) == 2
    
    # Verify they map to "Other" group
    assert (unknown_activities["Activity Group"] == "Other").all()
    
    # Verify Run activity still maps correctly
    run_activities = df[df["Activity Type"] == "Run"]
    assert len(run_activities) == 1
    assert (run_activities["Activity Group"] == "Running").all()


def test_mixed_known_and_unknown_activities():
    """Test mixed known and unknown activity types are handled correctly."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"Jan 1, 2024, 10:00:00 AM",Run,3600,10.0,10.0,50
"Jan 2, 2024, 10:00:00 AM",Kayaking,3600,8.0,8.0,30
"Jan 3, 2024, 10:00:00 AM",Ride,7200,50.0,25.0,200
"Jan 4, 2024, 10:00:00 AM",Yoga,1800,0.5,1.0,0
"Jan 5, 2024, 10:00:00 AM",Swim,1800,1500,2.5,0
"Jan 6, 2024, 10:00:00 AM",Rock Climbing,5400,2.0,1.33,600
"Jan 7, 2024, 10:00:00 AM",Alpine Ski,5400,15.0,10.0,800
"Jan 8, 2024, 10:00:00 AM",Pilates,1800,1.0,2.0,0
"Jan 9, 2024, 10:00:00 AM",Rugby,5400,5.0,3.33,10"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Expected groups
    expected_groups = {
        "Run": "Running",
        "Kayaking": "Other",
        "Ride": "Cycling",
        "Yoga": "Other",
        "Swim": "Swimming",
        "Rock Climbing": "Other",
        "Alpine Ski": "Winter Sports",
        "Pilates": "Other",
        "Rugby": "Team Sports"
    }
    
    # Verify all expected activity types are present
    for activity_type, expected_group in expected_groups.items():
        activity_df = df[df["Activity Type"] == activity_type]
        assert len(activity_df) > 0, f"{activity_type} should be present in dataframe"
        actual_group = activity_df["Activity Group"].iloc[0]
        assert actual_group == expected_group, f"{activity_type} should map to {expected_group}, got {actual_group}"
    
    # Verify counts by group
    assert len(df[df["Activity Group"] == "Running"]) == 1
    assert len(df[df["Activity Group"] == "Cycling"]) == 1
    assert len(df[df["Activity Group"] == "Swimming"]) == 1
    assert len(df[df["Activity Group"] == "Winter Sports"]) == 1
    assert len(df[df["Activity Group"] == "Team Sports"]) == 1
    assert len(df[df["Activity Group"] == "Other"]) == 4  # Kayaking, Yoga, Rock Climbing, Pilates
