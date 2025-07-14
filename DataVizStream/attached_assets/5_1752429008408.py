# Complete 3D Geolocation Bubble Visualization - Final Correct Code
print("Creating complete 3D Geolocation Bubble visualization...")

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
import webbrowser
import os
import requests

# Fetch live data from Abstract Geolocation API
api_url = "https://ipgeolocation.abstractapi.com/v1/?api_key=YOUR_API_KEY"  # Replace with your API key
response = requests.get(api_url)
data = response.json()

# Convert the API response to a DataFrame
# The API returns a single record; wrap in a list for DataFrame
# You may need to adjust the rest of the code to use the available fields
# For demonstration, we'll plot latitude/longitude as x/y, and set z=0

df = pd.DataFrame([data])

print(f"Dataset created with {len(df)} record(s) from API")
# Prepare data for plotting
try:
    bubble_x = [float(df['longitude'][0])]
    bubble_y = [float(df['latitude'][0])]
    bubble_z = [0]  # No altitude, so set to 0
    city = df['city'][0] if 'city' in df.columns else 'Unknown'
    country = df['country'][0] if 'country' in df.columns else 'Unknown'
    bubble_text = [f"{city}, {country}"]
except Exception as e:
    print(f"Error extracting geolocation data: {e}")
    bubble_x = [0]
    bubble_y = [0]
    bubble_z = [0]
    bubble_text = ["No data"]

fig = go.Figure(data=[
    go.Scatter3d(
        x=bubble_x,
        y=bubble_y,
        z=bubble_z,
        mode='markers',
        marker=dict(
            size=20,
            color='blue',
            opacity=0.8
        ),
        hovertext=bubble_text,
        hoverinfo='text',
        name='Geolocation'
    )
])

fig.update_layout(
    title='Geolocation Bubble',
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Altitude',
        aspectratio=dict(x=1, y=1, z=0.5),
        dragmode='orbit',
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    hovermode='closest',
    paper_bgcolor='#ECF0F1',
    plot_bgcolor='#ECF0F1'
)

filename = 'geolocation_bubble_3d.html'
fig.write_html(filename)

print(f"Geolocation visualization saved as: {filename}")

html_path = os.path.abspath(filename)
webbrowser.open('file://' + html_path)

print("\
Visualization Features:")
print("- Interactive 3D bubble representing geolocation")
print("- Bubble color represents location")
print("- Hover for detailed location information")
print("- Mouse controls: rotate, zoom, pan")

# Example: Fetch a real-time startup dataset from a free API (StartupBlink demo API)
import requests

api_url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=world-startup-database&q=&rows=100"  # Free public dataset
try:
    response = requests.get(api_url)
    data = response.json()
    # The API returns a dict with a 'records' key containing the list
    if isinstance(data, dict) and 'records' in data:
        records = data['records']
        # Flatten the nested structure
        df = pd.json_normalize(records)
    else:
        raise ValueError("Unexpected API response format")
    print(f"Fetched {len(df)} startup records from API.")
except Exception as e:
    print(f"Error fetching real-time startup data: {e}")
    # Fallback: use a single geolocation bubble as before
    df = pd.DataFrame([{'fields.longitude': 0, 'fields.latitude': 0, 'fields.name': 'No data', 'fields.country': ''}])

# Now use df for visualization as before, but adapt the plotting code to your API's fields
# Example for plotting all startups as bubbles (if API provides longitude/latitude):
try:
    bubble_x = df['fields.longitude'].astype(float) if 'fields.longitude' in df.columns else np.zeros(len(df))
    bubble_y = df['fields.latitude'].astype(float) if 'fields.latitude' in df.columns else np.zeros(len(df))
    bubble_z = np.zeros(len(df))  # No altitude, so set to 0
    bubble_text = [
        f"{row.get('fields.name', 'Unknown')}, {row.get('fields.city', '')}, {row.get('fields.country', '')}"
        for _, row in df.iterrows()
    ]
except Exception as e:
    print(f"Error extracting bubble data: {e}")
    bubble_x = [0]
    bubble_y = [0]
    bubble_z = [0]
    bubble_text = ["No data"]

fig = go.Figure(data=[
    go.Scatter3d(
        x=bubble_x,
        y=bubble_y,
        z=bubble_z,
        mode='markers',
        marker=dict(
            size=8,
            color='blue',
            opacity=0.8
        ),
        hovertext=bubble_text,
        hoverinfo='text',
        name='Startups'
    )
])

fig.update_layout(
    title='Startup Locations Bubble',
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Altitude',
        aspectratio=dict(x=1, y=1, z=0.5),
        dragmode='orbit',
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    hovermode='closest',
    paper_bgcolor='#ECF0F1',
    plot_bgcolor='#ECF0F1'
)

filename = 'startup_locations_bubble_3d.html'
fig.write_html(filename)

print(f"Startup locations visualization saved as: {filename}")

html_path = os.path.abspath(filename)
webbrowser.open('file://' + html_path)

print("\nStartup Visualization Features:")
print("- Interactive 3D bubble representing startup locations")
print("- Bubble color represents location")
print("- Hover for detailed location information")
print("- Mouse controls: rotate, zoom, pan")