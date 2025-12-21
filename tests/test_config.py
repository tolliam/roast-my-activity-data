"""Unit tests for config module."""

import pytest
from src.config import (
    VERSION,
    APP_TITLE,
    DEFAULT_DAYS_BACK,
    MIN_DAYS_BACK,
    MAX_DAYS_BACK,
    DATA_FILE_PATH,
    EARTH_CIRCUMFERENCE_KM,
    EVEREST_HEIGHT_M,
    WEEKS_PER_YEAR,
    ACTIVITY_COLORS,
    ACTIVITY_GROUP_MAP,
    CUSTOM_CSS,
    PLOTLY_LIGHT_THEME,
    PLOTLY_DARK_THEME
)


def test_version_constant():
    """Test that version constant is defined."""
    assert isinstance(VERSION, str), "VERSION should be a string"
    assert len(VERSION) > 0, "VERSION should not be empty"


def test_app_title_constant():
    """Test that app title is defined."""
    assert isinstance(APP_TITLE, str), "APP_TITLE should be a string"
    assert len(APP_TITLE) > 0, "APP_TITLE should not be empty"
    assert "Roast" in APP_TITLE, "APP_TITLE should contain 'Roast'"


def test_days_back_constants():
    """Test days back configuration constants."""
    assert isinstance(DEFAULT_DAYS_BACK, int), "DEFAULT_DAYS_BACK should be an integer"
    assert isinstance(MIN_DAYS_BACK, int), "MIN_DAYS_BACK should be an integer"
    assert isinstance(MAX_DAYS_BACK, int), "MAX_DAYS_BACK should be an integer"
    
    # Test logical relationships
    assert MIN_DAYS_BACK <= DEFAULT_DAYS_BACK <= MAX_DAYS_BACK, \
        "Days back constants should follow: MIN <= DEFAULT <= MAX"
    assert MIN_DAYS_BACK > 0, "MIN_DAYS_BACK should be positive"


def test_data_file_path_constant():
    """Test that data file path is defined."""
    assert isinstance(DATA_FILE_PATH, str), "DATA_FILE_PATH should be a string"
    assert len(DATA_FILE_PATH) > 0, "DATA_FILE_PATH should not be empty"
    assert DATA_FILE_PATH.endswith('.csv'), "DATA_FILE_PATH should be a CSV file"


def test_physical_constants():
    """Test physical constants are defined with reasonable values."""
    assert isinstance(EARTH_CIRCUMFERENCE_KM, int), "EARTH_CIRCUMFERENCE_KM should be an integer"
    assert EARTH_CIRCUMFERENCE_KM == 40075, "Earth circumference should be 40,075 km"
    
    assert isinstance(EVEREST_HEIGHT_M, int), "EVEREST_HEIGHT_M should be an integer"
    assert EVEREST_HEIGHT_M == 8849, "Everest height should be 8,849 m"
    
    assert isinstance(WEEKS_PER_YEAR, int), "WEEKS_PER_YEAR should be an integer"
    assert WEEKS_PER_YEAR == 52, "Weeks per year should be 52"


def test_activity_colors_dict():
    """Test activity colors dictionary structure."""
    assert isinstance(ACTIVITY_COLORS, dict), "ACTIVITY_COLORS should be a dictionary"
    assert len(ACTIVITY_COLORS) > 0, "ACTIVITY_COLORS should not be empty"
    
    # Test that all values are valid hex color codes
    for activity, color in ACTIVITY_COLORS.items():
        assert isinstance(activity, str), f"Activity key '{activity}' should be a string"
        assert isinstance(color, str), f"Color for '{activity}' should be a string"
        assert color.startswith('#'), f"Color '{color}' for '{activity}' should start with '#'"
        assert len(color) == 7, f"Color '{color}' for '{activity}' should be 7 characters (#RRGGBB)"
    
    # Test for expected activity types
    expected_activities = ["Running", "Cycling", "Swimming", "Walking", "Strength", "Other"]
    for activity in expected_activities:
        assert activity in ACTIVITY_COLORS, f"Expected activity '{activity}' not found in ACTIVITY_COLORS"


