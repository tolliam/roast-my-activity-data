# Architecture Documentation

Technical overview of the Roast My Strava application architecture.

## System Overview

Roast My Strava is a Streamlit-based web application that provides activity analytics for Strava data. The application follows a modular architecture with clear separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│                    (Streamlit App)                       │
│                       app.py                             │
└────────────┬────────────────────────────────────────────┘
             │
             ├─────────────┬──────────────┬────────────────┐
             │             │              │                │
             ▼             ▼              ▼                ▼
      ┌───────────┐ ┌────────────┐ ┌─────────┐    ┌──────────┐
      │  config   │ │data_loader │ │  utils  │    │   viz    │
      │  .py      │ │   .py      │ │  .py    │    │  .py     │
      └───────────┘ └────────────┘ └─────────┘    └──────────┘
             │             │              │                │
             └─────────────┴──────────────┴────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  activities.csv  │
                    │   (Data Store)   │
                    └──────────────────┘
```

## Module Breakdown

### 1. app.py - Main Application

**Purpose**: Entry point and UI orchestration

**Responsibilities**:
- Page configuration and styling setup
- Sidebar creation and user input handling
- Tab management (Recent vs All-Time)
- Coordinate data flow between modules
- Render UI components and layouts

**Key Functions**:
- `main()`: Application entry point
- `setup_page()`: Configure Streamlit settings
- `create_sidebar()`: Build sidebar controls
- `render_recent_activity_tab()`: Recent activity UI
- `render_alltime_tab()`: All-time analysis UI
- `render_summary_metrics()`: Metric cards
- `render_fun_metrics()`: Comparative metrics

**Design Pattern**: Controller pattern - coordinates between data and view

### 2. src/config.py - Configuration

**Purpose**: Centralized configuration and constants

**Contents**:
- `APP_TITLE`: Application title
- `DEFAULT_DAYS_BACK`: Default time range
- `DATA_FILE_PATH`: Path to CSV data
- `EARTH_CIRCUMFERENCE_KM`: Physical constants
- `ACTIVITY_COLORS`: Color palette dictionary
- `ACTIVITY_GROUP_MAP`: Activity type mappings
- `CUSTOM_CSS`: Complete CSS styling

**Design Pattern**: Configuration module - single source of truth

**Why Separate**:
- Easy customization without code changes
- Reusable constants across modules
- Type safety with explicit definitions
- Clear documentation of configurable values

### 3. src/data_loader.py - Data Layer

**Purpose**: Data loading, cleaning, and transformation

**Key Functions**:

`load_strava_data(file_path) -> pd.DataFrame`
- Reads CSV file
- Converts data types (dates, numeric fields)
- Creates derived columns
- Maps activity types to groups
- Filters invalid records
- Returns sorted DataFrame

`filter_by_activities(df, selected) -> pd.DataFrame`
- Filters by activity group

`filter_by_date_range(df, days_back) -> pd.DataFrame`
- Filters by time period

`get_quarterly_stats(df) -> pd.DataFrame`
- Aggregates by quarter

`get_monthly_trends(df) -> pd.DataFrame`
- Calculates trend metrics

**Caching**: Uses `@st.cache_data` decorator for performance

**Design Pattern**: Data Access Layer (DAL)

### 4. src/utils.py - Business Logic

**Purpose**: Statistics calculations and utility functions

**Key Functions**:

`calculate_fun_metrics(df) -> Dict`
- Computes comparative metrics
- Returns dictionary with 8 key metrics

`get_personal_records(df) -> Dict`
- Extracts max values for PRs
- Returns dictionary with 4 records

`calculate_summary_stats(df) -> Dict`
- Basic aggregations
- Returns summary dictionary

`format_metric_display(value, type) -> Tuple`
- Formats values for UI display
- Returns (display_value, help_text)

**Design Pattern**: Service layer - pure business logic

**Why Separate from data_loader**:
- Different responsibility (calculation vs loading)
- Testable in isolation
- Reusable across different UIs

### 5. src/visualizations.py - View Layer

**Purpose**: Chart and graph generation

**Key Functions** (all return `go.Figure`):
- `create_distance_timeline()`: Line chart
- `create_activity_type_pie()`: Pie chart
- `create_duration_histogram()`: Histogram
- `create_cumulative_distance_chart()`: Cumulative line
- `create_quarterly_trends_chart()`: Multi-line
- `create_stacked_activity_chart()`: Stacked bar
- `create_rolling_average_chart()`: Rolling average
- `create_year_over_year_chart()`: YoY comparison
- `create_quarterly_bar_chart()`: Bar chart
- `create_activity_heatmap()`: Heatmap

**Design Pattern**: View factory - creates visual components

**Consistency**:
- All functions return Plotly Figure objects
- Standard parameter patterns
- Consistent color usage from config
- Similar naming conventions

## Data Flow

### Typical Request Flow

1. **User Interaction**
   - User adjusts sidebar filters
   - Streamlit re-runs app.py

2. **Data Loading** (cached)
   - `load_strava_data()` reads CSV
   - Data cleaned and transformed
   - Result cached for performance

3. **Filtering**
   - Apply activity type filter
   - Apply date range filter
   - Create filtered DataFrames

4. **Processing**
   - Calculate statistics (`utils.py`)
   - Aggregate data (`data_loader.py`)
   - Generate trends

5. **Visualization**
   - Create charts (`visualizations.py`)
   - Format metrics (`utils.py`)
   - Render UI components

6. **Display**
   - Streamlit renders components
   - User sees updated dashboard

## Design Principles

### Separation of Concerns

Each module has a single, well-defined responsibility:
- **config**: Settings and constants
- **data_loader**: Data operations
- **utils**: Calculations
- **visualizations**: Chart creation
- **app**: UI and coordination

### DRY (Don't Repeat Yourself)

- Common calculations in `utils.py`
- Reusable chart functions in `visualizations.py`
- Shared constants in `config.py`
- Generic helper functions

### Type Safety

- Type hints on all function signatures
- Clear return types
- Typed dictionaries for configuration

### Testability

- Pure functions without side effects
- Minimal dependencies between modules
- Easy to mock for testing
- Clear input/output contracts

### Performance

- Aggressive caching of data loading
- Efficient pandas operations
- Minimal recomputation
- Streamlit's built-in optimization

## Technology Stack

### Core Framework
- **Streamlit 1.28+**: Web application framework
  - Automatic UI updates
  - Built-in caching
  - Simple Python API

### Data Processing
- **Pandas 2.0+**: DataFrames and data manipulation
  - Fast aggregations
  - Time series support
  - Data cleaning utilities

### Visualization
- **Plotly 5.17+**: Interactive charts
  - Responsive design
  - Hover tooltips
  - Export capabilities

### Additional Libraries
- **python-dateutil**: Date parsing and manipulation

## State Management

Streamlit's reactive model:
- Top-to-bottom script execution
- Widgets trigger re-runs
- `@st.cache_data` prevents redundant computation
- Session state not needed (stateless design)

## Error Handling

### Data Loading
```python
try:
    df = load_strava_data()
