from PIL import Image
import numpy as np
from scipy.spatial.transform import Rotation

from src.cube import Cube
from src.panel import Panel
import matplotlib.pyplot as plt
import scipy


# the order is z, x, y
def generate_cartesian_mesh_grid(x, y, z, angle, position):
    # rotation on 3 axis
    # rotation around z, define the rotation matrix
    # rotation around x, "
    # rotation around y, "
    # translate position, move to the position
    rotation_matrix = Rotation.from_euler('zxy', np.array([angle]))

    # apply rotation
    coordinates = np.vstack((x.flatten(), y.flatten(), z.flatten()))
    rotated_coords = rotation_matrix.apply(coordinates)
    cartesian_x, cartesian_y, cartesian_z = rotated_x + position[0], rotated_y + position[0], rotated_z + position[0]
    return cartesian_x, cartesian_y, cartesian_z


# Plot figure plt width 2000 height 1000

plt.figure(figsize=(2000, 1000))
panel = Panel("images/example1.png", [0, 0, 0], [0, -1, 0], 2, 2)

x_initial = np.linspace(0, panel.width, 100)
y_initial = np.linspace(0, panel.height, 100)
z_initial = 0

x_untransformed, y_untransformed, z_untransformed = np.meshgrid(x_initial, y_initial, z_initial)

cart_x, cart_y, cart_z = generate_cartesian_mesh_grid(x_initial, y_initial, z_initial, panel.angle, panel.position)
print(cart_x, cart_y, cart_z)









