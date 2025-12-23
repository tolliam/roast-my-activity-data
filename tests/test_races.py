"""Unit tests for race detection and formatting functions."""

import pytest
import pandas as pd
from datetime import datetime
from src.utils import is_race, format_race_time, get_races


class TestIsRace:
    """Tests for race detection function."""
    
    def test_parkrun_variations(self):
        """Test parkrun detection with different variations."""
        assert is_race("Swindon parkrun") is True
        assert is_race("York parkrun") is True
        assert is_race("Parkrun") is True
        assert is_race("PARKRUN") is True  # Case insensitive
        assert is_race("park run") is True
        assert is_race("Park Run") is True
    
    def test_marathon_variations(self):
        """Test marathon detection including half and ultra."""
        assert is_race("Yorkshire marathon") is True
        assert is_race("Devizes Half Marathon") is True
        assert is_race("half marathon") is True
        assert is_race("ultra marathon") is True
        assert is_race("MARATHON") is True  # Case insensitive
    
    def test_specific_race_names(self):
        """Test detection of specific race names from the data."""
        assert is_race("Chippenham Half") is True
        assert is_race("Bath half") is True
        assert is_race("Weymouth Ironman 70.3") is True
        assert is_race("London 10,000") is True
        assert is_race("Aboyne Highland Games 11km Hill race") is True
        assert is_race("River Thames Half marathon") is True
    
    def test_race_keyword_variations(self):
        """Test various race-related keywords."""
        assert is_race("10k race") is True
        assert is_race("5K Race") is True
        assert is_race("10km race") is True
        assert is_race("5km trail race") is True
        assert is_race("triathlon") is True
        assert is_race("Duathlon Championship") is True
        assert is_race("relay race") is True
        assert is_race("competition") is True
        assert is_race("championships") is True
    
    def test_non_races(self):
        """Test that regular activities are not detected as races."""
        assert is_race("Morning Run") is False
        assert is_race("Evening Ride") is False
        assert is_race("Recovery run") is False
        assert is_race("Lunch Run") is False
        assert is_race("Afternoon Run") is False
        assert is_race("Easy pace") is False
        assert is_race("Training run") is False
        assert is_race("Tempo run") is False
    
    def test_anti_patterns(self):
        """Test that anti-patterns are correctly excluded."""
        assert is_race("1/3 marathon") is False  # Training run
        assert is_race("Almost half marathon") is False  # Training run
        assert is_race("Accidental almost half marathon") is False
        assert is_race("Almost marathon") is False
        assert is_race("pre race warm up") is False
        assert is_race("post race cool down") is False
    
    def test_case_insensitivity(self):
        """Test that race detection is case insensitive."""
        assert is_race("parkrun") is True
        assert is_race("Parkrun") is True
        assert is_race("PARKRUN") is True
        assert is_race("PaRkRuN") is True
        assert is_race("YORKSHIRE MARATHON") is True
        assert is_race("yorkshire marathon") is True
    
    def test_with_description(self):
        """Test race detection using both name and description."""
        assert is_race("Sunday Run", "It was a race!") is True
        assert is_race("Training", "parkrun this morning") is True
        assert is_race("Activity", "10k competition") is True
        # But anti-patterns should still apply
        assert is_race("Long run", "almost marathon distance") is False
    
    def test_edge_cases(self):
        """Test edge cases like empty strings."""
        assert is_race("") is False
        assert is_race("", "") is False
        assert is_race("   ") is False


class TestFormatRaceTime:
    """Tests for race time formatting function."""
    
    def test_hours_minutes_seconds(self):
        """Test formatting with hours, minutes, and seconds."""
        assert format_race_time(3661) == "1:01:01"
        assert format_race_time(7200) == "2:00:00"
        assert format_race_time(5177) == "1:26:17"
        assert format_race_time(12969) == "3:36:09"
    
    def test_minutes_seconds_only(self):
        """Test formatting with only minutes and seconds (< 1 hour)."""
        assert format_race_time(125) == "2:05"
        assert format_race_time(1159) == "19:19"
        assert format_race_time(1093) == "18:13"
        assert format_race_time(59) == "0:59"
        assert format_race_time(60) == "1:00"
    
    def test_zero_and_small_values(self):
        """Test formatting with small time values."""
        assert format_race_time(0) == "0:00"
        assert format_race_time(1) == "0:01"
        assert format_race_time(10) == "0:10"
    
    def test_exact_hour_boundaries(self):
        """Test formatting at exact hour boundaries."""
        assert format_race_time(3600) == "1:00:00"
        assert format_race_time(7200) == "2:00:00"
        assert format_race_time(3599) == "59:59"  # Just under 1 hour


