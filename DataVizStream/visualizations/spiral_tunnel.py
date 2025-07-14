import numpy as np
import plotly.graph_objects as go
import pandas as pd

def create_spiral_tunnel_visualization(data):
    """Create 3D spiral tunnel visualization - from your concept 2 file."""
    try:
        if not data:
            raise ValueError("No data provided")
            
        df = pd.DataFrame(data)
        
        # Performance optimization for large datasets
        if len(df) > 1000:
            sample_size = 1000
            df = df.sample(n=sample_size, random_state=42)
            print(f"Sampled {sample_size} points for spiral tunnel performance")
        
        # Ensure required columns exist with fallbacks
        if 'Growth Rate (%)' not in df.columns:
            df['Growth Rate (%)'] = np.random.uniform(50, 200, len(df))
        if 'Valuation ($B)' not in df.columns:
            df['Valuation ($B)'] = np.random.uniform(1, 50, len(df))
        if 'AI Impact Score' not in df.columns:
            df['AI Impact Score'] = np.random.uniform(20, 90, len(df))

        # Normalize growth rate for tunnel speed
        # (Assume 'Growth Rate (%)' is a column in the data)
        growth_norm = (df['Growth Rate (%)'] - df['Growth Rate (%)'].min()) / (df['Growth Rate (%)'].max() - df['Growth Rate (%)'].min() + 1e-9)

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
            f"<b>{row.get('Company', f'Company {i}')}</b><br>Valuation: ${row['Valuation ($B)']}B<br>AI Impact Score: {row['AI Impact Score']}<br>Growth Rate: {row['Growth Rate (%)']}%"
            for i, (_, row) in enumerate(df.iterrows())
        ]
        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='lines+markers',
            line=dict(color='royalblue', width=6),
            marker=dict(size=7, color=z, colorscale='Viridis', opacity=0.8),
            hoverinfo='text',
            text=hover_text,
            name='Tunnel Trajectory'
        ))

        # Update layout for better visualization
        fig.update_layout(
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                aspectratio=dict(x=1, y=1, z=2),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
                bgcolor='rgba(10,10,30,1)'
            ),
            title='Unicorn Companies Tunnel Spiral Spectrum',
            margin=dict(l=0, r=0, b=0, t=40),
            paper_bgcolor='rgba(10,10,30,1)',
            font=dict(color='white')
        )
        
        return fig
        
    except Exception as e:
        print(f"Error in spiral tunnel visualization: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers'))
        fig.update_layout(title="Error in Spiral Tunnel Visualization")
        return fig