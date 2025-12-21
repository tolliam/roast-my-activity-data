"""Unit tests for utils module."""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO

from src.utils import (
    calculate_fun_metrics,
    get_personal_records,
    calculate_summary_stats,
    calculate_exercise_obsession_score,
    calculate_cheeky_metrics,
    format_metric_display
)
from src.config import EARTH_CIRCUMFERENCE_KM, EVEREST_HEIGHT_M


def create_sample_dataframe():
    """Helper function to create sample activity data."""
    today = datetime.now()
    data = {
        'Activity Date': [
            today - timedelta(days=1),
            today - timedelta(days=2),
            today - timedelta(days=3),
            today - timedelta(days=10),
        ],
        'Activity Type': ['Run', 'Ride', 'Run', 'Walk'],
        'Distance (km)': [10.0, 50.0, 5.0, 3.0],
        'Duration (min)': [60.0, 120.0, 30.0, 40.0],
        'Elevation (m)': [100.0, 500.0, 50.0, 20.0],
        'Average Speed (km/h)': [10.0, 25.0, 10.0, 4.5]
    }
    return pd.DataFrame(data)


def test_calculate_fun_metrics():
    """Test calculation of fun comparative metrics."""
    df = create_sample_dataframe()
    
    metrics = calculate_fun_metrics(df)
    
    # Test that all expected keys are present
    expected_keys = [
        'total_distance', 'total_elevation', 'total_hours', 'total_activities',
        'times_around_world', 'times_up_everest', 'days_active', 'activities_per_week'
    ]
    for key in expected_keys:
        assert key in metrics, f"Expected key '{key}' not found in metrics"
    
    # Test total distance calculation
    assert metrics['total_distance'] == 68.0, f"Expected 68.0 km, got {metrics['total_distance']}"
    
    # Test total elevation calculation
    assert metrics['total_elevation'] == 670.0, f"Expected 670.0 m, got {metrics['total_elevation']}"
    
    # Test total hours calculation (250 minutes = 4.166... hours)
    expected_hours = 250.0 / 60
    assert abs(metrics['total_hours'] - expected_hours) < 0.01, f"Expected {expected_hours:.2f} hours, got {metrics['total_hours']}"
    
    # Test total activities
    assert metrics['total_activities'] == 4, f"Expected 4 activities, got {metrics['total_activities']}"
    
    # Test times around world calculation
    expected_times_around_world = 68.0 / EARTH_CIRCUMFERENCE_KM
    assert abs(metrics['times_around_world'] - expected_times_around_world) < 0.0001
    
    # Test times up everest calculation
    expected_times_up_everest = 670.0 / EVEREST_HEIGHT_M
    assert abs(metrics['times_up_everest'] - expected_times_up_everest) < 0.0001


def test_get_personal_records():
    """Test extraction of personal records."""
    df = create_sample_dataframe()
    
    prs = get_personal_records(df)
    
    # Test that all expected keys are present
    expected_keys = ['longest_distance', 'longest_duration', 'most_elevation', 'fastest_speed']
    for key in expected_keys:
        assert key in prs, f"Expected key '{key}' not found in personal records"
    
    # Test longest distance
    assert prs['longest_distance'] == 50.0, f"Expected 50.0 km, got {prs['longest_distance']}"
    
    # Test longest duration
    assert prs['longest_duration'] == 120.0, f"Expected 120.0 min, got {prs['longest_duration']}"
    
    # Test most elevation
    assert prs['most_elevation'] == 500.0, f"Expected 500.0 m, got {prs['most_elevation']}"
    
    # Test fastest speed
    assert prs['fastest_speed'] == 25.0, f"Expected 25.0 km/h, got {prs['fastest_speed']}"


def test_calculate_summary_stats():
    """Test calculation of summary statistics."""
    df = create_sample_dataframe()
    
    stats = calculate_summary_stats(df)
    
    # Test that all expected keys are present
    expected_keys = ['total_activities', 'total_distance', 'total_duration', 'total_elevation']
    for key in expected_keys:
        assert key in stats, f"Expected key '{key}' not found in stats"
    
    # Test total activities
    assert stats['total_activities'] == 4, f"Expected 4 activities, got {stats['total_activities']}"
    
    # Test total distance
    assert stats['total_distance'] == 68.0, f"Expected 68.0 km, got {stats['total_distance']}"
    
    # Test total duration in hours (250 minutes = 4.166... hours)
    expected_hours = 250.0 / 60
    assert abs(stats['total_duration'] - expected_hours) < 0.01, f"Expected {expected_hours:.2f} hours, got {stats['total_duration']}"
    
    # Test total elevation
    assert stats['total_elevation'] == 670.0, f"Expected 670.0 m, got {stats['total_elevation']}"


