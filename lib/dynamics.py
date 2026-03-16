import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from astropy.constants import R_earth
from planets import *

class Body():
    """Defines a body with position x, velocity v, mass m, and acceleration a."""
    def __init__(self, name, x=np.random.random(3), v=np.zeros(3, dtype=float), 
                 a=np.zeros(3, dtype=float), mass=1.0):
        if not isinstance(name, str):
            raise TypeError(f"Expected name to be str, got {type(name)} instead")
        if not isinstance(x, np.ndarray):
            raise TypeError(f"Expected x to be np.ndarray, got {type(x)} instead")
        if not isinstance(v, np.ndarray):
            raise TypeError(f"Expected v to be np.ndarray, got {type(v)} instead")
        if not isinstance(mass, float):
            raise TypeError(f"Expected mass to be float, got {type(mass)} instead")

        self.name = name
        self.x = np.reshape(x, (1, 3))
        self.v = np.reshape(v, (1, 3))
        self.mass = mass
        self.a = np.zeros((1,3))
        self.force = np.zeros(3)

    def calculate_force(self, other_bodies):
        """Calculates the gravitational force exerted by other bodies."""
        G = 6.67430e-11  # gravitational constant
        self.force.fill(0)  # Reset force to zero
        for other in other_bodies:
            if other is not self:
                r_vec = other.x[-1] - self.x[-1]
                r_mag = np.linalg.norm(r_vec)
                if r_mag != 0:
                    force_magnitude = G * self.mass * other.mass / r_mag**2
                    self.force += force_magnitude * r_vec / r_mag

    def update_acceleration(self):
        """Updates acceleration based on the current force."""

        self.a = np.vstack((self.a, self.force / self.mass))


class Jet(Body):
    def __init__(self, name, x, v, mass):
        super().__init__(name, x, v, mass)
        self.thrust_history = []

    def apply_thrust(self, thrust_vector):
        self.force += thrust_vector
        self.thrust_history.append(thrust_vector)

    def enforce_surface_constraint(self, planet):
        """
        Prevent the jet from collapsing into the planet's center by enforcing
        a minimum distance equal to the planet's radius.
        """
        r_vec = self.x[-1] - planet.x[-1]
        r_mag = np.linalg.norm(r_vec)
        if r_mag < R_earth.value:
            # Project the jet back to the Earth's surface
            self.x[-1] = planet.x[-1] + r_vec / r_mag * R_earth.value
            self.v[-1] = np.zeros(3)  # Optionally reset velocity to zero

def update_bodies(bodies, dt, earth):
    for body in bodies:
        body.calculate_force(bodies)
        if isinstance(body, Jet):
            body.apply_thrust([0, 0, 0])
        body.update_acceleration()

    for body in bodies:
        new_x = body.x[-1] + body.v[-1] * dt + 0.5 * body.a[-1] * dt**2
        body.x = np.vstack((body.x, new_x))

    for body in bodies:
        body.calculate_force(bodies)

    for body in bodies:
        new_a = body.force / body.mass
        new_v = body.v[-1] + 0.5 * (body.a[-1] + new_a) * dt
        body.v = np.vstack((body.v, new_v))
        body.a = np.vstack((body.a, new_a))

    # Enforce surface constraint for jets
    for body in bodies:
        if isinstance(body, Jet):
            body.enforce_surface_constraint(earth)

def orthogonal_unit_vector(v):
    # Ensure the input is a numpy array
    v = np.array(v)
    
    # Check the dimension of the vector
    if len(v) != 3:
        raise ValueError("This method only works for 3-dimensional vectors.")
    
    # Choose a random vector that is not parallel to v
    # A good strategy is to pick a vector with one element different from v's elements.
    if np.allclose(v, [1, 0, 0]):
        random_vec = np.array([0, 1, 0])  # If v is along x-axis, choose y-axis
    else:
        random_vec = np.array([1, 0, 0])  # Default random vector
    
    # Compute the cross product (gives a vector orthogonal to both v and random_vec)
    orthogonal_vec = np.cross(v, random_vec)
    
    # Normalize the orthogonal vector to make it a unit vector
    orthogonal_unit_vec = orthogonal_vec / np.linalg.norm(orthogonal_vec)
    
    return orthogonal_unit_vec