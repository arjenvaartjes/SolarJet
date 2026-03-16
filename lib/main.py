from planets import *
from dynamics import *
from jets import *
from plotting import *
import numpy as np

dt = 10*86400  # 10x one day in seconds
time = np.arange(0, 10*365*24*3600, dt)[:1]  # simulate ten years

# Update the positions of all bodies over time

for i, t in enumerate(time):
    update_bodies(bodies, dt, earth)
    print(jetson.force)
    print(jetson.a)
    print(jetson.v)
    print(jetson.x)

    print(earth.force)
    print(earth.a)
    print(earth.v)
    print(earth.x)

# plot_radius(bodies)
# plot_bodies_animated(bodies)