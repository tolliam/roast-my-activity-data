# 🔥 Roast My Activity Data

A comprehensive, professional-grade activity analytics dashboard built with Streamlit. Transform your activity data into beautiful, interactive visualizations and gain deep insights into your athletic performance.

**✨ This app was 100% vibe coded ✨**

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-red)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

### Easy to access and customise
- **No Setup Required**: Works for anyone without installing Python locally via [Streamlit Cloud](https://roast-my-activity-data.streamlit.app/)
- **Upload Your Own Data**: Upload any Strava activities CSV file directly in the app (uploads are ephemeral ie not kept by the app creator or Streamlit Cloud)

### 📊 Recent Activity Analysis
- **Customizable Time Ranges**: Filter activities from 1-90 days
- **Activity Type Filtering**: Focus on specific activity types (Running, Cycling, Swimming, etc.)
- **Interactive Charts**: Distance timelines, activity distribution pie charts, duration histograms
- **Detailed Activity Table**: Sortable table with all recent activities

### 🏆 All-Time Analytics
- **Cumulative Statistics**: Total distance, duration, elevation, and activity counts
- **Fun Comparative Metrics**: 
  - How many times around Earth have you traveled? 🌍
  - How many times up Mt. Everest have you climbed? 🏔️
  - Total time active in days or years ⏱️
- **Trend Analysis**: 
  - Quarterly distance and activity trends
  - Rolling averages for smooth trend visualization
  - Year-over-year comparisons
  - Activity type composition over time
- **Personal Records**: Track your longest, fastest, and highest-elevation activities
- **Calendar Heatmap**: Visualize activity patterns throughout the year
- **Quarterly Breakdown**: Detailed statistics by quarter

### 🎨 Professional Design
- Responsive layout with customizable sidebar
- Clean, modern UI with gradient styling
- Professional data tables and metric cards

## 📋 Requirements

- Python 3.8 or higher
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

2. **Create a virtual environment** (recommended)
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

### Getting Your Activity Data

1. Log in to your fitness tracking platform (e.g., [Strava.com](https://www.strava.com/))
2. Go to Settings → My Account → Download or Delete Your Account
3. Click "Get Started" under "Download Request"
4. Wait for the email with your data export
5. Extract the ZIP file and locate `activities.csv`
6. Place `activities.csv` in the `data/` folder

### Running the App

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## 📁 Project Structure

```
roast-my-strava/
├── app.py                 # Main Streamlit application
├── src/
│   ├── __init__.py       # Package initialization
│   ├── config.py         # Configuration and constants
│   ├── data_loader.py    # Data loading and preprocessing
│   ├── utils.py          # Utility functions and calculations
│   └── visualizations.py # Chart and graph creation
├── data/
│   └── activities.csv    # Your Strava data (not included)
├── docs/
│   ├── ARCHITECTURE.md   # System architecture documentation
│   └── USAGE.md          # Detailed usage guide
├── tests/
│   ├── test_config.py        # Tests for configuration module
│   ├── test_data_loader.py   # Tests for data loading functions
│   └── test_utils.py         # Tests for utility functions
├── requirements.txt      # Python dependencies
├── setup.py             # Package setup configuration
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
├── README.md            # This file
└── CONTRIBUTING.md      # Contribution guidelines
```

## 🎯 Usage

### Basic Usage

1. **Select Time Range**: Use the sidebar slider to choose how many days of recent activity to display
2. **Filter Activities**: Select which activity types to include in your analysis
3. **Explore Tabs**: 
   - **Recent Activity**: View your latest activities with interactive charts
   - **All-Time Analysis**: Dive deep into your complete activity history

### Advanced Features

- **Quarterly Analysis**: Track your progress quarter by quarter
- **Personal Records**: Automatically identifies your best performances
- **Trend Visualization**: Spot patterns with rolling averages and cumulative charts
- **Calendar Heatmap**: See at a glance which days you're most active

For detailed usage instructions, see [docs/USAGE.md](docs/USAGE.md)

## 🛠️ Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run tests with verbose output
pytest tests/ -v

# Run a specific test file
pytest tests/test_data_loader.py -v
```

### Code Organization

- **src/config.py**: All configuration constants, color schemes, and CSS styling
- **src/data_loader.py**: Data loading, cleaning, and transformation functions
- **src/utils.py**: Helper functions for statistics and calculations
- **src/visualizations.py**: All Plotly chart creation functions
- **app.py**: Main Streamlit app with UI layout and orchestration

### Adding New Features

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## 📊 Data Format

The app expects an activities CSV export with these key columns:
- `Activity Date`: Date and time of activity
- `Activity Type`: Type of activity (Run, Ride, etc.)
- `Distance`: Distance in kilometers
- `Elapsed Time`: Duration in seconds
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
MAX_DAYS_BACK = 180     # Extend maximum range
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Visualizations powered by [Plotly](https://plotly.com/)
- Data processing with [Pandas](https://pandas.pydata.org/)
- Color palette based on [UK Government Analysis Function](https://analysisfunction.civilservice.gov.uk/policy-store/codes-for-accessible-colours/)

## 📧 Support

- **Issues**: Please use the [GitHub issue tracker](https://github.com/tolliam/roast-my-activity-data/issues)
- **Questions**: Open a discussion on GitHub

## 🚦 Project Status

Active development - Version 1.0.0

## 📈 Future Enhancements

- [ ] Direct API integration with fitness platforms
- [ ] Pace analysis and splits
- [ ] Heart rate zone analysis
- [ ] Training load calculations
- [ ] Goal tracking and progress
- [ ] Export reports as PDF
- [ ] Comparative athlete analytics
- [ ] Machine learning predictions

---

**Made with ❤️ for athletes who love their data**
