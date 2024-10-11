from dynamics import *
import plotly.graph_objects as go
from plotting import *
from astropy.coordinates import get_sun
from astropy.time import Time, TimeDelta
import astropy.units as u
from astropy.coordinates import get_body

# Define the list of planets
planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

# Get the current time
now = Time.now()
dt = TimeDelta(1 * u.hour)

# Use a dictionary to store the coordinates
coordinates = {}
velocities = {}

# Get the Sun's position at the current time
sun_coords = get_sun(now)

for planet in planets:
    # Get the planet's position at time 'now' and 'now - dt'
    body_coords_now = get_body(planet, now)
    body_coords_past = get_body(planet, now - dt)

    # Calculate the position relative to the Sun at both time intervals
    relative_coords_now = body_coords_now.cartesian - sun_coords.cartesian
    relative_coords_past = body_coords_past.cartesian - get_sun(now - dt).cartesian
    
    # Store the current position in meters
    coordinates[planet] = [
        relative_coords_now.x.to(u.m).value,
        relative_coords_now.y.to(u.m).value,
        relative_coords_now.z.to(u.m).value
    ]
    
    # Calculate velocity as (position_now - position_past) / dt
    velocity_vector = (relative_coords_now - relative_coords_past) / dt
    
    # Store the velocity in meters per second
    velocities[planet] = [
        velocity_vector.x.to(u.m/u.s).value,
        velocity_vector.y.to(u.m/u.s).value,
        velocity_vector.z.to(u.m/u.s).value
    ]

# Define solar system bodies
sun = Body("Sun", x=np.array([0.0, 0.0, 0.0]), v=np.array([0.0, 0.0, 0.0]), mass=1.989e30)
mercury = Body("Mercury", x=np.array(coordinates["mercury"]), v=np.array(velocities["mercury"]), mass=3.285e23)
venus = Body("Venus", x=np.array(coordinates["venus"]), v=np.array(velocities["venus"]), mass=4.867e24)
earth = Body("Earth", x=np.array(coordinates["earth"]), v=np.array(velocities["earth"]), mass=5.972e24)
mars = Body("Mars", x=np.array(coordinates["mars"]), v=np.array(velocities["mars"]), mass=6.39e23)
jupiter = Body("Jupiter", x=np.array(coordinates["jupiter"]), v=np.array(velocities["jupiter"]), mass=1.898e27)
saturn = Body("Saturn", x=np.array(coordinates["saturn"]), v=np.array(velocities["saturn"]), mass=5.683e26)
uranus = Body("Uranus", x=np.array(coordinates["uranus"]), v=np.array(velocities["uranus"]), mass=8.681e25)
neptune = Body("Neptune", x=np.array(coordinates["neptune"]), v=np.array(velocities["neptune"]), mass=1.024e26)


bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
dt = 10*86400  # 10x one day in seconds
time = np.arange(0, 10*365*24*3600, dt)  # simulate ten years

# Update the positions of all bodies over time
for i, t in enumerate(time):
    update_bodies(bodies, dt)

plot_bodies_animated(bodies)

