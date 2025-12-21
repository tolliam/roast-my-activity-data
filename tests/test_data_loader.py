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
