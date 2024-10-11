import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def plot_radius(bodies):
    """
    Plot the radius (distance from the Sun) of each body in separate subplots.
    
    Parameters:
    bodies (list): List of Body objects containing positions and velocities of solar system bodies.
    """
    # Number of bodies to plot
    num_bodies = len(bodies)
    
    # Create subplots: one row for each body
    fig = make_subplots(rows=num_bodies, cols=1, shared_xaxes=True,
                        subplot_titles=[body.name for body in bodies])
    
    # Time array (assuming the length of the position history is the same for all bodies)
    time = np.arange(len(bodies[0].x))
    
    for i, body in enumerate(bodies):
        # Calculate the radius for each body over time (Euclidean norm)
        radius = np.linalg.norm(body.x, axis=1)
        
        # Create a trace for the current body
        trace = go.Scatter(x=time, y=radius, mode='lines', name=body.name)
        
        # Add the trace to the subplot (one plot per body)
        fig.add_trace(trace, row=i+1, col=1)
    
    # Update layout: you can customize this layout to fit your needs
    fig.update_layout(
        height=300 * num_bodies,  # Height scaling with number of subplots
        title_text="Radius of Bodies from the Sun Over Time",
        xaxis_title="Time (arbitrary units)",
        yaxis_title="Radius (m)",
        showlegend=False
    )
    
    # Show the plot
    fig.show()

# Example: Sun-Earth system
def plot_bodies_animated(bodies):
    fig = go.Figure()

    # Define number of time steps (assuming all bodies have the same time dimension)
    num_steps = bodies[0].x.shape[0]

    # Create initial traces for each body
    for body in bodies:
        # Initial empty trajectory (will be built progressively)
        fig.add_trace(go.Scatter(
            x=[], 
            y=[], 
            mode='lines', 
            name=f"{body.name} trajectory", 
            line=dict(dash='solid', width=1)
        ))
        fig.add_trace(go.Scatter(x=[body.x[0, 0]], y=[body.x[0, 1]], mode='markers', name=body.name))

    # Create frames for each time step
    frames = []
    for t in range(num_steps):
        frame_data = []
        for body in bodies:
            # Add the trajectory from the start up to the current time step
            frame_data.append(go.Scatter(
                x=body.x[:t, 0], 
                y=body.x[:t, 1], 
                mode='lines',
                line=dict(dash='solid', width=1),
                name=f"{body.name} trajectory"
            ))
            frame_data.append(go.Scatter(x=[body.x[t, 0]], y=[body.x[t, 1]]))
        frames.append(go.Frame(data=frame_data, name=str(t)))

    # Update layout with animation settings
    fig.update_layout(
        title="Solar System Simulation",
        xaxis=dict(range=[-5e12, 5e12]),  # Fix x-axis bounds
        yaxis=dict(range=[-5e12, 5e12]),  # Fix y-axis bounds
        xaxis_title="X (m)", 
        yaxis_title="Y (m)",
        updatemenus=[{
            'type': 'buttons',
            'buttons': [{
                'label': 'Play',
                'method': 'animate',
                'args': [None, {
                    'frame': {'duration': 10, 'redraw': True},
                    'fromcurrent': True,
                    'mode': 'immediate'
                }]
            }, {
                'label': 'Pause',
                'method': 'animate',
                'args': [[None], {'frame': {'duration': 0}, 'mode': 'immediate'}]
            }]
        }]
    )

    # Add slider to control the frames
    sliders = [{
        'steps': [{
            'args': [[str(t)], {'frame': {'duration': 10, 'redraw': True}, 'mode': 'immediate'}],
            'label': str(t),
            'method': 'animate'
        } for t in range(num_steps)],
        'currentvalue': {'prefix': 'Frame: '}
    }]

    fig.update_layout(sliders=sliders)

    # Add frames to figure
    fig.frames = frames

    fig.show()