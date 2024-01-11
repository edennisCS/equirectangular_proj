from PIL import Image
import numpy as np
from scipy.spatial.transform import Rotation

from src.cube import Cube
from src.panel import Panel
import matplotlib.pyplot as plt
import scipy



def cartesian_to_equirectangular(x, y, z):
    lon = np.degrees(np.arctan2(x, y))
    lat = np.degrees(np.arcsin(z / np.sqrt(x**2 + y**2 + z**2)))
    return lon, lat

# the order is z, x, y
def generate_cartesian_mesh_grid(x, y, z, angle, position):
    # rotation on 3 axis
    # rotation around z, define the rotation matrix
    # rotation around x, "
    # rotation around y, "
    # translate position, move to the position
    rotation_matrix = Rotation.from_euler('zxy', np.array([angle]))

    mult = rotation_matrix.apply(np.array([x.ravel(), y.ravel(), z.ravel()]).transpose())
    xrot = mult[:, 0]
    yrot = mult[:, 1]
    zrot = mult[:, 2]

    cartesian_x, cartesian_y, cartesian_z = xrot + position[0], yrot + position[1], zrot + position[2]
    return cartesian_x, cartesian_y, cartesian_z


# Plot figure plt width 2000 height 1000

plt.figure(figsize=(2000, 1000))
panel = Panel("images/example1.png", [0, 0, 0], [0, -1, 0], 2, 2)

x_initial = np.linspace(-panel.width/2, panel.width/2, 100)
y_initial = np.linspace(0, 0, 100)
z_initial = np.linspace(-panel.width/2, panel.height/2, 100)

x_untransformed, y_untransformed, z_untransformed = np.meshgrid(x_initial, y_initial, z_initial)

cart_x, cart_y, cart_z = generate_cartesian_mesh_grid(x_initial, y_initial, z_initial, panel.angle, panel.position)
print(cart_x, cart_y, cart_z)
cartesian_to_equirectangular(cart_x, cart_y, cart_z)
lon, lat = cartesian_to_equirectangular(cart_x, cart_y, cart_z)
print(lon, lat)
plt.pcolormesh(lon, lat, np.array(Image.open(panel.image_path).resize((100, 100))))
plt.show()












