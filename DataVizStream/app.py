import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import time
from datetime import datetime
import os

# Hide Streamlit Deploy button and default menu
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header [data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    button[aria-label="Share"], button[aria-label="Deploy"] {display: none !important;}
    [data-testid="stDeployButton"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Import visualization modules
from visualizations.geolocation_bubble import create_geolocation_visualization
from visualizations.wave_surface import create_wave_surface_visualization
from visualizations.spiral_tunnel import create_spiral_tunnel_visualization
from visualizations.ripple_bubbles import create_ripple_bubbles_visualization
from visualizations.undulating_wave import create_undulating_wave_visualization
from utils.data_sources import get_real_time_data, get_unicorn_data

# Configure page
st.set_page_config(
    page_title="3D Visualization Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 30

# Sidebar navigation
st.sidebar.title("🎯 3D Visualization Dashboard")
st.sidebar.markdown("---")

# Navigation tabs - 5 Unicorn Visualization Concepts
visualization_options = [
    "The AI Innovation Wave",
    "The Unicorn Surge", 
    "Industry Quake: AI's Ripple Effect",
    "The AI Ascent: Charting Startup Velocity",
    "The AI Growth Spiral"
]

selected_viz = st.sidebar.selectbox(
    "Select Visualization",
    visualization_options,
    index=0
)

# Refresh controls
st.sidebar.markdown("### 🔄 Data Refresh Controls")
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("🔄 Refresh Now"):
        st.session_state.last_refresh = datetime.now()
        st.rerun()

with col2:
    st.session_state.auto_refresh = st.checkbox(
        "Auto Refresh",
        value=st.session_state.auto_refresh
    )

st.session_state.refresh_interval = st.sidebar.slider(
    "Refresh Interval (seconds)",
    min_value=10,
    max_value=300,
    value=st.session_state.refresh_interval,
    step=10
)

# Data source selection
st.sidebar.markdown("### 📊 Unicorn Data Sources")
data_source = st.sidebar.selectbox(
    "Select Data Source",
    [
        "Large Unicorn Dataset",
        "Real-time Unicorn Data", 
        "Static Unicorn Dataset",
        "AI-Powered Unicorn Analysis"
    ],
    index=0
)

# Dataset size control
st.sidebar.markdown("### 🔢 Unicorn Dataset Size")
if "Large" in data_source:
    dataset_size = st.sidebar.slider(
        "Number of Unicorn Companies",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100
    )
else:
    dataset_size = st.sidebar.number_input(
        "Max Unicorn Companies",
        min_value=10,
        max_value=500,
        value=100,
        step=10
    )

# Status indicators
st.sidebar.markdown("### 📈 Status")
st.sidebar.info(f"Last Updated: {st.session_state.last_refresh.strftime('%H:%M:%S')}")

if st.session_state.auto_refresh:
    st.sidebar.success("🟢 Auto Refresh: ON")
else:
    st.sidebar.warning("🟡 Auto Refresh: OFF")

# Auto refresh functionality
if st.session_state.auto_refresh:
    time_since_refresh = (datetime.now() - st.session_state.last_refresh).seconds
    if time_since_refresh >= st.session_state.refresh_interval:
        st.session_state.last_refresh = datetime.now()
        st.rerun()

# Main content area
st.title("🦄 Unicorn Startup 3D Visualization Dashboard")
st.markdown("Interactive 3D visualization of unicorn startups with AI impact scoring powered by i2u.ai")

# Import additional data functions
from utils.data_sources import (
    get_crypto_data, get_market_data, get_weather_stations_data,
    get_nyc_open_data, get_github_activity_data, get_earthquake_data,
    generate_large_realistic_dataset
)

# Get data based on selection
try:
    start_time = time.time()
    
    if data_source == "Large Unicorn Dataset":
        data = generate_large_realistic_dataset(dataset_size)
    elif data_source == "Real-time Unicorn Data":
        # Combine real-time with unicorn focus
        data = get_real_time_data()
        if data and len(data) > dataset_size:
            data = data[:dataset_size]
    elif data_source == "AI-Powered Unicorn Analysis":
        # Generate AI-enhanced unicorn data
        base_data = get_unicorn_data()
        if len(base_data) < dataset_size:
            additional_data = generate_large_realistic_dataset(dataset_size - len(base_data))
            data = base_data + additional_data
        else:
            data = base_data[:dataset_size]
    else:  # Static Unicorn Dataset
        data = get_unicorn_data()
        if data and len(data) > dataset_size:
            data = data[:dataset_size]
        
    load_time = time.time() - start_time
    data_status = f"✅ Data loaded successfully in {load_time:.2f}s"
    
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    data = get_unicorn_data()
    data_status = "⚠️ Using fallback unicorn data"

# Display data status and metrics
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    st.info(data_status)
with col2:
    data_count = len(data) if data is not None else 0
    st.metric("Data Points", f"{data_count:,}")
with col3:
    if data is not None and len(data) > 0:
        data_df = pd.DataFrame(data)
        memory_usage = data_df.memory_usage(deep=True).sum() / (1024 * 1024)  # MB
        st.metric("Memory Usage", f"{memory_usage:.1f} MB")
    else:
        st.metric("Memory Usage", "0 MB")
with col4:
    if st.button("📥 Export Data"):
        if data is not None:
            csv = pd.DataFrame(data).to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# Display data type breakdown
if data is not None and len(data) > 0:
    with st.expander("📊 Dataset Overview", expanded=False):
        data_df = pd.DataFrame(data)
        
        # Data type breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Sector Distribution:**")
            if 'Sector' in data_df.columns:
                sector_counts = data_df['Sector'].value_counts()
                st.bar_chart(sector_counts)
            elif 'type' in data_df.columns:
                type_counts = data_df['type'].value_counts()
                st.bar_chart(type_counts)
            else:
                st.info("No sector classification available")
                
        with col2:
            st.markdown("**Status Distribution:**")
            if 'Status' in data_df.columns:
                status_counts = data_df['Status'].value_counts()
                st.bar_chart(status_counts)
            elif 'Country' in data_df.columns:
                country_counts = data_df['Country'].value_counts().head(10)
                st.bar_chart(country_counts)
            else:
                st.info("No status data available")
        
        # Sample data preview
        st.markdown("**Sample Data (First 10 Rows):**")
        st.dataframe(data_df.head(10), use_container_width=True)

# Render selected visualization
st.markdown("---")

try:
    if "The AI Innovation Wave" in selected_viz:
        fig = create_wave_surface_visualization(data)
        st.subheader("The AI Innovation Wave")
        st.markdown("**Dimensions:** X-axis = Growth Rate | Y-axis = Valuation | Z-axis = AI Impact Score (powered by i2u.ai)")
        st.markdown("Companies visualized as peaks rising from the crest of the wave.")
        
    elif "The Unicorn Surge" in selected_viz:
        fig = create_spiral_tunnel_visualization(data)
        st.subheader("The Unicorn Surge")
        st.markdown("**Interactive VR-style corridor** lined with glowing nodes representing unicorns and soonicorns.")
        st.markdown("Click nodes to explore company profiles. Tunnel accelerates with growth velocity.")
        
    elif "Industry Quake: AI's Ripple Effect" in selected_viz:
        fig = create_ripple_bubbles_visualization(data)
        st.subheader("Industry Quake: AI's Ripple Effect")
        st.markdown("**Disruption waves across industries.** Startups sit at epicenter, sending shockwaves based on market impact.")
        st.markdown("AI integration predicts future ripples and simulates potential disruptions.")
        
    elif "The AI Ascent: Charting Startup Velocity" in selected_viz:
        fig = create_undulating_wave_visualization(data)
        st.subheader("The AI Ascent: Charting Startup Velocity")
        st.markdown("**Acceleration toward unicorn status.** Height = Valuation | Color = Sector | Speed = Growth Velocity")
        st.markdown("Shows the vertical journey from startup to unicorn powered by AI.")
        
    elif "The AI Growth Spiral" in selected_viz:
        fig = create_geolocation_visualization(data)
        st.subheader("The AI Growth Spiral")
        st.markdown("**Compounding growth of AI-driven startups.** Each spiral loop = milestone (Seed → Series A → Unicorn)")
        st.markdown("AI scoring layer highlights companies likely to spiral upward next.")

    # Display the figure
    if fig:
        # Visualization controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            opacity = st.slider("Surface Opacity", 0.1, 1.0, 0.8, 0.1)
        with col2:
            marker_size = st.slider("Marker Size", 5, 30, 15, 1)
        with col3:
            animation_speed = st.slider("Animation Speed", 0.5, 3.0, 1.0, 0.1)
        
        # Update figure with controls
        if hasattr(fig, 'data'):
            for trace in fig.data:
                if hasattr(trace, 'opacity'):
                    trace.opacity = opacity
                if hasattr(trace, 'marker') and hasattr(trace.marker, 'size'):
                    if isinstance(trace.marker.size, (int, float)):
                        trace.marker.size = marker_size
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True, height=700)
        
except Exception as e:
    st.error(f"❌ Error creating visualization: {str(e)}")
    st.info("Please check your data source and try again.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        🎯 Interactive 3D Visualization Dashboard | Built with Streamlit & Plotly
    </div>
    """,
    unsafe_allow_html=True
)

# Auto-refresh placeholder for smooth updates
if st.session_state.auto_refresh:
    placeholder = st.empty()
    with placeholder.container():
        progress_bar = st.progress(0)
        for i in range(st.session_state.refresh_interval):
            progress_bar.progress((i + 1) / st.session_state.refresh_interval)
            time.sleep(1)
        placeholder.empty()
        st.rerun()
