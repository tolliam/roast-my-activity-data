# Usage Guide - Roast My Activity Data

Complete guide to using the Roast My Activity Data analytics dashboard.

## Table of Contents

- [Getting Started](#getting-started)
- [Interface Overview](#interface-overview)
- [Features Deep Dive](#features-deep-dive)
- [Tips & Tricks](#tips--tricks)
- [Troubleshooting](#troubleshooting)

## Getting Started

### First Time Setup

1. **Export your activity data**
   - Log into your fitness platform (e.g., Strava.com)
   - Go to Settings → My Account
   - Scroll to "Download or Delete Your Account"
   - Click "Get Started" under "Download Request"
   - Wait for email (can take a few hours)
   - Download and extract the ZIP file

2. **Prepare your data**
   - Find `activities.csv` in the extracted files
   - Copy it to the `data/` folder in this project
   - Make sure it's named exactly `activities.csv`

3. **Launch the app**
   ```bash
   streamlit run app.py
   ```

## Interface Overview

### Understanding Activity Types

The app categorizes your Strava activities into broader groups for easier analysis:

- **Running**: Run, Virtual Run
- **Cycling**: Ride
- **Swimming**: Swim, Open Water Swim
- **Walking**: Walk, Hike
- **Strength**: Weight Training, Workout, Rowing
- **Winter Sports**: Alpine Ski, Backcountry Ski, Nordic Ski, Snowboard
- **Team Sports**: Rugby, Football, Netball, Basketball, Soccer
- **Other**: Water Sport, Unknown, and any other activity types

These groupings allow you to filter and analyze your activities by broader categories rather than individual activity types. You can find the complete mapping in the **Help tab** within the app.

### Sidebar Controls

**Show activities from last N days**
- Slider control: 1-90 days
- Default: 30 days
- Affects the "Recent Activity" tab only

**Filter by Activity Type**
- Multi-select dropdown
- Options: Running, Cycling, Swimming, Walking, Strength, Other
- Default: All types selected
- Affects both Recent and All-Time tabs

### Main Tabs

**📊 Recent Activity**
- Focuses on your selected time period
- Quick overview of recent performance
- Perfect for tracking current training

**🏆 All-Time Analysis**
- Complete activity history
- Long-term trends and patterns
- Personal records and achievements

**🎉 Just for Fun**
- Fun metrics and comparisons
- Exercise obsession meter
- Creative ways to visualize your data

**❓ Help**
- Activity type mapping reference
- Quick tips and getting started guide
- Links to documentation and support

## Features Deep Dive

### Recent Activity Tab

#### Summary Metrics
Four key metrics at the top:
- **Total Activities**: Count of activities in period
- **Total Distance**: Sum of all distances (km)
- **Total Duration**: Combined activity time (hours)
- **Total Elevation**: Total elevation gain (meters)

#### Distance Timeline Chart
- Line graph showing distance per activity
- Hover over points to see exact values
- Helps identify activity frequency patterns
- Spot increases or decreases in training load

#### Activity Type Pie Chart
- Visual breakdown of activity types
- Color-coded by activity category
- Percentages show distribution
- Click legend items to show/hide categories

#### Duration Distribution Histogram
- Shows how your activity durations are distributed
- Find your typical workout length
- Identify if you're doing mostly short or long sessions
- Helps plan balanced training

#### Recent Activities Table
- Sortable table of all recent activities
- Click column headers to sort
- Columns: Date, Type, Distance, Duration, Elevation, Speed
- Useful for detailed review

### All-Time Analysis Tab

#### Summary Statistics
Same four metrics as Recent tab, but for all activities:
- Total Activities
- Total Distance (km)
- Total Duration (hours)
- Total Elevation (m)

#### Fun Comparative Metrics
Puts your achievements in perspective:

**📅 Activities/Week**
- Average activities per week over your history
- Based on total activities / 52 weeks

**🌍 Around Earth**
- How many times you've traveled Earth's circumference (40,075 km)
- Shows as percentage if less than 1x
- Shows as multiple if you've gone around 1+ times

**⏱️ Time Active**
- Total time spent being active
- Shown in days if less than a year
- Shown in years if more than 365 days

**🏔️ Up Mt Everest**
- How many times you've climbed Everest's height (8,849m)
- Shows as percentage if less than 1x
- Shows as multiple if 1+ times

#### Cumulative Distance Chart
- Running total of distance over time
- Shows your total mileage growth
- Steeper slopes = more active periods
- Flat sections = breaks or reduced activity

#### Quarterly Activity Trends
- Two metrics plotted together:
  - Distance per quarter
  - Activity count per quarter
- Compare volume vs frequency
- Identify seasonal patterns

#### Activity Type Composition Over Time
- Stacked bar chart by quarter
- See how your activity mix changes
- Identify phases (cycling season, running focus, etc.)
- Color-coded by activity type

#### Rolling Average Distance
- Smoothed trend line (2-quarter rolling average)
- Removes noise to show true trends
- Great for long-term progress tracking

#### Year-over-Year Comparison
- Compare same months across different years
- Each line = one year
- See if you're improving year over year
- Identify consistent patterns

#### Personal Records 🏆

Four key PRs automatically identified:
- **Longest Distance**: Your single longest activity
- **Longest Duration**: Your longest single session
- **Most Elevation**: Biggest elevation gain in one activity
- **Fastest Speed**: Highest average speed achieved

#### Quarterly Summary

**Quarterly Distance Bar Chart**
- Total distance by quarter
- Easy comparison across quarters
- Identify your most active periods

**Quarterly Statistics Table**
- Detailed breakdown by quarter
- Columns: Quarter, Activity Count, Distance, Duration, Elevation
- Sortable for analysis

#### Activity Calendar Heatmap 📅
- Visual calendar for current year
- Week of year (x-axis) vs day of week (y-axis)
- Color intensity = number of activities
- Darker green = more activities that day
- Spot weekly patterns and rest days

## Tips & Tricks

### Getting the Most from Your Data

1. **Compare time periods**
   - Use the sidebar slider to compare different date ranges
   - Switch back and forth to see changes

2. **Focus on specific activities**
   - Unselect activity types you're not interested in
   - Great for runners to exclude cycling, etc.

3. **Identify training patterns**
   - Look at the calendar heatmap to see which days you typically train
   - Use duration histogram to find your preferred workout length

4. **Track progress**
   - Check year-over-year chart to see improvements
   - Compare quarterly totals to previous periods

5. **Set goals**
   - Use the "Around Earth" metric as motivation
   - Track progress toward climbing "Everest"

### Performance Tips

- **First load may be slow** for large datasets (5000+ activities)
- Subsequent loads are faster thanks to caching
- Changing filters is instant
- Use smaller date ranges for faster visualization updates

### Understanding the Charts

**When to use Recent vs All-Time:**
- **Recent**: Current training focus, week-to-week changes
- **All-Time**: Big picture, long-term progress, lifetime achievements

**Color meanings:**
- Running: Dark blue (#12436D)
- Cycling: Turquoise (#28A197)
- Swimming: Dark pink (#801650)
- Walking: Orange (#F46A25)
- Strength: Light purple (#A285D1)
- Other: Dark grey (#3D3D3D)

## Troubleshooting

### Common Issues

**"Data file not found" error**
- Ensure `activities.csv` is in the `data/` folder
- Check the filename is exactly `activities.csv`
- Verify the file isn't corrupted

**Charts not displaying**
- Check that you have activities in the selected date range
- Try selecting "All activity types" if some are unselected
- Increase the days back slider

**Slow performance**
- First load of large datasets takes time (normal)
- Close other browser tabs
- Try filtering to fewer activity types
- Restart the Streamlit app

**Missing activities**
- Verify your activity export is complete
- Check if activities have required fields (date, distance, duration)
- Activities with missing data are filtered out

**Incorrect metrics**
- Verify your activity data export is recent
- Re-download from your platform if data seems outdated
- Check that CSV columns match expected format

### Getting Help

If you encounter issues:
1. Check the error message in the browser
2. Look at the terminal/console for Python errors
3. Verify your CSV file format matches the expected export format
4. Open an issue on GitHub with details

## Advanced Usage

### Customizing the Experience

See [README.md](../README.md) for:
- Changing color schemes
- Adjusting default settings
- Modifying metrics calculations

### Data Privacy

- All data stays on your local machine
- No data is uploaded or shared
- Your activities remain private
- Delete `activities.csv` anytime to remove data

### Updating Your Data

To refresh with new activities:
1. Request new activity export
2. Replace `data/activities.csv` with new file
3. Refresh the browser (Ctrl+R or Cmd+R)
4. App will automatically reload with new data

---

**Enjoy analyzing your athletic journey! 🏃‍♂️🚴‍♀️🏊‍♂️**
