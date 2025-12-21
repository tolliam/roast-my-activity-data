"""Unit tests for data_loader module."""

import pytest
import pandas as pd
from datetime import datetime
from io import StringIO
from src.data_loader import load_strava_data, filter_by_activities, filter_by_date_range


def test_swimming_and_rowing_distance_conversion():
    """Test that swimming and rowing distances are correctly converted from meters to km."""
    # Create sample CSV data with distances in meters for Swim and Rowing
    csv_data = """Activity ID,Activity Date,Activity Name,Activity Type,Activity Description,Elapsed Time,Distance,Max Heart Rate,Relative Effort,Commute,Activity Private Note,Activity Gear,Filename,Athlete Weight,Bike Weight,Elapsed Time,Moving Time,Distance,Max Speed,Average Speed,Elevation Gain,Elevation Loss,Elevation Low,Elevation High
1,"Jan 1, 2024, 10:00:00 AM",Morning Swim,Swim,,1800,1000,,,false,,,,,,,1800,1000,,,10,,,
2,"Jan 2, 2024, 10:00:00 AM",Morning Row,Rowing,,600,2000,,,false,,,,,,,600,2000,,,5,,,
3,"Jan 3, 2024, 10:00:00 AM",Morning Ride,Ride,,3600,25.5,,,false,,,,,,,3600,25.5,,,100,,,
4,"Jan 4, 2024, 10:00:00 AM",Morning Run,Run,,1800,5.0,,,false,,,,,,,1800,5.0,,,50,,,"""
    
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
