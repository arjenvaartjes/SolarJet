from dynamics import *
import plotly.graph_objects as go
from plotting import *

# Define solar system bodies
sun = Body("Sun", x=np.array([0.0, 0.0, 0.0]), v=np.array([0.0, 0.0, 0.0]), mass=1.989e30)
mercury = Body("Mercury", x=np.array([57.9e9, 0.0, 0.0]), v=np.array([0.0, 47.36e3, 0.0]), mass=3.285e23)
venus = Body("Venus", x=np.array([108.2e9, 0.0, 0.0]), v=np.array([0.0, 35.02e3, 0.0]), mass=4.867e24)
earth = Body("Earth", x=np.array([149.6e9, 0.0, 0.0]), v=np.array([0.0, 29.78e3, 0.0]), mass=5.972e24)
mars = Body("Mars", x=np.array([227.9e9, 0.0, 0.0]), v=np.array([0.0, 24.077e3, 0.0]), mass=6.39e23)
jupiter = Body("Jupiter", x=np.array([778.5e9, 0.0, 0.0]), v=np.array([0.0, 13.07e3, 0.0]), mass=1.898e27)
saturn = Body("Saturn", x=np.array([1.433e12, 0.0, 0.0]), v=np.array([0.0, 9.68e3, 0.0]), mass=5.683e26)
uranus = Body("Uranus", x=np.array([2.877e12, 0.0, 0.0]), v=np.array([0.0, 6.8e3, 0.0]), mass=8.681e25)
neptune = Body("Neptune", x=np.array([4.503e12, 0.0, 0.0]), v=np.array([0.0, 5.43e3, 0.0]), mass=1.024e26)

bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
dt = 10*86400  # one day in seconds
time = np.arange(0, 10*365*24*3600, dt)  # simulate ten years

# Update the positions of all bodies over time
for i, t in enumerate(time):
    update_bodies(bodies, dt)

plot_bodies_animated(bodies)

1/0

# Set up plot
fig, ax = plt.subplots(figsize=(20, 10))

# Plot each body
colors = ['yellow', 'gray', 'orange', 'blue', 'red', 'brown', 'lightblue', 'lightgreen', 'blue']
labels = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
plots = []
trajectories = []

for i, body in enumerate(bodies):
    plot, = ax.plot([], [], color=colors[i], marker='o', label=labels[i], markersize=2)
    trajectory, = ax.plot([], [], color=colors[i], lw=1)
    plots.append(plot)
    trajectories.append(trajectory)

ax.legend()

# Initialize the plot and set sensible initial limits
def init():
    # Find the min and max of initial positions to set the initial limits
    x_positions = [body.x[0, 0] for body in bodies]
    y_positions = [body.x[0, 1] for body in bodies]
    
    # Calculate a margin for better visualization
    x_margin = (max(x_positions) - min(x_positions)) * 0.1
    y_margin = (max(y_positions) - min(y_positions)) * 0.1
    
    # Set initial limits
    ax.set_xlim(-max(x_positions) - x_margin, max(x_positions) + x_margin)
    ax.set_ylim(-max(y_positions) - x_margin, max(y_positions) + x_margin)
    
    for plot, trajectory in zip(plots, trajectories):
        plot.set_data([], [])
        trajectory.set_data([], [])
    
    return plots + trajectories

def animate(i):
    # Get current x and y axis limits to preserve user zooming
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    for j, body in enumerate(bodies):
        plots[j].set_data([body.x[i, 0]], [body.x[i, 1]])
        trajectories[j].set_data(body.x[:i, 0], body.x[:i, 1])

    # Set the axis limits back to what the user set to maintain zoom level
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    return plots + trajectories

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(time), interval=10, blit=False)

plt.show()
