from dynamics import *
import plotly.graph_objects as go
from plotting import *
from astropy.coordinates import get_sun
from astropy.time import Time
import astropy.units as u
from astropy.coordinates import get_body

# Define the list of planets
planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

# Get the current time
now = Time.now()

# Use a dictionary to store the coordinates
coordinates = {}

# Set the solar system ephemeris to 'builtin' for convenience

for planet in planets:
    # Get the body coordinates
    body_coords = get_body(planet, now)
    
    # Store the coordinates in meters
    coordinates[planet] = [
        body_coords.cartesian.x.to(u.m).value,
        body_coords.cartesian.y.to(u.m).value,
        body_coords.cartesian.z.to(u.m).value
    ]

# Define solar system bodies
sun = Body("Sun", x=np.array([0.0, 0.0, 0.0]), v=np.array([0.0, 0.0, 0.0]), mass=1.989e30)
mercury = Body("Mercury", x=np.array(coordinates["mercury"]), v=np.array([0.0, 47.36e3, 0.0]), mass=3.285e23)
venus = Body("Venus", x=np.array(coordinates["venus"]), v=np.array([0.0, 35.02e3, 0.0]), mass=4.867e24)
earth = Body("Earth", x=np.array(coordinates["earth"]), v=np.array([0.0, 29.78e3, 0.0]), mass=5.972e24)
mars = Body("Mars", x=np.array(coordinates["mars"]), v=np.array([0.0, 24.077e3, 0.0]), mass=6.39e23)
jupiter = Body("Jupiter", x=np.array(coordinates["jupiter"]), v=np.array([0.0, 13.07e3, 0.0]), mass=1.898e27)
saturn = Body("Saturn", x=np.array(coordinates["saturn"]), v=np.array([0.0, 9.68e3, 0.0]), mass=5.683e26)
uranus = Body("Uranus", x=np.array(coordinates["uranus"]), v=np.array([0.0, 6.8e3, 0.0]), mass=8.681e25)
neptune = Body("Neptune", x=np.array(coordinates["neptune"]), v=np.array([0.0, 5.43e3, 0.0]), mass=1.024e26)

bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
dt = 10*86400  # 10x one day in seconds
time = np.arange(0, 10*365*24*3600, dt)  # simulate ten years

# Update the positions of all bodies over time
for i, t in enumerate(time):
    update_bodies(bodies, dt)

plot_bodies_animated(bodies)

