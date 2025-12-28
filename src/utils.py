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
        description = "Your gear is always ready to go. Exercise is a lifestyle, not a hobby."
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
        - longest_duration: Longest single activity duration using moving time (min)
        - most_elevation: Most elevation gain in single activity (m)
        - fastest_speed: Fastest average speed (km/h)
        
    Examples:
        >>> prs = get_personal_records(df)
        >>> print(f"Longest distance: {prs['longest_distance']:.1f} km")
    """
    # Define minimum realistic speeds by activity type (km/h)
    # Activities slower than this are likely GPS errors (left on overnight, etc.)
    min_speeds = {
        'Cycling': 5.0,      # Very slow touring
        'Running': 3.0,      # Very slow jog
        'Hiking': 1.0,       # Slow hike
        'Walking': 1.0,      # Slow walk
        'Swimming': 0.5,     # Very slow swim
        'Strength': 0.0,     # No minimum for stationary activities
        'Winter Sports': 3.0,
        'Team Sports': 2.0,
        'Other': 0.0
    }
    
    # Use Moving Time for duration if available, otherwise fall back to Duration (min)
    if 'Moving Time' in df.columns:
        # Create a copy with calculated speed from moving time
        df_copy = df.copy()
        df_copy['Calculated Speed'] = df_copy['Distance (km)'] / (df_copy['Moving Time'] / 3600)
        
        # Filter out unrealistically slow activities for each group
        realistic_activities = []
        for activity_group in df_copy['Activity Group'].unique():
            group_df = df_copy[df_copy['Activity Group'] == activity_group]
            min_speed = min_speeds.get(activity_group, 0.0)
            
            if min_speed > 0:
                realistic = group_df[group_df['Calculated Speed'] >= min_speed]
                realistic_activities.append(realistic)
            else:
                realistic_activities.append(group_df)
        
        if realistic_activities:
            filtered_df = pd.concat(realistic_activities, ignore_index=True)
            if len(filtered_df) > 0:
                longest_duration = (filtered_df['Moving Time'] / 60).max()
            else:
                longest_duration = (df['Moving Time'] / 60).max()
        else:
            longest_duration = (df['Moving Time'] / 60).max()
    else:
        longest_duration = df["Duration (min)"].max()
    
    return {
        'longest_distance': df["Distance (km)"].max(),
        'longest_duration': longest_duration,
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


def is_race(activity_name: str, activity_description: str = "") -> bool:
    """Determine if an activity is a race based on keywords in name/description.
    
    Args:
        activity_name: Name of the activity.
        activity_description: Optional description of the activity.
        
    Returns:
        True if the activity is likely a race, False otherwise.
        
    Examples:
        >>> is_race("Parkrun")
        True
        >>> is_race("Morning Run")
        False
        >>> is_race("Yorkshire marathon")
        True
    """
    # Handle None or non-string values
    activity_name = str(activity_name) if activity_name and not isinstance(activity_name, str) else (activity_name or "")
    activity_description = str(activity_description) if activity_description and not isinstance(activity_description, str) else (activity_description or "")
    
    # Handle NaN values
    if activity_name == "nan":
        activity_name = ""
    if activity_description == "nan":
        activity_description = ""
    
    name_lower = activity_name.lower()
    desc_lower = activity_description.lower()
    combined = (name_lower + " " + desc_lower).strip()
    
    # Anti-patterns that indicate NOT a race even if they contain race keywords
    anti_patterns = [
        "1/3 marathon",
        "almost half marathon",
        "almost marathon",
        "almost half",
        "pre race",
        "post race",
        "training",  # "duathlon training", "race training"
        "recovery",  # "recovery 10k"
        "worth missing parkrun",  # skipped parkrun for something else
        "missing parkrun",
        "skip parkrun",
        "skipped parkrun",
        "race across world",  # TV show
        "featured in race",  # TV show reference
        "route",  # "marathon route bike ride"
        "half ben nevis",  # mountain reference
        "halfway",  # not a race
        "too long 10k",  # sarcastic name
    ]
    
    # Check anti-patterns first
    for pattern in anti_patterns:
        if pattern in combined:
            return False
    
    # Strong race indicators - primarily check activity name
    # These are unambiguous race terms
    strong_keywords = [
        "parkrun",
        "park run",
        "half marathon",
        "marathon",
        "ultra marathon",
        "triathlon",
        "duathlon",
        "ironman",
        "10k race",
        "5k race",
        "championship",
        "championships",
        " xc ",  # cross country with spaces to avoid matching "exercise"
        "xc race",
        "xc run",
    ]
    
    for keyword in strong_keywords:
        if keyword in name_lower:
            return True
    
    # Special handling for "XC" (cross country) - match if it's a word boundary
    import re
    if re.search(r'\bxc\b', name_lower):
        return True
    
    # Medium strength - check name first, then description
    # Format: "City Name Half" or "City Name 10k"
    medium_keywords = [
        "10k",
        "5k",
        "10km",
        "5km",
        "10,000",
        "5,000",
    ]
    
    for keyword in medium_keywords:
        # Check if keyword is in name as a standalone distance reference
        if keyword in name_lower:
            # Make sure it's not part of a longer phrase that's not a race
            if "route" not in name_lower and "training" not in name_lower:
                return True
    
    # Weak indicator - "race" keyword needs more context
    # Only matches if "race" is in the name AND seems to be referring to an event
    if "race" in name_lower:
        # Exclude if it's part of other phrases
        if "race across" not in name_lower and "route" not in name_lower:
            return True
    
    # Special case: "Half" in activity name (e.g., "Chippenham Half")
    # Only match if it's likely referring to a half marathon
    if " half" in name_lower or name_lower.endswith("half"):
        # Make sure it's not a false positive
        if "ben nevis" not in name_lower and "way" not in name_lower:
            return True
    
    # "relay" is a strong indicator if in name
    if "relay" in name_lower:
        return True
    
    return False


def format_race_time(seconds: float) -> str:
    """Format time in seconds to HH:MM:SS or MM:SS format.
    
    Args:
        seconds: Time in seconds.
        
    Returns:
        Formatted time string as HH:MM:SS (if >= 1 hour) or MM:SS.
        
    Examples:
        >>> format_race_time(3661)
        '1:01:01'
        >>> format_race_time(125)
        '2:05'
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def get_best_race_times(df: pd.DataFrame) -> Dict[str, any]:
    """Get best race times for standard distances (5k, 10k, half marathon, marathon).
    
    Args:
        df: DataFrame containing activity data.
        
    Returns:
        Dictionary with keys '5k', '10k', 'half', 'marathon' containing best times
        and dates, or None if no races found for that distance.
    """
    # Filter to running activities only
    running_df = df[df['Activity Group'] == 'Running'].copy()
    
    if len(running_df) == 0:
        return {'5k': None, '10k': None, 'half': None, 'marathon': None}
    
    results = {}
    
    # Define distance ranges (in km) for each race type
    # Allow small tolerance for GPS inaccuracy
    distance_ranges = {
        '5k': (4.8, 5.2),      # 5km parkrun
        '10k': (9.8, 10.5),    # 10km
        'half': (20.5, 21.5),  # Half marathon (21.1km)
        'marathon': (41.5, 43.0)  # Marathon (42.2km)
    }
    
    for race_type, (min_dist, max_dist) in distance_ranges.items():
        # Filter to activities in this distance range
        candidates = running_df[
            (running_df['Distance (km)'] >= min_dist) & 
            (running_df['Distance (km)'] <= max_dist)
        ].copy()
        
        if len(candidates) > 0:
            # Get the fastest (minimum time)
            # Use Elapsed Time if available, otherwise use Time
            time_col = 'Elapsed Time' if 'Elapsed Time' in candidates.columns else 'Time'
            if time_col in candidates.columns:
                fastest_idx = candidates[time_col].idxmin()
                fastest = candidates.loc[fastest_idx]
                
                results[race_type] = {
                    'time': fastest[time_col],
                    'time_formatted': format_race_time(fastest[time_col]),
                    'distance': fastest['Distance (km)'],
                    'date': fastest['Activity Date'],
                    'name': fastest.get('Activity Name', 'Unknown')
                }
            else:
                results[race_type] = None
        else:
            results[race_type] = None
    
    return results


