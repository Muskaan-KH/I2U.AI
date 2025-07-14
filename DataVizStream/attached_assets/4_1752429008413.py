import numpy as np
import plotly.graph_objects as go
import json
import pandas as pd

# Generate grid points for the surface
grid_size = 50

# Load unicorn data
with open('unicorn_data.json', 'r') as file:
    unicorn_data = json.load(file)
df = pd.DataFrame(unicorn_data)

# Set grid range based on data
x_min, x_max = df['Valuation ($B)'].min(), df['Valuation ($B)'].max()
y_min, y_max = df['Growth Rate (%)'].min(), df['Growth Rate (%)'].max()

# Expand a bit for visual margin
x_pad = (x_max - x_min) * 0.1
y_pad = (y_max - y_min) * 0.1
x = np.linspace(x_min - x_pad, x_max + x_pad, grid_size)
y = np.linspace(y_min - y_pad, y_max + y_pad, grid_size)
x_grid, y_grid = np.meshgrid(x, y)

# Create a periodic wave pattern with 10 oscillations
z = np.sin(10 * np.sqrt((x_grid - x_min)/(x_max - x_min + 1e-9) ** 2 + (y_grid - y_min)/(y_max - y_min + 1e-9) ** 2))

# Plot the surface with a color gradient from blue to red
fig_surface = go.Figure(data=[go.Surface(
    x=x,
    y=y,
    z=z,
    colorscale='RdBu',
    colorbar=dict(title='Wave Height'),
    opacity=0.4,
    contours = {
        "z": {
            "show": True,
            "usecolormap": True,
            "highlightcolor":"#42f462",
            "project": {"z": True}
        }
    }
)])

fig_surface.update_layout(title='Undulating Wave Surface with Multiple Oscillations')

# Add company bubbles all over the wave that represent company details
np.random.seed(42)
company_x = np.random.uniform(x_min - x_pad, x_max + x_pad, len(df))
company_y = np.random.uniform(y_min - y_pad, y_max + y_pad, len(df))
company_z = np.sin(10 * np.sqrt((company_x - x_min)/(x_max - x_min + 1e-9) ** 2 + (company_y - y_min)/(y_max - y_min + 1e-9) ** 2))

company_text = [
    f"<b>{row['Company']}</b><br>Valuation: ${row['Valuation ($B)']}B<br>AI Impact Score: {row['AI Impact Score']}<br>Growth Rate: {row['Growth Rate (%)']}%"
    for _, row in df.iterrows()
]

fig_surface.add_trace(go.Scatter3d( 
    x=company_x,
    y=company_y,
    z=company_z,
    mode='markers',
    marker=dict(size=5, color='black', opacity=0.8),
    text=company_text,
    hoverinfo='text',  # Only show company info, not x/y/z
    name='Companies'
))

# Save the plot as an HTML file and open in browser for VS Code terminal compatibility
import os
import webbrowser
html_path = os.path.abspath('11_wave_surface.html')
fig_surface.write_html(html_path)
webbrowser.open('file://' + html_path)