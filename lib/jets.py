from dynamics import *
from planets import *
from astropy.constants import R_earth

jetson = Jet('jetty', x=earth.x + np.array([R_earth.value, 0, 0]), v=np.zeros(3), mass=1000)

bodies.append(jetson)
