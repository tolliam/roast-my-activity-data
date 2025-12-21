"""Unit tests for utils module."""

import pytest
import pandas as pd
from datetime import datetime
from src.utils import get_personal_records, calculate_summary_stats, calculate_fun_metrics


def test_get_personal_records_dynamic():
    """Test that personal records are calculated dynamically from data, not hardcoded."""
    # Create test data with known values
    test_data = {
        'Activity Date': [datetime(2024, 1, 1), datetime(2024, 1, 2), datetime(2024, 1, 3)],
        'Activity Type': ['Run', 'Ride', 'Run'],
        'Distance (km)': [10.0, 150.0, 5.0],  # Max: 150.0
        'Duration (min)': [60.0, 300.0, 30.0],  # Max: 300.0 (5 hours)
        'Elevation (m)': [100.0, 500.0, 50.0],  # Max: 500.0
        'Average Speed (km/h)': [10.0, 30.0, 10.0]  # Max: 30.0
    }
    df = pd.DataFrame(test_data)
    
    # Get personal records
    prs = get_personal_records(df)
    
    # Verify that PRs match the max values from data (not hardcoded)
    assert prs['longest_distance'] == 150.0, "Longest distance should be dynamically calculated"
    assert prs['longest_duration'] == 300.0, "Longest duration should be dynamically calculated"
    assert prs['most_elevation'] == 500.0, "Most elevation should be dynamically calculated"
    assert prs['fastest_speed'] == 30.0, "Fastest speed should be dynamically calculated"


def test_get_personal_records_different_values():
    """Test that personal records change with different data sets."""
    # First dataset
    data1 = {
        'Activity Date': [datetime(2024, 1, 1)],
        'Activity Type': ['Run'],
        'Distance (km)': [50.0],
        'Duration (min)': [180.0],
        'Elevation (m)': [200.0],
        'Average Speed (km/h)': [16.7]
    }
    df1 = pd.DataFrame(data1)
    prs1 = get_personal_records(df1)
    
    # Second dataset with different values
    data2 = {
        'Activity Date': [datetime(2024, 1, 1)],
        'Activity Type': ['Run'],
        'Distance (km)': [100.0],  # Different
        'Duration (min)': [360.0],  # Different
        'Elevation (m)': [400.0],  # Different
        'Average Speed (km/h)': [25.0]  # Different
    }
    df2 = pd.DataFrame(data2)
    prs2 = get_personal_records(df2)
    
    # Verify that PRs are different (proving they're not hardcoded)
    assert prs1['longest_distance'] != prs2['longest_distance'], "PRs should differ with different data"
    assert prs1['longest_duration'] != prs2['longest_duration'], "PRs should differ with different data"
    assert prs1['most_elevation'] != prs2['most_elevation'], "PRs should differ with different data"
    assert prs1['fastest_speed'] != prs2['fastest_speed'], "PRs should differ with different data"


def test_get_personal_records_no_hardcoded_3000():
    """Specifically test that 3000 and 43 are not hardcoded values."""
    # Create data that should NOT return 3000 or 43
    test_data = {
        'Activity Date': [datetime(2024, 1, 1)],
        'Activity Type': ['Run'],
        'Distance (km)': [42.195],  # Marathon distance
        'Duration (min)': [180.0],  # 3 hours
        'Elevation (m)': [100.0],
        'Average Speed (km/h)': [14.065]
    }
    df = pd.DataFrame(test_data)
    prs = get_personal_records(df)
    
    # Ensure the results match our data, not hardcoded values
    assert prs['longest_distance'] == 42.195, "Should return actual data, not 3000"
    assert prs['longest_duration'] == 180.0, "Should return actual data, not 43*60"
    assert prs['most_elevation'] == 100.0, "Should return actual data, not 3000"