class TestGetRaces:
    """Tests for get_races function."""
    
    def test_filters_races_correctly(self):
        """Test that get_races returns only race activities."""
        test_data = {
            'Activity Name': [
                'York parkrun',
                'Morning Run',
                'Chippenham Half',
                'Evening Ride',
                'Yorkshire marathon'
            ],
            'Activity Date': [
                datetime(2024, 1, 1),
                datetime(2024, 1, 2),
                datetime(2024, 1, 3),
                datetime(2024, 1, 4),
                datetime(2024, 1, 5)
            ],
            'Activity Type': ['Run', 'Run', 'Run', 'Ride', 'Run'],
            'Activity Description': ['', '', '', '', ''],
            'Distance (km)': [5.0, 10.0, 21.1, 30.0, 42.2],
            'Elapsed Time': [1200, 3600, 5400, 7200, 12000],
            'Duration (min)': [20, 60, 90, 120, 200],
            'Elevation (m)': [10, 50, 100, 200, 150],
            'Average Speed (km/h)': [15, 10, 14, 15, 12]
        }
        df = pd.DataFrame(test_data)
        
        races = get_races(df)
        
        # Should only return the 3 races
        assert len(races) == 3
        assert 'York parkrun' in races['Race Name'].values
        assert 'Chippenham Half' in races['Race Name'].values
        assert 'Yorkshire marathon' in races['Race Name'].values
        assert 'Morning Run' not in races['Race Name'].values
        assert 'Evening Ride' not in races['Race Name'].values
    
    def test_races_sorted_by_date_descending(self):
        """Test that races are sorted by date, most recent first."""
        test_data = {
            'Activity Name': [
                'Race 1',
                'Race 2',
                'Race 3'
            ],
            'Activity Date': [
                datetime(2024, 1, 1),
                datetime(2024, 1, 15),
                datetime(2024, 1, 10)
            ],
            'Activity Type': ['Run', 'Run', 'Run'],
            'Activity Description': ['', '', ''],
            'Distance (km)': [5.0, 10.0, 15.0],
            'Elapsed Time': [1200, 2400, 3600],
            'Duration (min)': [20, 40, 60],
            'Elevation (m)': [10, 20, 30],
            'Average Speed (km/h)': [15, 15, 15]
        }
        df = pd.DataFrame(test_data)
        
        races = get_races(df)
        
        # Verify dates are in descending order
        dates = races['Date'].tolist()
        assert dates[0] == datetime(2024, 1, 15)  # Most recent
        assert dates[1] == datetime(2024, 1, 10)
        assert dates[2] == datetime(2024, 1, 1)  # Oldest
    
    def test_time_formatted_correctly(self):
        """Test that race times are formatted as strings."""
        test_data = {
            'Activity Name': ['Parkrun', 'Half Marathon'],
            'Activity Date': [datetime(2024, 1, 1), datetime(2024, 1, 2)],
            'Activity Type': ['Run', 'Run'],
            'Activity Description': ['', ''],
            'Distance (km)': [5.0, 21.1],
            'Elapsed Time': [1200, 5400],  # 20:00 and 1:30:00
            'Duration (min)': [20, 90],
            'Elevation (m)': [10, 100],
            'Average Speed (km/h)': [15, 14]
        }
        df = pd.DataFrame(test_data)
        
        races = get_races(df)
        
        # Check time formatting
        assert races.iloc[1]['Time'] == '20:00'  # Most recent (parkrun)
        assert races.iloc[0]['Time'] == '1:30:00'  # Older (half marathon)
    
    def test_correct_columns_returned(self):
        """Test that get_races returns the correct columns."""
        test_data = {
            'Activity Name': ['Parkrun'],
            'Activity Date': [datetime(2024, 1, 1)],
            'Activity Type': ['Run'],
            'Activity Description': [''],
            'Distance (km)': [5.0],
            'Elapsed Time': [1200],
            'Duration (min)': [20],
            'Elevation (m)': [10],
            'Average Speed (km/h)': [15]
        }
        df = pd.DataFrame(test_data)
        
        races = get_races(df)
        
        expected_columns = ['Race Name', 'Date', 'Distance (km)', 'Time', 'Activity Type']
        assert list(races.columns) == expected_columns
    
    def test_empty_dataframe_when_no_races(self):
        """Test that an empty DataFrame with correct columns is returned when no races."""
        test_data = {
            'Activity Name': ['Morning Run', 'Evening Ride'],
            'Activity Date': [datetime(2024, 1, 1), datetime(2024, 1, 2)],
            'Activity Type': ['Run', 'Ride'],
            'Activity Description': ['', ''],
            'Distance (km)': [10.0, 30.0],
            'Elapsed Time': [3600, 7200],
            'Duration (min)': [60, 120],
            'Elevation (m)': [50, 200],
            'Average Speed (km/h)': [10, 15]
        }
        df = pd.DataFrame(test_data)
        
        races = get_races(df)
        
        assert len(races) == 0
        expected_columns = ['Race Name', 'Date', 'Distance (km)', 'Time', 'Activity Type']
        assert list(races.columns) == expected_columns
    
    def test_missing_description_handled(self):
        """Test that missing Activity Description column is handled gracefully."""
        test_data = {
            'Activity Name': ['York parkrun', 'Morning Run'],
            'Activity Date': [datetime(2024, 1, 1), datetime(2024, 1, 2)],
            'Activity Type': ['Run', 'Run'],
            'Distance (km)': [5.0, 10.0],
            'Elapsed Time': [1200, 3600],
            'Duration (min)': [20, 60],
            'Elevation (m)': [10, 50],
            'Average Speed (km/h)': [15, 10]
        }
        df = pd.DataFrame(test_data)
        
        # Should not raise an error
        races = get_races(df)
        
        assert len(races) == 1
        assert 'York parkrun' in races['Race Name'].values
    
    def test_real_data_examples(self):
        """Test with examples from actual activities.csv."""
        test_data = {
            'Activity Name': [
                'Devizes Half Marathon',
                'Swindon parkrun',
                'Yorkshire marathon',
                'Chippenham Half',
                'Weymouth Ironman 70.3',
                'Bath half',
                'Morning Run',
                '1/3 marathon',
                'Almost half marathon'
            ],
            'Activity Date': [
                datetime(2012, 10, 21),
                datetime(2013, 4, 6),
                datetime(2013, 10, 20),
                datetime(2013, 9, 15),
                datetime(2017, 9, 17),
                datetime(2017, 3, 12),
                datetime(2024, 1, 1),
                datetime(2024, 1, 2),
                datetime(2024, 1, 3)
            ],
            'Activity Type': ['Run', 'Run', 'Run', 'Run', 'Swim', 'Run', 'Run', 'Run', 'Run'],
            'Activity Description': [''] * 9,
            'Distance (km)': [21.1, 5.0, 42.2, 21.3, 2.2, 21.4, 10.0, 14.5, 20.0],
            'Elapsed Time': [5177, 1159, 12969, 5145, 2663, 5601, 3600, 3702, 4415],
            'Duration (min)': [86, 19, 216, 86, 44, 93, 60, 62, 74],
            'Elevation (m)': [93, 0, 100, 66, 0, 128, 50, 13, 35],
            'Average Speed (km/h)': [14, 15, 12, 15, 3, 14, 10, 14, 16]
        }
        df = pd.DataFrame(test_data)
        
        races = get_races(df)
        
        # Should return 6 races, not the training runs
        assert len(races) == 6
        race_names = races['Race Name'].values
        assert 'Devizes Half Marathon' in race_names
        assert 'Swindon parkrun' in race_names
        assert 'Yorkshire marathon' in race_names
        assert 'Chippenham Half' in race_names
        assert 'Weymouth Ironman 70.3' in race_names
        assert 'Bath half' in race_names
        # These should NOT be in the races
        assert 'Morning Run' not in race_names
        assert '1/3 marathon' not in race_names
        assert 'Almost half marathon' not in race_names