def test_calculate_exercise_obsession_score():
    """Test exercise obsession score calculation."""
    df = create_sample_dataframe()
    
    score, level, description = calculate_exercise_obsession_score(df)
    
    # Test that score is within valid range
    assert 0 <= score <= 100, f"Score should be between 0 and 100, got {score}"
    
    # Test that level is a non-empty string
    assert isinstance(level, str), f"Level should be a string, got {type(level)}"
    assert len(level) > 0, "Level should not be empty"
    
    # Test that description is a non-empty string
    assert isinstance(description, str), f"Description should be a string, got {type(description)}"
    assert len(description) > 0, "Description should not be empty"


def test_calculate_exercise_obsession_score_high_volume():
    """Test exercise obsession score with high volume data."""
    # Create data for someone who exercises 7 days a week for 3 months
    start_date = datetime.now() - timedelta(days=90)
    dates = [start_date + timedelta(days=i) for i in range(90)]
    
    data = {
        'Activity Date': dates,
        'Activity Type': ['Run'] * 90,
        'Distance (km)': [10.0] * 90,
        'Duration (min)': [60.0] * 90,
        'Elevation (m)': [100.0] * 90,
        'Average Speed (km/h)': [10.0] * 90
    }
    df = pd.DataFrame(data)
    
    score, level, description = calculate_exercise_obsession_score(df)
    
    # With daily activities for 90 days, score should be high
    # Expected minimum of 60 based on: high frequency (25 pts), high volume (25 pts),
    # perfect consistency (20 pts), and some dedication/variety points
    assert score >= 60, f"Expected high score for daily exerciser, got {score}"


def test_calculate_cheeky_metrics():
    """Test calculation of cheeky, humorous metrics."""
    df = create_sample_dataframe()
    
    metrics = calculate_cheeky_metrics(df)
    
    # Test that all expected keys are present
    expected_keys = [
        'marathons', 'bananas', 'football_pitches',
        'eiffel_towers', 'empire_states', 'burj_khalifas',
        'friends_episodes', 'lotr_trilogies',
        'big_macs', 'pizza_slices', 'beers',
        'faster_than_sloth', 'percent_of_bolt'
    ]
    for key in expected_keys:
        assert key in metrics, f"Expected key '{key}' not found in cheeky metrics"
    
    # Test marathons calculation (68 km / 42.195 km)
    expected_marathons = 68.0 / 42.195
    assert abs(metrics['marathons'] - expected_marathons) < 0.01
    
    # Test that all metrics are positive numbers
    for key, value in metrics.items():
        assert isinstance(value, (int, float)), f"Metric '{key}' should be numeric, got {type(value)}"
        assert value >= 0, f"Metric '{key}' should be non-negative, got {value}"


def test_format_metric_display_earth():
    """Test formatting of Earth circumference metrics."""
    # Test when value >= 1
    display, help_text = format_metric_display(1.5, 'earth')
    assert display == "1.50x", f"Expected '1.50x', got '{display}'"
    assert "40" in help_text and "km" in help_text  # Check for Earth circumference in some format
    
    # Test when value < 1
    display, help_text = format_metric_display(0.25, 'earth')
    assert display == "25.0%", f"Expected '25.0%', got '{display}'"
    assert "40" in help_text and "km" in help_text


def test_format_metric_display_everest():
    """Test formatting of Everest height metrics."""
    # Test when value >= 1
    display, help_text = format_metric_display(2.0, 'everest')
    assert display == "2.0x", f"Expected '2.0x', got '{display}'"
    assert "Everest" in help_text and "m" in help_text  # Check for Everest height in some format
    
    # Test when value < 1
    display, help_text = format_metric_display(0.5, 'everest')
    assert display == "50%", f"Expected '50%', got '{display}'"
    assert "8" in help_text and "m" in help_text  # Check for height value in meters


def test_format_metric_display_time():
    """Test formatting of time metrics."""
    # Test when value >= 365 (years)
    display, help_text = format_metric_display(400, 'time')
    assert "year" in display, f"Expected 'year' in display, got '{display}'"
    assert "hours" in help_text
    
    # Test when value < 365 (days)
    display, help_text = format_metric_display(30, 'time')
    assert "30 days" in display, f"Expected '30 days' in display, got '{display}'"
    assert "hours" in help_text


def test_calculate_fun_metrics_with_single_activity():
    """Test fun metrics calculation with a single activity."""
    today = datetime.now()
    data = {
        'Activity Date': [today],
        'Distance (km)': [10.0],
        'Duration (min)': [60.0],
        'Elevation (m)': [100.0],
    }
    df = pd.DataFrame(data)
    
    metrics = calculate_fun_metrics(df)
    
    # Test single activity totals
    assert metrics['total_distance'] == 10.0
    assert metrics['total_activities'] == 1
    assert metrics['total_elevation'] == 100.0
