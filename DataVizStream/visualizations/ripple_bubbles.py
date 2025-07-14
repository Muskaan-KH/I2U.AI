import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def create_ripple_bubbles_visualization(data):
    """Create 3D ripple bubbles animation visualization - from your concept 3 file."""
    try:
        if not data:
            raise ValueError("No data provided")
            
        # Convert data to DataFrame
        unicorn_df = pd.DataFrame(data)
        
        # Performance optimization for large datasets
        if len(unicorn_df) > 800:
            sample_size = 800
            unicorn_df = unicorn_df.sample(n=sample_size, random_state=42)
            print(f"Sampled {sample_size} points for ripple bubbles performance")
        
        # Ensure required columns exist with fallbacks
        if 'Growth Rate (%)' not in unicorn_df.columns:
            unicorn_df['Growth Rate (%)'] = np.random.uniform(50, 200, len(unicorn_df))
        if 'Valuation ($B)' not in unicorn_df.columns:
            unicorn_df['Valuation ($B)'] = np.random.uniform(1, 50, len(unicorn_df))
        if 'AI Impact Score' not in unicorn_df.columns:
            unicorn_df['AI Impact Score'] = np.random.uniform(20, 90, len(unicorn_df))

        # Normalize for visualization
        unicorn_df['Valuation_Norm'] = unicorn_df['Valuation ($B)'] / unicorn_df['Valuation ($B)'].max()
        unicorn_df['Growth_Norm'] = unicorn_df['Growth Rate (%)'] / unicorn_df['Growth Rate (%)'].max()
        unicorn_df['Impact_Norm'] = unicorn_df['AI Impact Score'] / unicorn_df['AI Impact Score'].max()

        # Only show company bubbles, no ripple surfaces
        # Spread bubbles all over the 3D space for better visual separation
        np.random.seed(42)  # For reproducibility
        n = len(unicorn_df)
        # Spread bubbles in a cube (0,1) for each axis, but keep color/size meaningful
        bubble_x = np.random.uniform(0, 1, n)
        bubble_y = np.random.uniform(0, 1, n)
        bubble_z = np.random.uniform(0, 1, n)
        bubble_size = np.clip(unicorn_df['Valuation ($B)'] * 0.7, 6, 30)
        bubble_color = unicorn_df['AI Impact Score']
        bubble_text = [
            f"<b>{row.get('Company', f'Company {i}')}</b><br>Valuation: ${row['Valuation ($B)']}B<br>AI Impact Score: {row['AI Impact Score']}<br>Growth Rate: {row['Growth Rate (%)']}%"
            for i, (_, row) in enumerate(unicorn_df.iterrows())
        ]

        fig = go.Figure(data=[
            go.Scatter3d(
                x=bubble_x,
                y=bubble_y,
                z=bubble_z,
                mode='markers',  # Remove '+text' so names are not always shown
                marker=dict(
                    size=bubble_size,
                    color=bubble_color,
                    colorscale='Viridis',
                    opacity=0.9,
                    line=dict(width=1, color='DarkSlateGrey')
                ),
                # Remove text and textposition so names are only in hover
                hovertext=bubble_text,
                hoverinfo='text',
                name='Unicorn Companies'
            )
        ])

        # Animate the ripple effect for the bubbles using Plotly frames
        frames = []
        num_frames = 60
        for frame in range(num_frames):
            frame_bubble_z = []
            for i, row in unicorn_df.iterrows():
                # Animate z as a ripple for each bubble
                z = 0.5 + 0.4 * np.sin(2 * np.pi * frame / num_frames + i * 0.2)
                frame_bubble_z.append(z)
            frames.append(go.Frame(data=[
                go.Scatter3d(
                    x=bubble_x,
                    y=bubble_y,
                    z=frame_bubble_z,
                    mode='markers',
                    marker=dict(
                        size=bubble_size,
                        color=bubble_color,
                        colorscale='Viridis',
                        opacity=0.9,
                        line=dict(width=1, color='DarkSlateGrey')
                    ),
                    hovertext=bubble_text,
                    hoverinfo='text',
                    name='Unicorn Companies'
                )
            ]))
        fig.frames = frames

        fig.update_layout(
            updatemenus=[dict(type='buttons', showactive=False,
                              buttons=[
                                  dict(label='Play', method='animate', args=[None, {'frame': {'duration': 60, 'redraw': True}, 'fromcurrent': True}]),
                                  dict(label='Pause', method='animate', args=[[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}])
                              ])],
            title='3D Unicorn Companies Bubble Map',
            scene=dict(
                xaxis_title='Spread X',
                yaxis_title='Spread Y',
                zaxis_title='Spread Z',
                aspectratio=dict(x=1, y=1, z=1),
                dragmode='orbit',
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            hovermode='closest',
            paper_bgcolor='#ECF0F1',
            plot_bgcolor='#ECF0F1'
        )
        
        return fig
        
    except Exception as e:
        print(f"Error in ripple bubbles visualization: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers'))
        fig.update_layout(title="Error in Ripple Bubbles Visualization")
        return fig