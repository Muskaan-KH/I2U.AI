import numpy as np
import plotly.graph_objects as go
import pandas as pd

def create_undulating_wave_visualization(data):
    """Create 3D undulating wave surface with multiple oscillations - from your concept 4 file."""
    try:
        if not data:
            raise ValueError("No data provided")
            
        df = pd.DataFrame(data)
        
        # Performance optimization for large datasets
        if len(df) > 1200:
            sample_size = 1200
            df = df.sample(n=sample_size, random_state=42)
            print(f"Sampled {sample_size} points for undulating wave performance")
        
        # Ensure required columns exist with fallbacks
        if 'Growth Rate (%)' not in df.columns:
            df['Growth Rate (%)'] = np.random.uniform(50, 200, len(df))
        if 'Valuation ($B)' not in df.columns:
            df['Valuation ($B)'] = np.random.uniform(1, 50, len(df))
        if 'AI Impact Score' not in df.columns:
            df['AI Impact Score'] = np.random.uniform(20, 90, len(df))

        # Generate grid points for the surface
        grid_size = 50

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
            f"<b>{row.get('Company', f'Company {i}')}</b><br>Valuation: ${row['Valuation ($B)']}B<br>AI Impact Score: {row['AI Impact Score']}<br>Growth Rate: {row['Growth Rate (%)']}%"
            for i, (_, row) in enumerate(df.iterrows())
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

        fig_surface.update_layout(
            scene=dict(
                xaxis_title='Valuation ($B)',
                yaxis_title='Growth Rate (%)',
                zaxis_title='Wave Height',
            ),
            margin=dict(l=0, r=0, b=0, t=50)
        )
        
        return fig_surface
        
    except Exception as e:
        print(f"Error in undulating wave visualization: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers'))
        fig.update_layout(title="Error in Undulating Wave Visualization")
        return fig