from dynamics import *

# Example: Earth and Moon
body1 = Body("Earth", x=np.array([0.0, 0.0, 0.0]), v=np.array([0.0, 0.0, 0.0]), mass=5.972e24)
body2 = Body("Moon", x=np.array([384400e3, 0.0, 0.0]), v=np.array([0.0, 1022.0, 0.0]), mass=7.348e22)
body3 = Body("Moon2", x=np.array([384400e3*2, 0.0, 0.0]), v=np.array([0.0, 400.0, 0.0]), mass=7.348e21)

bodies = [body1, body2, body3]
dt = 30000  # seconds
time = np.arange(0, 365*24*3600, dt)  # 30 days

for i, t in enumerate(time):
    update_bodies(bodies, dt)

fig, ax = plt.subplots(figsize=(8, 8))

ax.set_aspect('equal', 'box')

earth, = ax.plot([], [], color='blue', marker='o', label='Earth')
moon, = ax.plot([], [], color='green', marker='o', label='Moon')
planet, = ax.plot([], [], color='orange', marker='o', label='Moon2')
trajectory_earth, = ax.plot([], [], 'b-', lw=1)
trajectory_moon, = ax.plot([], [], 'g-', lw=1)
trajectory_planet, = ax.plot([], [], color='orange', ls='-', lw=1)

ax.legend()

def init():
    earth.set_data([], [])
    moon.set_data([], [])
    planet.set_data([], [])
    trajectory_earth.set_data([], [])
    trajectory_moon.set_data([], [])
    trajectory_planet.set_data([], [])
    return earth, moon, planet, trajectory_earth, trajectory_moon, trajectory_planet

def animate(i):
    earth.set_data([body1.x[i, 0]], [body1.x[i, 1]])
    moon.set_data([body2.x[i, 0]], [body2.x[i, 1]])
    planet.set_data([body3.x[i, 0]], [body3.x[i, 1]])
    trajectory_earth.set_data(body1.x[:i, 0], body1.x[:i, 1])
    trajectory_moon.set_data(body2.x[:i, 0], body2.x[:i, 1])
    trajectory_planet.set_data(body3.x[:i, 0], body3.x[:i, 1])

    ax.set_xlim(body1.x[i, 0] - 10e8, body1.x[i, 0] + 10e8)
    ax.set_ylim(body1.x[i, 1] - 10e8, body1.x[i, 1] + 10e8)
    return earth, moon, planet, trajectory_earth, trajectory_moon, trajectory_planet

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(time), interval=10, blit=True)

plt.show()