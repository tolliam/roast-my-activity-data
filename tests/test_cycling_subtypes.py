"""Unit tests for cycling subtype detection and configuration."""

import pytest
import pandas as pd
from src.config import ACTIVITY_COLORS, ACTIVITY_GROUP_MAP, MTB_KEYWORDS, ROAD_CYCLING_KEYWORDS
from src.data_loader import detect_cycling_subtype


def test_cycling_subtype_colors_exist():
    """Test that all cycling subtypes have colors defined."""
    cycling_types = ["Cycling", "Mountain Biking", "Road Cycling"]
    
    for cycling_type in cycling_types:
        assert cycling_type in ACTIVITY_COLORS, f"{cycling_type} should be in ACTIVITY_COLORS"
        assert ACTIVITY_COLORS[cycling_type] is not None, f"{cycling_type} should have a color"
        assert ACTIVITY_COLORS[cycling_type].startswith("#"), f"{cycling_type} color should be a hex code"
        assert len(ACTIVITY_COLORS[cycling_type]) == 7, f"{cycling_type} color should be in #RRGGBB format"


def test_ride_maps_to_cycling():
    """Test that Ride activity type maps to Cycling by default."""
    assert "Ride" in ACTIVITY_GROUP_MAP, "Ride should be in ACTIVITY_GROUP_MAP"
    assert ACTIVITY_GROUP_MAP["Ride"] == "Cycling", "Ride should map to Cycling"


def test_mtb_keywords_exist():
    """Test that MTB keywords list exists and is not empty."""
    assert MTB_KEYWORDS is not None, "MTB_KEYWORDS should be defined"
    assert len(MTB_KEYWORDS) > 0, "MTB_KEYWORDS should not be empty"
    assert "mtb" in MTB_KEYWORDS, "MTB_KEYWORDS should include 'mtb'"
    assert "mountain bike" in MTB_KEYWORDS, "MTB_KEYWORDS should include 'mountain bike'"


def test_road_cycling_keywords_exist():
    """Test that road cycling keywords list exists and is not empty."""
    assert ROAD_CYCLING_KEYWORDS is not None, "ROAD_CYCLING_KEYWORDS should be defined"
    assert len(ROAD_CYCLING_KEYWORDS) > 0, "ROAD_CYCLING_KEYWORDS should not be empty"
    assert "road bike" in ROAD_CYCLING_KEYWORDS, "ROAD_CYCLING_KEYWORDS should include 'road bike'"


def test_detect_mtb_from_description():
    """Test that MTB is detected from activity description."""
    row = pd.Series({
        'Activity Name': 'Morning Ride',
        'Activity Description': 'MTB trail ride'
    })
    result = detect_cycling_subtype(row)
    assert result == "Mountain Biking", "Should detect Mountain Biking from 'MTB' in description"


def test_detect_mtb_from_name():
    """Test that MTB is detected from activity name."""
    row = pd.Series({
        'Activity Name': 'Mountain bike adventure',
        'Activity Description': 'Fun ride'
    })
    result = detect_cycling_subtype(row)
    assert result == "Mountain Biking", "Should detect Mountain Biking from 'mountain bike' in name"


def test_detect_mtb_case_insensitive():
    """Test that MTB detection is case insensitive."""
    row = pd.Series({
        'Activity Name': 'MTB Trail',
        'Activity Description': ''
    })
    result = detect_cycling_subtype(row)
    assert result == "Mountain Biking", "Should detect Mountain Biking regardless of case"


def test_detect_road_cycling_from_description():
    """Test that road cycling is detected from activity description."""
    row = pd.Series({
        'Activity Name': 'Morning Ride',
        'Activity Description': 'road bike training'
    })
    result = detect_cycling_subtype(row)
    assert result == "Road Cycling", "Should detect Road Cycling from 'road bike' in description"


def test_detect_road_cycling_from_name():
    """Test that road cycling is detected from activity name."""
    row = pd.Series({
        'Activity Name': 'Road cycling training',
        'Activity Description': ''
    })
    result = detect_cycling_subtype(row)
    assert result == "Road Cycling", "Should detect Road Cycling from 'road cycling' in name"


def test_default_to_cycling():
    """Test that rides without specific keywords default to generic Cycling."""
    row = pd.Series({
        'Activity Name': 'Morning Ride',
        'Activity Description': 'Nice day for a ride'
    })
    result = detect_cycling_subtype(row)
    assert result == "Cycling", "Should default to generic Cycling when no specific keywords found"


def test_mtb_takes_precedence():
    """Test that MTB keywords take precedence over road cycling keywords."""
    row = pd.Series({
        'Activity Name': 'MTB ride',
        'Activity Description': 'Started on the road then hit the trails'
    })
    result = detect_cycling_subtype(row)
    assert result == "Mountain Biking", "MTB keywords should take precedence"


def test_handle_missing_description():
    """Test that function handles missing description gracefully."""
    row = pd.Series({
        'Activity Name': 'Ride',
        'Activity Description': None
    })
    result = detect_cycling_subtype(row)
    assert result == "Cycling", "Should handle missing description without error"


def test_handle_missing_name():
    """Test that function handles missing name gracefully."""
    row = pd.Series({
        'Activity Name': None,
        'Activity Description': 'MTB trail'
    })
    result = detect_cycling_subtype(row)
    assert result == "Mountain Biking", "Should handle missing name without error"


def test_all_cycling_groups_have_colors():
    """Test that all cycling groups have colors defined."""
    cycling_groups = ["Cycling", "Mountain Biking", "Road Cycling"]
    
    for group in cycling_groups:
        assert group in ACTIVITY_COLORS, f"Cycling group '{group}' is missing from ACTIVITY_COLORS"
