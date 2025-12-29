# 🔥 Roast My Activity Data

A friendly, accessible activity analytics dashboard built with Streamlit. Transform your activity data into beautiful, interactive visualizations and gain insights into your athletic performance.

**✨ This app was 100% vibe coded ✨**

![Python](https://img.shields.io/badge/python-3.13%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-red)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

### Easy to access and customise
- **No Setup Required**: Works for anyone without installing Python locally via [Streamlit Cloud](https://roast-my-activity-data.streamlit.app/)
- **Upload Your Own Data**: Upload any Strava activities CSV file directly in the app (uploads are ephemeral ie not kept by the app creator or Streamlit Cloud)

### 📊 Recent Activity Analysis
- **Customizable Time Ranges**: Filter activities from 1-365 days
- **Activity Profiles**: Choose presets like Runner, Cyclist, Triathlete, Team Player, and more
- **Interactive Charts**: Distance timelines, activity distribution pie charts, duration histograms
- **Time of Day Analysis**: See when you're most active with hourly breakdowns and heatmaps
- **Detailed Activity Table**: Sortable table with all recent activities including pace/speed

### 🏆 All-Time Analytics
- **Cumulative Statistics**: Total distance, duration, elevation, and activity counts
- **Fun Comparative Metrics**: 
  - How many times around Earth have you traveled? 🌍
  - How many times up Mt. Everest have you climbed? 🏔️
  - Activities per week average
- **Trend Analysis**: 
  - Monthly, quarterly, or annual distance and activity trends
  - Activity type composition over time with stacked charts
  - Flexible time interval selection
- **Personal Records**: Track your longest, fastest, and highest-elevation activities
- **Day & Month Patterns**: Analyze which days of the week and months of the year you're most active
- **Race Detection**: Automatically identifies and highlights race activitiesghout the year
- **Quarterly Breakdown**: Detailed statistics by quarter

### 🎨 Clean Design
- Responsive layout with customizable sidebar
- Dark mode support for charts
- Clean, modern UI with gradient styling
- Organized data tables and metric cards
- UK Government Analysis Function accessible color palette

### 🎉 Just for Fun
- **Exercise-oholic Meter**: See how obsessed you are with exercise based on frequency, volume, and consistency
- **Cheeky Metrics**: Fun alternative ways to view your stats

## 📋 Requirements

- Python 3.13 or higher
- Strava data export (CSV format)

## 🚀 Quick Start

### Option 1: Use the Deployed App (No Installation!)

The easiest way to use this app is via Streamlit Cloud:
1. Visit the [deployed app](https://roast-my-activity-data.streamlit.app/)
2. Click "Upload CSV" in the sidebar
3. Upload your Strava activities.csv file
4. Start analyzing!

👉 **See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions**

### Option 2: Run Locally

#### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/roast-my-activity-data.git
   cd roast-my-activity-data
   ```

2. **Create a conda environment** (recommended)
   ```bash
   conda create -n roast-my-activity python=3.13 -y
   conda activate roast-my-activity
   ```
   
   Or use a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Getting Your Activity Data from Strava

1. Log in to [Strava.com](https://www.strava.com/)
2. Click on your profile picture in the top right corner → **Settings**
3. In the left sidebar, click **My Account**
4. Scroll down to the **"Download or Delete Your Account"** section
5. Under "Request Your Archive", click **Get Started**
6. Click **Request Your Archive** to confirm
7. Wait for an email from Strava with your data export (typically arrives within a few hours, but can take up to 7 days)
8. Once received, open the email and click the download link
9. Extract the downloaded ZIP file
10. Locate the `activities.csv` file inside the extracted folder
11. Place `activities.csv` in the `data/` folder of this project

## 📁 Project Structure

```
roast-my-activity-data/
├── app.py                      # Main Streamlit application
├── src/
│   ├── __init__.py            # Package initialization
│   ├── config.py              # Configuration and constants
│   ├── data_loader.py         # Data loading and preprocessing
│   ├── utils.py               # Utility functions and calculations
│   ├── visualizations.py      # Plotly chart creation (legacy)
│   └── visualizations_altair.py # Altair chart creation (current)
├── data/
│   └── activities.csv         # Your Strava data (not included)
├── docs/
│   ├── ARCHITECTURE.md        # System architecture documentation
│   └── USAGE.md               # Detailed usage guide
├── tests/
│   ├── test_data_loader.py    # Data loading tests
│   ├── test_config.py         # Configuration tests
│   ├── test_races.py          # Race detection tests
│   ├── test_team_sports_config.py # Team sports tests
│   ├── test_unmapped_activities.py # Unmapped activity tests
│   └── test_utils.py          # Utility function tests
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup configuration
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
├── README.md                  # This file
├── CONTRIBUTING.md            # Contribution guidelines
└── DEPLOYMENT.md              # Deployment instructions
```

## 🎯 Usage

### Basic Usage

1. **Select Time Range**: Use the sidebar slider to choose how many days of recent activity to display
2. **Filter Activities**: Select which activity types to include in your analysis
3. **Choose Activity Profile**: Pick from Runner, Cyclist, Triathlete, Team Player, Racketeer, and more
4. **Explore Tabs**: 
   - **Recent Activity**: View your latest activities with interactive charts
   - **All-Time Analysis**: Dive deep into your complete activity history
   - **Just for Fun**: See quirky metrics and comparisons
   - **Help**: View documentation and profile descriptions

### Advanced Features

- **Quarterly Analysis**: Track your progress quarter by quarter
- **Personal Records**: Automatically identifies your best performances
- **Trend Visualization**: Spot patterns with rolling averages and cumulative charts
- **Calendar Heatmap**: See at a glance which days you're most active
- **Race Detection**: Automatically identifies race activities throughout the year

For detailed usage instructions, see [USAGE.md](docs/USAGE.md)

## 🛠️ Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

### Code Organization

- **src/config.py**: All configuration constants, color schemes, and CSS styling
- **src/data_loader.py**: Data loading, cleaning, and transformation functions
- **src/utils.py**: Helper functions for statistics and calculations
- **src/visualizations_altair.py**: All Altair chart creation functions (current)
- **src/visualizations.py**: Plotly chart creation functions (legacy)
- **app.py**: Main Streamlit app with UI layout and orchestration

For detailed architecture information, see [ARCHITECTURE.md](docs/ARCHITECTURE.md)

### Adding New Features

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## 📊 Data Format


The app expects an activities CSV export with these key columns:
- `Activity Date`: Date and time of activity
- `Activity Type`: Type of activity (Run, Ride, etc.)
- `Distance`: Distance in kilometers
- `Moving Time`: Duration in seconds (time actually moving, excluding stops)
- `Elevation Gain`: Elevation in meters
- `Average Speed`: Speed in km/h

## 🎨 Customization

### Changing Colors

Edit the `ACTIVITY_COLORS` dictionary in `src/config.py`:

```python
ACTIVITY_COLORS = {
    "Running": "#12436D",    # Your custom color
    "Cycling": "#28A197",
    # ... etc
}
```

### Adjusting Metrics

Modify constants in `src/config.py`:

```python
DEFAULT_DAYS_BACK = 30  # Change default time range
MAX_DAYS_BACK = 365     # Extend maximum range
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Visualizations powered by [Altair](https://altair-viz.github.io)
- Activity data from [Strava](https://www.strava.com)
- UK Government Analysis Function accessible color palette

## 🚦 Project Status

Active development - Version 0.10.1

## 📈 Future Enhancements

- [ ] Direct API integration with fitness platforms
- [x] Pace analysis and speed timelines
- [ ] Heart rate zone analysis
- [ ] Training load calculations
- [ ] Goal tracking and progress
- [ ] Export reports as PDF
- [ ] Comparative athlete analytics
- [ ] Machine learning predictions
- [x] Time of day analysis
- [x] Day of week and month patterns
- [x] Race detection

---

**Made with ❤️ for athletes who love their data**
