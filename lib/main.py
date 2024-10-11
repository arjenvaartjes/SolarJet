from dynamics import *
from planets import *
from plotting import *
import numpy as np

dt = 10*86400  # 10x one day in seconds
time = np.arange(0, 10*365*24*3600, dt)  # simulate ten years

# Update the positions of all bodies over time
for i, t in enumerate(time):
    update_bodies(bodies, dt)

# plot_radius(bodies)
plot_bodies_animated(bodies)