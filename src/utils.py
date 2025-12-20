"""Utility functions for calculating statistics and fun metrics.

This module provides helper functions for computing interesting statistics
about activities, such as personal records and comparative metrics.
"""

import pandas as pd
from typing import Dict, Tuple

from src.config import EARTH_CIRCUMFERENCE_KM, EVEREST_HEIGHT_M, WEEKS_PER_YEAR


def calculate_exercise_obsession_score(df: pd.DataFrame) -> Tuple[int, str, str]:
    """Calculate how obsessed someone is with exercise (0-100 scale).
    
    Analyzes multiple factors including frequency, consistency, volume,
    and variety to determine exercise addiction level.
    
    Args:
        df: DataFrame containing activity data.
        
    Returns:
        Tuple of (score, level_name, description) where:
        - score: 0-100 obsession rating
        - level_name: Category like "Casual Dabbler", "Weekend Warrior", etc.
        - description: Cheeky description of their exercise habits
        
    Examples:
        >>> score, level, desc = calculate_exercise_obsession_score(df)
        >>> print(f"You're a {level} scoring {score}/100!")
    """
    total_activities = len(df)
    date_range_days = (df['Activity Date'].max() - df['Activity Date'].min()).days
    
    if date_range_days == 0:
        date_range_days = 1
    
    # Factor 1: Activities per week (0-25 points)
    activities_per_week = (total_activities / date_range_days) * 7
    frequency_score = min(25, activities_per_week * 5)  # Cap at 25
    
    # Factor 2: Total hours spent (0-25 points) 
    total_hours = df['Duration (min)'].sum() / 60
    hours_per_week = (total_hours / date_range_days) * 7
    volume_score = min(25, hours_per_week * 2.5)  # 10 hrs/week = max
    
    # Factor 3: Consistency - how many weeks have activities (0-20 points)
    df_with_week = df.copy()
    df_with_week['week'] = df_with_week['Activity Date'].dt.to_period('W')
    active_weeks = df_with_week['week'].nunique()
    total_weeks = max(1, date_range_days / 7)
    consistency_score = (active_weeks / total_weeks) * 20
    
    # Factor 4: Variety of activities (0-15 points)
    unique_activities = df['Activity Type'].nunique()
    variety_score = min(15, unique_activities * 3)  # 5+ types = max
    
    # Factor 5: Weekend warrior vs daily grind (0-15 points)
    df_with_day = df.copy()
    df_with_day['day_of_week'] = df_with_day['Activity Date'].dt.dayofweek
    weekend_activities = len(df_with_day[df_with_day['day_of_week'].isin([5, 6])])
    weekday_activities = total_activities - weekend_activities
    balance_ratio = min(weekday_activities, weekend_activities) / max(1, total_activities)
    dedication_score = balance_ratio * 15
    
    # Total score
    total_score = int(frequency_score + volume_score + consistency_score + 
                     variety_score + dedication_score)
    
    # Determine level and description
    if total_score >= 85:
        level = "Exercise Addict 🔥"
        description = "You probably dream about workouts. Your rest days need rest days."
    elif total_score >= 70:
        level = "Fitness Fanatic 💪"
        description = "Your gym bag is permanently packed. You know all the PTs by name."
    elif total_score >= 55:
        level = "Committed Crusher 🏃"
        description = "You've got a routine and you stick to it. Rain or shine, you're out there."
    elif total_score >= 40:
        level = "Enthusiastic Amateur 🚴"
        description = "You're keen when the weather's nice. Mostly nice."
    elif total_score >= 25:
        level = "Weekend Warrior ⚽"
        description = "Mondays are for recovery. And Tuesdays. Actually, most days really."
    elif total_score >= 10:
        level = "Casual Dabbler 🚶"
        description = "You exercise sometimes. When you remember. Or when your jeans get tight."
    else:
        level = "Couch Enthusiast 🛋️"
        description = "You're more of a 'spiritual' athlete. Thinking about it counts, right?"
    
    return total_score, level, description


