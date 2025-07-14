import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import griddata

def create_wave_surface_visualization(data):
    """Create 3D wave surface visualization - from your concept 1 file."""
    try:
        if not data:
            raise ValueError("No data provided")
            
        df = pd.DataFrame(data)
        
        # Performance optimization for large datasets
        if len(df) > 1500:
            sample_size = 1500
            df = df.sample(n=sample_size, random_state=42)
            print(f"Sampled {sample_size} points for wave surface performance")
        
        # Ensure required columns exist with fallbacks
        if 'Growth Rate (%)' not in df.columns:
            df['Growth Rate (%)'] = np.random.uniform(50, 200, len(df))
        if 'Valuation ($B)' not in df.columns:
            df['Valuation ($B)'] = np.random.uniform(1, 50, len(df))
        if 'AI Impact Score' not in df.columns:
            df['AI Impact Score'] = np.random.uniform(20, 90, len(df))

        # Normalize growth rate for marker size (optional, for visual effect)
        growth_norm = (df['Growth Rate (%)'] - df['Growth Rate (%)'].min()) / (df['Growth Rate (%)'].max() - df['Growth Rate (%)'].min() + 1e-9)

        # --- 2. Generate 3D Wave Surface Data ---
        # Define the range for X (Growth Rate) and Y (Valuation) for the surface grid
        x_min, x_max = df['Growth Rate (%)'].min(), df['Growth Rate (%)'].max()
        y_min, y_max = df['Valuation ($B)'].min(), df['Valuation ($B)'].max()

        # Create a dense meshgrid for the surface to ensure smoothness
        # Increased num_points for a smoother, more detailed wave
        num_points = 100
        xi = np.linspace(x_min, x_max, num_points)
        yi = np.linspace(y_min, y_max, num_points)
        XI, YI = np.meshgrid(xi, yi)

        # Prepare points and values for interpolation
        # 'points' are the (x, y) coordinates of your actual data
        points = df[['Growth Rate (%)', 'Valuation ($B)']].values
        # 'values' are the Z-values (AI Impact Score) corresponding to 'points'
        values = df['AI Impact Score'].values

        # Interpolate AI Impact Score (Z) onto the meshgrid using cubic interpolation for smoothness
        ZI = griddata(points, values, (XI, YI), method='cubic')

        # Add a subtle sine/cosine wave effect to create a more pronounced "wave" appearance
        # Adjust amplitude and frequencies to control the wave's height and ripple density
        wave_amplitude = 1.5 # Controls the height of the added wave
        wave_frequency_x = 0.2 # Controls ripples along the X-axis (Growth Rate)
        wave_frequency_y = 0.1 # Controls ripples along the Y-axis (Valuation)
        ZI_wave_effect = ZI + wave_amplitude * (np.sin(wave_frequency_x * XI) + np.cos(wave_frequency_y * YI))

        # Handle NaNs that might result from interpolation outside the convex hull of data points.
        # Filling with the mean ensures a continuous surface without holes.
        ZI_wave_effect[np.isnan(ZI_wave_effect)] = np.nanmean(ZI_wave_effect)

        # --- 3. Create the Plotly Figure ---
        fig = go.Figure(
            data=[
                # Surface trace for the "wave" effect
                go.Surface(
                    x=XI,
                    y=YI,
                    z=ZI_wave_effect,
                    colorscale='Jet', # 'Jet' colorscale for distinct wave colors
                    opacity=0.8, # Slightly transparent wave
                    showscale=False, # Hide color scale for the surface
                    name='AI Impact Surface',
                    hoverinfo='skip' # No hover info for the surface itself
                ),
                # Scatter3d trace for individual company "bubbles"
                go.Scatter3d(
                    x=df['Growth Rate (%)'],
                    y=df['Valuation ($B)'],
                    z=df['AI Impact Score'] + 0.5,
                    mode='markers+text',
                    marker=dict(
                        size=8 + 12 * growth_norm,
                        color=df['AI Impact Score'],
                        colorscale='Hot',
                        colorbar=dict(title='AI Impact Score', x=0.85, y=0.7),
                        opacity=0.9,
                        line=dict(color='black', width=0.5)
                    ),
                    text=[
                        f"{row.get('Company', f'Company {i}')}" for i, (_, row) in enumerate(df.iterrows())
                    ],
                    textposition='top center',
                    textfont=dict(color='black', size=10, family='Arial'),
                    hovertext=[
                        f"<b>{row.get('Company', f'Company {i}')}</b><br>Valuation: ${row['Valuation ($B)']}B<br>AI Impact Score: {row['AI Impact Score']}<br>Growth Rate: {row['Growth Rate (%)']}%"
                        for i, (_, row) in enumerate(df.iterrows())
                    ],
                    hoverinfo='text',
                    name='Unicorn Companies'
                )
            ],
            layout=go.Layout(
                title={
                    'text': 'Unicorn Wave: Growth, Valuation & AI Impact',
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 24, 'color': '#2C3E50', 'family': 'Arial, sans-serif'}
                },
                scene=dict(
                    xaxis_title='Growth Rate (%)',
                    yaxis_title='Valuation (Billions USD)',
                    zaxis_title='AI Impact Score',
                    # Set initial camera angle for optimal view
                    camera=dict(
                        eye=dict(x=1.8, y=1.8, z=0.8) # Adjust these values to change default view
                    ),
                    xaxis=dict(backgroundcolor="#F0F0F0", gridcolor="white", showbackground=True, zerolinecolor="white"),
                    yaxis=dict(backgroundcolor="#F0F0F0", gridcolor="white", showbackground=True, zerolinecolor="white"),
                    zaxis=dict(backgroundcolor="#F0F0F0", gridcolor="white", showbackground=True, zerolinecolor="white")
                ),
                margin=dict(l=0, r=0, b=0, t=50),
                hovermode='closest', # Ensures hover works well for clustered points
                paper_bgcolor='#ECF0F1', # Light background for the entire plot area
                plot_bgcolor='#ECF0F1' # Light background for the plot itself
            )
        )
        
        return fig
        
    except Exception as e:
        print(f"Error in wave surface visualization: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers'))
        fig.update_layout(title="Error in Wave Surface Visualization")
        return fig