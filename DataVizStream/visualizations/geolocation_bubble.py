import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random

def create_geolocation_visualization(data):
    """Create 3D spiraling tsunami visualization - from your concept 5 file."""
    try:
        if not data:
            raise ValueError("No data provided")
            
        # Create DataFrame from data
        df = pd.DataFrame(data)
        
        # Performance optimization for large datasets
        if len(df) > 2000:
            sample_size = 2000
            df = df.sample(n=sample_size, random_state=42)
            print(f"Sampled {sample_size} points from {len(data)} for better performance")
        
        # Ensure required columns exist with fallbacks
        if 'Valuation ($B)' not in df.columns:
            df['Valuation ($B)'] = np.random.uniform(1, 50, len(df))
        if 'AI Impact Score' not in df.columns:
            df['AI Impact Score'] = np.random.uniform(20, 90, len(df))

        print(f"Dataset created with {len(df)} AI companies")
        # Calculate spiral coordinates and create 3D visualization
        print("Calculating spiral coordinates...")

        # Sort by valuation for spiral positioning
        df_sorted = df.sort_values('Valuation ($B)', ascending=True).reset_index(drop=True)

        # Calculate spiral coordinates
        n_points = len(df_sorted)
        t = np.linspace(0, 6*np.pi, n_points)  # 3 full rotations

        # Spiral parameters for tsunami effect
        radius_base = 2
        radius_growth = 0.3
        height_multiplier = 0.5

        # Calculate coordinates
        x_coords = []
        y_coords = []
        z_coords = []

        for i, angle in enumerate(t):
            # Expanding radius as we go up the spiral
            radius = radius_base + radius_growth * i/n_points * 8
            
            # X and Y coordinates for spiral
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            # Z coordinate increases with position and valuation
            z = height_multiplier * i + df_sorted.iloc[i]['Valuation ($B)'] * 0.1
            
            x_coords.append(x)
            y_coords.append(y)
            z_coords.append(z)

        # Add coordinates to dataframe
        df_sorted['x'] = x_coords
        df_sorted['y'] = y_coords
        df_sorted['z'] = z_coords

        print("Spiral coordinates calculated successfully")
        # Create the 3D visualization with proper styling
        print("Creating 3D Plotly visualization...")

        # Create bubble sizes (scale valuation for better visibility, but clamp to a max/min)
        min_size = 8
        max_size = 40
        bubble_sizes = df_sorted['Valuation ($B)'] * 1.2 + min_size  # Lower scaling factor
        bubble_sizes = bubble_sizes.clip(lower=min_size, upper=max_size)

        # Create hover text with detailed information
        hover_text = []
        for i, row in df_sorted.iterrows():
            text = (
                f"<b>{row.get('Company', f'Company {i}')}</b><br>" +
                f"Valuation: ${row['Valuation ($B)']:.1f}B<br>" +
                f"AI Impact Score: {row['AI Impact Score']:.1f}/100<br>"
            )
            hover_text.append(text)

        # Create the 3D scatter plot
        fig = go.Figure()

        # Add the main scatter plot
        scatter = go.Scatter3d(
            x=df_sorted['x'],
            y=df_sorted['y'],
            z=df_sorted['z'],
            mode='markers',
            marker=dict(
                size=bubble_sizes,
                color=df_sorted['AI Impact Score'],
                colorscale='Viridis',
                opacity=0.8,
                colorbar=dict(
                    title="AI Impact Score",
                    x=1.02,  # Position colorbar to the right
                    len=0.7,
                    thickness=15
                ),
                line=dict(width=1, color='white')
            ),
            text=hover_text,
            hovertemplate='%{text}<extra></extra>',
            name='AI Startups'
        )

        fig.add_trace(scatter)

        print("Main scatter plot created")
        # Add spiral trajectory line for tsunami effect
        print("Adding spiral trajectory line...")

        # Create a smooth spiral line
        t_smooth = np.linspace(0, 6*np.pi, 200)
        x_line = []
        y_line = []
        z_line = []

        for i, angle in enumerate(t_smooth):
            radius = radius_base + radius_growth * i/200 * 8
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            z = height_multiplier * i/200 * n_points
            
            x_line.append(x)
            y_line.append(y)
            z_line.append(z)

        # Add spiral line
        spiral_line = go.Scatter3d(
            x=x_line,
            y=y_line,
            z=z_line,
            mode='lines',
            line=dict(
                color='rgba(255, 255, 255, 0.3)',
                width=3
            ),
            name='Growth Trajectory',
            hoverinfo='skip'
        )

        fig.add_trace(spiral_line)

        print("Spiral trajectory added")
        # Configure layout and styling
        print("Configuring layout and styling...")

        fig.update_layout(
            title={
                'text': '3D AI Startup Growth Tsunami<br><sub>Interactive Spiral Visualization of AI Company Valuations & Impact</sub>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': 'white'}
            },
            scene=dict(
                xaxis=dict(
                    title='X Coordinate',
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.2)',
                    showbackground=True,
                    zerolinecolor='rgba(255,255,255,0.2)',
                ),
                yaxis=dict(
                    title='Y Coordinate', 
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.2)',
                    showbackground=True,
                    zerolinecolor='rgba(255,255,255,0.2)',
                ),
                zaxis=dict(
                    title='Growth Height',
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.2)',
                    showbackground=True,
                    zerolinecolor='rgba(255,255,255,0.2)',
                ),
                bgcolor='rgba(10,10,30,1)',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.2)
                )
            ),
            paper_bgcolor='rgba(10,10,30,1)',
            plot_bgcolor='rgba(10,10,30,1)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                x=0.02,
                y=0.98,
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1
            ),
            margin=dict(l=0, r=0, t=80, b=0),
            width=1000,
            height=700
        )

        print("Layout configured successfully")
        
        return fig
        
    except Exception as e:
        print(f"Error in spiraling tsunami visualization: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers'))
        fig.update_layout(title="Error in Spiraling Tsunami Visualization")
        return fig