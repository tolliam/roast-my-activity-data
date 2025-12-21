"""Unit tests for Winter Sports activity grouping."""

import pytest
from src.config import ACTIVITY_COLORS, ACTIVITY_GROUP_MAP


def test_winter_sports_activity_color_exists():
    """Test that Winter Sports activity group has a color defined."""
    assert "Winter Sports" in ACTIVITY_COLORS, "Winter Sports should be in ACTIVITY_COLORS"
    assert ACTIVITY_COLORS["Winter Sports"] is not None, "Winter Sports should have a color"
    # Verify it's a winter-themed light color (should start with # and be a valid hex)
    assert ACTIVITY_COLORS["Winter Sports"].startswith("#"), "Color should be a hex code"
    assert len(ACTIVITY_COLORS["Winter Sports"]) == 7, "Color should be in #RRGGBB format"


def test_ski_activities_map_to_winter_sports():
    """Test that all ski and snowboard activity types map to Winter Sports group."""
    ski_activities = ["Alpine Ski", "Backcountry Ski", "Nordic Ski", "Snowboard"]
    
    for activity in ski_activities:
        assert activity in ACTIVITY_GROUP_MAP, f"{activity} should be in ACTIVITY_GROUP_MAP"
        assert ACTIVITY_GROUP_MAP[activity] == "Winter Sports", \
            f"{activity} should map to Winter Sports, not {ACTIVITY_GROUP_MAP.get(activity)}"


def test_winter_sports_not_skiing():
    """Test that ski activities don't map to 'Skiing' anymore."""
    ski_activities = ["Alpine Ski", "Backcountry Ski", "Nordic Ski", "Snowboard"]
    
    for activity in ski_activities:
        if activity in ACTIVITY_GROUP_MAP:
            assert ACTIVITY_GROUP_MAP[activity] != "Skiing", \
                f"{activity} should not map to Skiing (should be Winter Sports)"


def test_activity_group_map_completeness():
    """Test that ACTIVITY_GROUP_MAP has all expected ski/snowboard activities."""
    expected_ski_activities = ["Alpine Ski", "Backcountry Ski", "Nordic Ski", "Snowboard"]
    
    for activity in expected_ski_activities:
        assert activity in ACTIVITY_GROUP_MAP, \
            f"{activity} is missing from ACTIVITY_GROUP_MAP"


def test_all_activity_groups_have_colors():
    """Test that all activity groups in MAP have corresponding colors."""
    # Get all unique groups from the map
    activity_groups = set(ACTIVITY_GROUP_MAP.values())
    
    for group in activity_groups:
        assert group in ACTIVITY_COLORS, \
            f"Activity group '{group}' is missing from ACTIVITY_COLORS"
