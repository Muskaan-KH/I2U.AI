# The error is an IndentationError, which means there's an unexpected indent in the code.
# Let's fix the indentation in the code snippet.

import numpy as np
import plotly.graph_objects as go
import pandas as pd

# Load the data for visualization
# The unicorn_spiral_spectrum1.html file is likely generated from unicorn_data.json
# so we use that as the data source

df = pd.read_json('unicorn_data.json')

# Normalize growth rate for tunnel speed
# (Assume 'Growth Rate (%)' is a column in the data)
growth_norm = (df['Growth Rate (%)'] - df['Growth Rate (%)'].min()) / (df['Growth Rate (%)'].max() - df['Growth Rate (%)'].min())

# Create a spiral tunnel spectrum
num_points = len(df)
# Spiral parameters
num_turns = 6  # More turns for a tunnel effect
z = np.linspace(0, 100, num_points)  # Height of the tunnel
# Spiral angle: more turns, evenly spaced
theta = np.linspace(0, num_turns * 2 * np.pi, num_points)
# Radius: can be constant or vary with growth
r_base = 40  # Increased from 20 to 40 for a larger tunnel radius
r_variation = 20 * growth_norm  # Increased from 10 to 20 for more spread
r = r_base + r_variation
# Cartesian coordinates
x = r * np.cos(theta)
y = r * np.sin(theta)

# Create the figure
fig = go.Figure()

# Add the spiral as a 3D line (tunnel effect)
# Prepare hover text with company details
hover_text = [
    f"<b>{row['Company']}</b><br>Valuation: ${row['Valuation ($B)']}B<br>AI Impact Score: {row['AI Impact Score']}<br>Growth Rate: {row['Growth Rate (%)']}%"
    for _, row in df.iterrows()
]
fig.add_trace(go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='lines+markers',
    line=dict(color='royalblue', width=6),
    marker=dict(size=7, color=z, colorscale='Viridis', opacity=0.8),
    hoverinfo='text',
    text=hover_text
))

# Add a tube-like mesh for a tunnel effect (optional, for more realism)
# Uncomment below for a mesh tunnel (requires more points for smoothness)
# from skimage.measure import marching_cubes_lewiner
# theta_dense = np.linspace(0, num_turns * 2 * np.pi, num_points * 10)
# z_dense = np.linspace(0, 100, num_points * 10)
# r_dense = r_base + np.mean(r_variation)
# x_tube = r_dense * np.cos(theta_dense)
# y_tube = r_dense * np.sin(theta_dense)
# fig.add_trace(go.Scatter3d(x=x_tube, y=y_tube, z=z_dense, mode='lines', line=dict(color='lightblue', width=2), opacity=0.2))

# Update layout for better visualization
fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectratio=dict(x=1, y=1, z=2),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
    ),
    title='Unicorn Companies Tunnel Spiral Spectrum',
    margin=dict(l=0, r=0, b=0, t=40)
)

# Save the plot as an HTML file (overwrite unicorn_spiral_spectrum1.html)
file_path = 'unicorn_spiral_spectrum1.html'
fig.write_html(file_path)

# Optionally open the HTML file in the default web browser
import webbrowser
webbrowser.open(file_path)

file_path