"""Unit tests for handling unmapped activity types."""

import pytest
import pandas as pd
from io import StringIO
from src.data_loader import load_strava_data


def test_unmapped_activity_types_default_to_other():
    """Test that activity types not in ACTIVITY_GROUP_MAP are mapped to 'Other'."""
    # Create CSV with unmapped activity types (Yoga, Dance)
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"Jan 1, 2024, 10:00:00 AM",Yoga,1800,0.0,0.0,0
"Jan 2, 2024, 10:00:00 AM",Dance,600,0.0,0.0,0"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Check that Activity Group column exists
    assert 'Activity Group' in df.columns, "Activity Group column should exist"
    
    # Check that all unmapped activities are mapped to "Other"
    activity_groups = df['Activity Group'].unique()
    assert len(activity_groups) == 1, "Should have only one activity group"
    assert activity_groups[0] == "Other", "Unmapped activities should map to 'Other'"
    
    # Ensure no NaN values in Activity Group
    assert df['Activity Group'].isna().sum() == 0, "Activity Group should not contain NaN values"


def test_mixed_mapped_and_unmapped_activities():
    """Test that mixed mapped and unmapped activities are handled correctly."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"Jan 1, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50
"Jan 2, 2024, 10:00:00 AM",Yoga,1800,0.0,0.0,0
"Jan 3, 2024, 10:00:00 AM",Dance,600,0.0,0.0,0
"Jan 4, 2024, 10:00:00 AM",Ride,3600,25.0,25.0,100"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Check that we have the expected activity groups
    activity_groups = sorted(df['Activity Group'].unique())
    assert "Running" in activity_groups, "Run should map to Running"
    assert "Cycling" in activity_groups, "Ride should map to Cycling"
    assert "Other" in activity_groups, "Unmapped activities should map to Other"
    
    # Ensure no NaN values
    assert df['Activity Group'].isna().sum() == 0, "Activity Group should not contain NaN values"
    
    # Verify sorting works without TypeError
    try:
        sorted_groups = sorted(df['Activity Group'].unique())
        assert isinstance(sorted_groups, list), "Should be able to sort activity groups"
    except TypeError as e:
        pytest.fail(f"Sorting activity groups should not raise TypeError: {e}")


def test_all_mapped_activities_still_work():
    """Test that fully mapped activities still work correctly."""
    csv_data = """Activity Date,Activity Type,Elapsed Time,Distance,Average Speed,Elevation Gain
"Jan 1, 2024, 10:00:00 AM",Run,1800,5.0,10.0,50
"Jan 2, 2024, 10:00:00 AM",Ride,3600,25.0,25.0,100
"Jan 3, 2024, 10:00:00 AM",Swim,1800,1000,2.0,0
"Jan 4, 2024, 10:00:00 AM",Walk,3600,4.0,4.0,20"""
    
    csv_file = StringIO(csv_data)
    df = load_strava_data(csv_file)
    
    # Check that all activities are correctly mapped
    activity_groups = sorted(df['Activity Group'].unique())
    assert "Running" in activity_groups, "Run should map to Running"
    assert "Cycling" in activity_groups, "Ride should map to Cycling"
    assert "Swimming" in activity_groups, "Swim should map to Swimming"
    assert "Walking" in activity_groups, "Walk should map to Walking"
    
    # Ensure no "Other" category is present (all are mapped)
    assert "Other" not in activity_groups, "All activities should be mapped, no 'Other'"
    
    # Ensure no NaN values
    assert df['Activity Group'].isna().sum() == 0, "Activity Group should not contain NaN values"
