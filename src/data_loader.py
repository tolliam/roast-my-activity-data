import pandas as pd
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def load_strava_data(file_path: Path) -> pd.DataFrame:
    """
    Load Strava activity data from CSV file.
    
    Args:
        file_path: Path to the CSV file containing Strava activity data
        
    Returns:
        DataFrame with cleaned and processed activity data
    """
    logger.info(f"Loading Strava data from {file_path}")
    
    # Read CSV file
    df = pd.read_csv(file_path)
    
    # Log basic info about loaded data
    logger.info(f"Loaded {len(df)} activities")
    logger.info(f"Columns: {df.columns.tolist()}")
    
    return df


def clean_strava_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare Strava data for analysis.
    
    Args:
        df: Raw DataFrame from CSV
        
    Returns:
        Cleaned DataFrame with proper types and derived fields
    """
    logger.info("Cleaning Strava data")
    
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # Convert Activity Date to datetime
    if "Activity Date" in df.columns:
        df["Activity Date"] = pd.to_datetime(df["Activity Date"])
    
    # Convert numeric columns
    numeric_cols = ["Distance", "Moving Time", "Elapsed Time", "Elevation Gain"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Add derived fields
    if "Moving Time" in df.columns and "Distance" in df.columns:
        # Calculate pace (min/km) - Moving Time is in seconds, Distance is in meters
        df["Pace"] = np.where(
            df["Distance"] > 0,
            (df["Moving Time"] / 60) / (df["Distance"] / 1000),
            np.nan
        )
    
    # Mark competition/race activities
    # Strava exports have a "Commute" field, we can use similar logic for races
    if "Commute" in df.columns:
        df["Competition"] = df["Commute"].fillna(False).astype(bool)
    else:
        df["Competition"] = False
    
    # Also detect races from activity name/description if available
    if "Activity Name" in df.columns:
        # Common race keywords (case-insensitive)
        race_keywords = [
            r'\brace\b', r'\bmarathon\b', r'\bhalf marathon\b', r'\bparkrun\b',
            r'\b5k\b', r'\b10k\b', r'\bhalf\b', r'\bfull\b',
            r'\bultra\b', r'\btriathlon\b', r'\bduathlon\b',
            r'\bironman\b', r'\bchampionship\b', r'\bcompetition\b',
            r'\btimed\b', r'\bevent\b', r'\bcup\b', r'\btrophy\b',
            r'\bopen\b.*\brace\b', r'\bfun run\b', r'\bcharity run\b'
        ]
        
        # Create a regex pattern from keywords
        import re
        pattern = '|'.join(race_keywords)
        
        # Mark as race if name matches any keyword
        name_is_race = df["Activity Name"].fillna("").str.contains(pattern, case=False, regex=True, na=False)
        df["Competition"] = df["Competition"] | name_is_race
    
    # Also check Activity Description if available
    if "Activity Description" in df.columns:
        desc_is_race = df["Activity Description"].fillna("").str.contains(pattern, case=False, regex=True, na=False)
        df["Competition"] = df["Competition"] | desc_is_race
    
    logger.info(f"Cleaned data: {len(df)} activities")
    
    return df


def load_and_prepare_data(file_path: Path) -> pd.DataFrame:
    """
    Complete pipeline to load and prepare Strava data.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Cleaned and prepared DataFrame
    """
    df = load_strava_data(file_path)
    df = clean_strava_data(df)
    return df
