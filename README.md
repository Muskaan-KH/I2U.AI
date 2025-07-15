# I2U.AI

# Unicorn Startup 3D Visualization Dashboard

## Overview
This project is an interactive Streamlit dashboard for visualizing unicorn startup data in 3D. It features multiple unique visualization concepts, real-time and static data sources. The dashboard is designed for performance, clarity, and a clean user experience.

## Features
- **Five 3D Visualization Concepts**: Explore unicorn startups using wave, tunnel, ripple, and spiral visualizations.
- **Multiple Data Sources**: Supports large synthetic datasets, real-time API data, and static JSON files.
- **No Export/Deploy UI**: All export and deploy controls are removed for a focused dashboard experience.
- **Auto-Refresh**: Configurable auto-refresh for real-time data updates.
- **Modern UI**: Clean, responsive layout with sidebar controls and interactive charts.

## Getting Started

### Prerequisites
- Python 3.10+
- Recommended: Create a virtual environment

### Install Dependencies
```powershell
pip install -r requirements.txt
```
Or, if `requirements.txt` is not present, install manually:
```powershell
pip install streamlit pandas numpy plotly sqlalchemy requests
```

### Run the Dashboard
```powershell
python -m streamlit run app.py --server.port 5001
```
Then open [http://localhost:5001](http://localhost:5001) in your browser.

## Project Structure
```
DataVizStream/
├── app.py                  # Main Streamlit app
├── utils/
│   └── data_sources.py     # Data loading 
├── visualizations/         # Visualization modules
├── unicorn_data_comprehensive.json  # Main unicorn dataset
├── unicorns.db             # SQLite database
├── attached_assets/        # Extra scripts and data
```

## Data Sources
- **JSON Files**: Fallback for unicorn data if DB is empty.
- **APIs**: Real-time data for startups data.

## Customization
- Add new visualization concepts in the `visualizations/` folder.
- Update or add unicorn data in the JSON files.
- Adjust UI and controls in `app.py` as needed.

## Notes
- The dashboard hides all Streamlit export and deploy UI elements for a clean look.
- If you see runtime warnings, they do not affect dashboard functionality.

## Project Creation Process & Tools Used

### How This Project Was Built
- **Project Planning**: Defined requirements for a interactive unicorn startup dashboard with multiple 3D visualization concepts and a clean, export-free UI.
- **Environment Setup**: Created a Python virtual environment and installed all required libraries.
- **Core Framework**: Used [Streamlit](https://streamlit.io/) for rapid web app development and interactive UI components.
- **Visualization**: Built 3D visualizations using [Plotly](https://plotly.com/python/) for interactive, high-performance graphics.
- **Data Sources**: Integrated real-time and static data sources, including APIs for startups data.
- **Performance Optimization**: Ensured fast dashboard loading by prioritizing DB reads and limiting dataset size in the UI.
- **UI/UX Customization**: Removed all export and deploy controls using custom CSS and Streamlit configuration for a focused user experience.
- **Testing & Iteration**: Ran the app locally, optimized for speed, and iteratively improved the UI and data logic.

### Main Tools & Libraries
- **Streamlit**: Web app framework for Python
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Plotly**: 3D and interactive visualizations
- **Requests**: HTTP requests for real-time data APIs
- **Python Standard Library**: For JSON, datetime, OS operations, and more