def calculate_cheeky_metrics(df: pd.DataFrame) -> Dict[str, any]:
    """Calculate cheeky, humorous alternative metrics.
    
    Converts your boring athletic achievements into fun, relatable comparisons
    that will make you laugh (or cringe).
    
    Args:
        df: DataFrame containing activity data.
        
    Returns:
        Dictionary containing cheeky metrics like marathons in beer cans,
        Big Macs burned, years of Friends episodes, etc.
        
    Examples:
        >>> metrics = calculate_cheeky_metrics(df)
        >>> print(f"You burned {metrics['big_macs']:.0f} Big Macs worth of calories!")
    """
    total_distance = df['Distance (km)'].sum()
    total_elevation = df['Elevation (m)'].sum()
    total_hours = df['Duration (min)'].sum() / 60
    total_minutes = df['Duration (min)'].sum()
    
    # Distance comparisons
    banana_length_m = 0.18  # Average banana is 18cm (USDA)
    football_pitch_m = 105  # Standard football pitch length (FIFA/Premier League)
    marathons = total_distance / 42.195  # Official marathon distance (IAAF)
    bananas = (total_distance * 1000) / banana_length_m
    football_pitches = (total_distance * 1000) / football_pitch_m
    
    # Elevation comparisons
    eiffel_tower_m = 330  # To the tip (Paris official)
    empire_state_m = 443  # To the roof (ESB official)
    burj_khalifa_m = 828  # Total height (Emaar Properties)
    eiffel_towers = total_elevation / eiffel_tower_m
    empire_states = total_elevation / empire_state_m
    burj_khalifas = total_elevation / burj_khalifa_m
    
    # Time comparisons
    friends_episode_min = 22  # Average runtime without ads (NBC)
    lotr_trilogy_min = 558  # Extended editions total (New Line Cinema)
    friends_episodes = total_minutes / friends_episode_min
    lotr_trilogies = total_minutes / lotr_trilogy_min
    
    # Calorie comparisons
    # Estimated: ~50 cal/km for running/cycling mix (Mayo Clinic)
    estimated_calories = total_distance * 50
    big_mac_calories = 563  # McDonald's official nutrition info
    pizza_slice_calories = 285  # Large pepperoni, 1/8 pizza (USDA)
    beer_calories = 150  # Average 12oz beer (USDA)
    big_macs = estimated_calories / big_mac_calories
    pizza_slices = estimated_calories / pizza_slice_calories
    beers = estimated_calories / beer_calories
    
    # Speed comparisons (based on distance traveled at avg speed)
    avg_speed_kmh = total_distance / total_hours if total_hours > 0 else 0
    sloth_speed_kmh = 0.24  # Three-toed sloth max speed (National Geographic)
    usain_bolt_kmh = 44.72  # World record 100m pace (IAAF)
    
    # Time to cover your total distance at different speeds
    sloth_hours = total_distance / sloth_speed_kmh if sloth_speed_kmh > 0 else 0
    your_hours = total_hours
    time_saved_vs_sloth = sloth_hours - your_hours
    faster_than_sloth = sloth_hours / your_hours if your_hours > 0 else 0
    percent_of_bolt = (avg_speed_kmh / usain_bolt_kmh * 100) if usain_bolt_kmh > 0 else 0
    
    return {
        # Distance
        'marathons': marathons,
        'bananas': bananas,
        'football_pitches': football_pitches,
        
        # Elevation
        'eiffel_towers': eiffel_towers,
        'empire_states': empire_states,
        'burj_khalifas': burj_khalifas,
        
        # Time
        'friends_episodes': friends_episodes,
        'lotr_trilogies': lotr_trilogies,
        
        # Calories
        'big_macs': big_macs,
        'pizza_slices': pizza_slices,
        'beers': beers,
        
        # Speed
        'faster_than_sloth': faster_than_sloth,
        'percent_of_bolt': percent_of_bolt,
    }


