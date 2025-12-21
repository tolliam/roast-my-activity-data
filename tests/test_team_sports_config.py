"""Unit tests for Team Sports activity grouping."""

import pytest
from src.config import ACTIVITY_COLORS, ACTIVITY_GROUP_MAP


def test_team_sports_activity_color_exists():
    """Test that Team Sports activity group has a color defined."""
    assert "Team Sports" in ACTIVITY_COLORS, "Team Sports should be in ACTIVITY_COLORS"
    assert ACTIVITY_COLORS["Team Sports"] is not None, "Team Sports should have a color"
    # Verify it's a valid hex color
    assert ACTIVITY_COLORS["Team Sports"].startswith("#"), "Color should be a hex code"
    assert len(ACTIVITY_COLORS["Team Sports"]) == 7, "Color should be in #RRGGBB format"
    # Verify it's the specified red color
    assert ACTIVITY_COLORS["Team Sports"] == "#D4351C", "Team Sports should be red (#D4351C)"


def test_team_sport_activities_map_to_team_sports():
    """Test that all team sport activity types map to Team Sports group."""
    team_sport_activities = ["Rugby", "Football", "Netball", "Basketball", "Soccer"]
    
    for activity in team_sport_activities:
        assert activity in ACTIVITY_GROUP_MAP, f"{activity} should be in ACTIVITY_GROUP_MAP"
        assert ACTIVITY_GROUP_MAP[activity] == "Team Sports", \
            f"{activity} should map to Team Sports, not {ACTIVITY_GROUP_MAP.get(activity)}"


def test_activity_group_map_team_sports_completeness():
    """Test that ACTIVITY_GROUP_MAP has all expected team sport activities."""
    expected_team_sports = ["Rugby", "Football", "Netball", "Basketball", "Soccer"]
    
    for activity in expected_team_sports:
        assert activity in ACTIVITY_GROUP_MAP, \
            f"{activity} is missing from ACTIVITY_GROUP_MAP"


def test_all_activity_groups_have_colors():
    """Test that all activity groups in MAP have corresponding colors."""
    # Get all unique groups from the map
    activity_groups = set(ACTIVITY_GROUP_MAP.values())
    
    for group in activity_groups:
        assert group in ACTIVITY_COLORS, \
            f"Activity group '{group}' is missing from ACTIVITY_COLORS"