except FileNotFoundError:
    st.error("Data file not found")
    return
except Exception as e:
    st.error(f"Error: {e}")
    return
```

### Visualization
- Check for empty DataFrames
- Return None for optional charts
- Graceful degradation

## Extension Points

### Adding New Visualizations

1. Create function in `visualizations.py`
2. Follow naming convention: `create_*_chart()`
3. Return `go.Figure`
4. Use colors from `config.ACTIVITY_COLORS`
5. Call from `app.py`

### Adding New Metrics

1. Add calculation to `utils.py`
2. Return dictionary or single value
3. Add formatting if needed
4. Display in `app.py`

### Adding New Activity Types

1. Update `config.ACTIVITY_GROUP_MAP`
2. Add color to `config.ACTIVITY_COLORS`
3. No code changes needed elsewhere

### Adding Configuration Options

1. Add constant to `config.py`
2. Import where needed
3. Document in README.md

## Performance Considerations

### Caching Strategy
- Cache data loading (expensive)
- Don't cache UI generation (cheap)
- Cache invalidates on file change

### Data Size Handling
- Tested with 5000+ activities
- Aggregations before visualization
- Efficient pandas operations
- Consider sampling for huge datasets

### Optimization Opportunities
- Lazy loading of tabs
- Progressive rendering for large charts
- Database backend for >10k activities
- Parallel processing for aggregations

## Security & Privacy

### Data Handling
- All data stays local
- No external API calls
- No data transmission
- CSV never modified

### Input Validation
- Pandas handles type conversion
- Error handling for missing columns
- Safe defaults for missing data

## Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Community Cloud
- Push to GitHub
- Connect repository
- Auto-deploy on commit

### Docker
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

### Self-Hosted
- Use systemd service
- Nginx reverse proxy
- SSL certificate

## Testing Strategy

### Unit Tests
- Test each module independently
- Mock external dependencies
- Cover edge cases

### Integration Tests
- Test data flow
- Verify calculations
- Check chart generation

### Example Test Structure
```python
# tests/test_utils.py
def test_calculate_fun_metrics():
    df = create_sample_dataframe()
    metrics = calculate_fun_metrics(df)
    assert metrics['times_around_world'] > 0
```

## Future Architecture Considerations

### Scalability
- Move to database for large datasets
- API backend separation
- Microservices architecture

### Features
- Real-time API integration with fitness platforms
- Multi-user support
- Comparison features
- Export capabilities

### Technology
- FastAPI backend
- React frontend
- PostgreSQL database
- Redis caching

---

**Last Updated**: December 2025
**Version**: 1.0.0