def get_races(df: pd.DataFrame) -> pd.DataFrame:
    """Filter activities to return only races, sorted by date (most recent first).
    
    Args:
        df: DataFrame containing activity data.
        
    Returns:
        DataFrame containing only race activities with columns:
        Race Name, Date, Distance (km), Time, Activity Type.
        
    Examples:
        >>> races = get_races(df)
        >>> print(races.columns)
        Index(['Race Name', 'Date', 'Distance (km)', 'Time', 'Activity Type'], dtype='object')
    """
    # Filter to races only
    df_copy = df.copy()
    
    # Handle missing descriptions
    if 'Activity Description' not in df_copy.columns:
        df_copy['Activity Description'] = ""
    df_copy['Activity Description'] = df_copy['Activity Description'].fillna("")
    
    # Apply race detection
    df_copy['Is Race'] = df_copy.apply(
        lambda row: is_race(row.get('Activity Name', ''), row.get('Activity Description', '')),
        axis=1
    )
    
    races_df = df_copy[df_copy['Is Race']].copy()
    
    if len(races_df) == 0:
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=['Race Name', 'Date', 'Distance (km)', 'Time', 'Activity Type'])
    
    # Format the time from seconds
    if 'Elapsed Time' in races_df.columns:
        races_df['Time'] = races_df['Elapsed Time'].apply(format_race_time)
    elif 'Time' in races_df.columns:
        races_df['Time'] = races_df['Time'].apply(format_race_time)
    else:
        races_df['Time'] = "N/A"
    
    # Create display DataFrame
    result = pd.DataFrame({
        'Race Name': races_df['Activity Name'],
        'Date': races_df['Activity Date'],
        'Distance (km)': races_df['Distance (km)'],
        'Time': races_df['Time'],
        'Activity Type': races_df['Activity Type']
    })
    
    # Sort by date, most recent first
    result = result.sort_values('Date', ascending=False)
    
    return result