def calculate_fun_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate fun comparative metrics from activity data.
    
    Computes interesting statistics like how many times around Earth
    you've traveled, how many times up Everest you've climbed, etc.
    
    Args:
        df: DataFrame containing activity data with Distance (km),
            Elevation (m), and Duration (min) columns.
            
    Returns:
        Dictionary containing:
        - total_distance: Total distance in km
        - total_elevation: Total elevation gain in meters
        - total_hours: Total activity time in hours
        - total_activities: Total number of activities
        - times_around_world: How many Earth circumferences traveled
        - times_up_everest: How many times Everest height climbed
        - days_active: Total days worth of activity time
        - activities_per_week: Average activities per week
        
    Examples:
        >>> metrics = calculate_fun_metrics(df)
        >>> print(f"You've traveled {metrics['times_around_world']:.2f}x around Earth!")
    """
    total_distance = df['Distance (km)'].sum()
    total_elevation = df['Elevation (m)'].sum()
    total_hours = df['Duration (min)'].sum() / 60
    total_activities = len(df)
    
    # Calculate actual time span of activities
    date_range = (df['Activity Date'].max() - df['Activity Date'].min()).days
    actual_weeks = date_range / 7 if date_range > 0 else 1
    
    times_around_world = total_distance / EARTH_CIRCUMFERENCE_KM
    times_up_everest = total_elevation / EVEREST_HEIGHT_M
    days_active = total_hours / 24
    activities_per_week = total_activities / actual_weeks
    
    return {
        'total_distance': total_distance,
        'total_elevation': total_elevation,
        'total_hours': total_hours,
        'total_activities': total_activities,
        'times_around_world': times_around_world,
        'times_up_everest': times_up_everest,
        'days_active': days_active,
        'activities_per_week': activities_per_week
    }


def get_personal_records(df: pd.DataFrame) -> Dict[str, float]:
    """Extract personal records from activity data.
    
    Args:
        df: DataFrame containing activity data.
        
    Returns:
        Dictionary containing personal records:
        - longest_distance: Longest single activity distance (km)
        - longest_duration: Longest single activity duration (min)
        - most_elevation: Most elevation gain in single activity (m)
        - fastest_speed: Fastest average speed (km/h)
        
    Examples:
        >>> prs = get_personal_records(df)
        >>> print(f"Longest distance: {prs['longest_distance']:.1f} km")
    """
    return {
        'longest_distance': df["Distance (km)"].max(),
        'longest_duration': df["Duration (min)"].max(),
        'most_elevation': df["Elevation (m)"].max(),
        'fastest_speed': df["Average Speed (km/h)"].max()
    }


def calculate_summary_stats(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate summary statistics for a set of activities.
    
    Args:
        df: DataFrame containing activity data.
        
    Returns:
        Dictionary with summary statistics:
        - total_activities: Total number of activities
        - total_distance: Sum of all distances (km)
        - total_duration: Sum of all durations (hours)
        - total_elevation: Sum of all elevation gain (m)
        
    Examples:
        >>> stats = calculate_summary_stats(recent_df)
        >>> print(f"Total: {stats['total_distance']:.1f} km")
    """
    return {
        'total_activities': len(df),
        'total_distance': df['Distance (km)'].sum(),
        'total_duration': df['Duration (min)'].sum() / 60,
        'total_elevation': df['Elevation (m)'].sum()
    }


def format_metric_display(value: float, metric_type: str) -> Tuple[str, str]:
    """Format metrics for display with appropriate units and thresholds.
    
    Args:
        value: The numeric value to format.
        metric_type: Type of metric ('earth', 'everest', 'time').
        
    Returns:
        Tuple of (display_value, help_text) for streamlit metric display.
        
    Examples:
        >>> display, help_text = format_metric_display(1.5, 'earth')
        >>> print(display)  # "1.50x"
    """
    if metric_type == 'earth':
        if value >= 1:
            return f"{value:.2f}x", f"Based on {EARTH_CIRCUMFERENCE_KM:,} km circumference"
        else:
            percentage = value * 100
            return f"{percentage:.1f}%", f"Progress towards {EARTH_CIRCUMFERENCE_KM:,} km"
            
    elif metric_type == 'everest':
        if value >= 1:
            return f"{value:.1f}x", f"Based on Everest's {EVEREST_HEIGHT_M:,}m height"
        else:
            percentage = value * 100
            return f"{percentage:.0f}%", f"Progress towards {EVEREST_HEIGHT_M:,}m"
            
    elif metric_type == 'time':
        if value >= 365:
            years = value / 365
            total_hours = int(value * 24)
            return f"{years:.1f} years", f"That's {total_hours:,} hours of activity!"
        else:
            total_hours = int(value * 24)
            return f"{int(value)} days", f"That's {total_hours:,} hours of activity!"
            
    return str(value), ""