def test_activity_group_map_dict():
    """Test activity group mapping dictionary structure."""
    assert isinstance(ACTIVITY_GROUP_MAP, dict), "ACTIVITY_GROUP_MAP should be a dictionary"
    assert len(ACTIVITY_GROUP_MAP) > 0, "ACTIVITY_GROUP_MAP should not be empty"
    
    # Test that all keys and values are strings
    for activity_type, group in ACTIVITY_GROUP_MAP.items():
        assert isinstance(activity_type, str), f"Activity type '{activity_type}' should be a string"
        assert isinstance(group, str), f"Group for '{activity_type}' should be a string"
    
    # Test for expected mappings
    expected_mappings = {
        "Run": "Running",
        "Ride": "Cycling",
        "Walk": "Walking",
        "Swim": "Swimming"
    }
    for activity_type, expected_group in expected_mappings.items():
        assert activity_type in ACTIVITY_GROUP_MAP, f"Expected activity type '{activity_type}' not found"
        assert ACTIVITY_GROUP_MAP[activity_type] == expected_group, \
            f"Expected '{activity_type}' to map to '{expected_group}', got '{ACTIVITY_GROUP_MAP[activity_type]}'"


def test_activity_group_map_groups_have_colors():
    """Test that all groups in ACTIVITY_GROUP_MAP have corresponding colors."""
    unique_groups = set(ACTIVITY_GROUP_MAP.values())
    
    for group in unique_groups:
        assert group in ACTIVITY_COLORS, \
            f"Group '{group}' from ACTIVITY_GROUP_MAP not found in ACTIVITY_COLORS"


def test_custom_css_string():
    """Test that custom CSS is defined."""
    assert isinstance(CUSTOM_CSS, str), "CUSTOM_CSS should be a string"
    assert len(CUSTOM_CSS) > 0, "CUSTOM_CSS should not be empty"
    assert "<style>" in CUSTOM_CSS, "CUSTOM_CSS should contain <style> tag"
    assert "</style>" in CUSTOM_CSS, "CUSTOM_CSS should contain </style> tag"


def test_plotly_light_theme_dict():
    """Test plotly light theme structure."""
    assert isinstance(PLOTLY_LIGHT_THEME, dict), "PLOTLY_LIGHT_THEME should be a dictionary"
    
    # Test for expected keys
    expected_keys = ["plot_bgcolor", "paper_bgcolor", "font_color", "grid_color", "title_color"]
    for key in expected_keys:
        assert key in PLOTLY_LIGHT_THEME, f"Expected key '{key}' not found in PLOTLY_LIGHT_THEME"
        assert isinstance(PLOTLY_LIGHT_THEME[key], str), \
            f"Value for '{key}' in PLOTLY_LIGHT_THEME should be a string"


def test_plotly_dark_theme_dict():
    """Test plotly dark theme structure."""
    assert isinstance(PLOTLY_DARK_THEME, dict), "PLOTLY_DARK_THEME should be a dictionary"
    
    # Test for expected keys
    expected_keys = ["plot_bgcolor", "paper_bgcolor", "font_color", "grid_color", "title_color"]
    for key in expected_keys:
        assert key in PLOTLY_DARK_THEME, f"Expected key '{key}' not found in PLOTLY_DARK_THEME"
        assert isinstance(PLOTLY_DARK_THEME[key], str), \
            f"Value for '{key}' in PLOTLY_DARK_THEME should be a string"


def test_plotly_themes_have_same_keys():
    """Test that light and dark themes have the same keys."""
    light_keys = set(PLOTLY_LIGHT_THEME.keys())
    dark_keys = set(PLOTLY_DARK_THEME.keys())
    
    assert light_keys == dark_keys, \
        f"Light and dark themes should have the same keys. Difference: {light_keys.symmetric_difference(dark_keys)}"
