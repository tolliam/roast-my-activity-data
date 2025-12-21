"""Unit tests for data_loader module."""

import pytest
import pandas as pd
from datetime import datetime
from io import StringIO
from src.data_loader import (
    load_strava_data, filter_by_activities, filter_by_date_range,
    filter_races, filter_training
)


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


def test_competition_field_handling():
    """Test that Competition field is properly loaded and converted to boolean."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain,Competition
"Jan 1, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,True
"Jan 2, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,False
"Jan 3, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,
"Jan 4, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,1"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Check that Competition column exists
    assert "Competition" in df.columns, "Competition column should exist"
    
    # Check that it's boolean type
    assert df["Competition"].dtype == bool, "Competition should be boolean"
    
    # Check values
    assert df.iloc[0]["Competition"] == True, "First activity should be a race"
    assert df.iloc[1]["Competition"] == False, "Second activity should not be a race"
    assert df.iloc[2]["Competition"] == False, "Empty values should be False"
    assert df.iloc[3]["Competition"] == True, "1 should be converted to True"


def test_filter_races():
    """Test filtering to get only race activities."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain,Competition
"Jan 1, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,True
"Jan 2, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,False
"Jan 3, 2024, 10:00:00 AM",Ride,3600,25.5,25.5,100,True
"Jan 4, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,False"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Filter races
    races = filter_races(df)
    
    # Should have 2 races
    assert len(races) == 2, f"Should have 2 races, got {len(races)}"
    
    # All should be marked as Competition
    assert races["Competition"].all(), "All filtered activities should be races"


def test_filter_training():
    """Test filtering to get only training activities (non-races)."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain,Competition
"Jan 1, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,True
"Jan 2, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,False
"Jan 3, 2024, 10:00:00 AM",Ride,3600,25.5,25.5,100,True
"Jan 4, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,False"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Filter training
    training = filter_training(df)
    
    # Should have 2 training activities
    assert len(training) == 2, f"Should have 2 training activities, got {len(training)}"
    
    # None should be marked as Competition
    assert not training["Competition"].any(), "No filtered activities should be races"


def test_races_and_training_sum_to_total():
    """Test that races + training equals total activities."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain,Competition
"Jan 1, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,True
"Jan 2, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,False
"Jan 3, 2024, 10:00:00 AM",Ride,3600,25.5,25.5,100,True
"Jan 4, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,False
"Jan 5, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50,"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    races = filter_races(df)
    training = filter_training(df)
    
    # Sum should equal total
    assert len(races) + len(training) == len(df), "Races + Training should equal total activities"


def test_missing_competition_column():
    """Test that missing Competition column is handled gracefully."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"Jan 1, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50
"Jan 2, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Competition column should be added with False values
    assert "Competition" in df.columns, "Competition column should be created"
    assert not df["Competition"].any(), "All activities should be non-races when column is missing"
    
    # filter_races should return empty dataframe
    races = filter_races(df)
    assert len(races) == 0, "Should have no races when Competition column is missing"
    
    # filter_training should return all activities
    training = filter_training(df)
    assert len(training) == len(df), "All activities should be training when Competition column is missing"


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
