from PIL import Image
import numpy as np
from scipy.spatial.transform import Rotation

from src.cube import Cube
from src.panel import Panel
import matplotlib.pyplot as plt
import scipy

def cartesian_to_equirectangular(coordinate):
    lon = np.degrees(np.arctan2(coordinate[0], coordinate[2]))
    lat = np.degrees(np.arcsin(np.clip(coordinate[1]/ np.sqrt(coordinate[0]**2 + coordinate[1]**2 + coordinate[2]**2), -1, 1)))

    return np.array([lon, lat])

def generate_distorted_mesh_grid(x, y):
    distortion_factor = 0.2
    distorted_x = x + distortion_factor * np.sin(y)
    distorted_y = y + distortion_factor * np.cos(x)
    return distorted_x, distorted_y

def apply_rotational_transformation(coordinate, angle):
    rotation_matrix = Rotation.from_euler('zxy', np.array([angle]), degrees=True)
    rotated_coordinate = rotation_matrix.apply(coordinate).flatten()
    return rotated_coordinate 

def apply_translation_transformation(coordinate, translation):
    return coordinate + translation

# Plot figure plt width 2000 height 1000

plt.figure(figsize=(20, 10))

panels = [
    Panel("r", [0, 0, 0], [0, -1, 0], 2, 2),
    Panel("g", [180, 0, 0], [0, 1, 0], 2, 2),
    Panel("b", [90, -90, 0], [1, 0, 0], 2, 2),
    Panel("b", [90, 90, 0], [-1, 0, 0], 2, 2),
    Panel("y", [0, 90, 0], [0, 0, 1], 2, 2),
    Panel("y", [0, 90, 0], [0, 0, -1], 2, 2)
]

cube_instance = Cube()

# # Accessing panels in the list
# for panel in panels:

for panel in panels:
    x_initial = np.linspace(-panel.width/2, panel.width/2, 50)
    y_initial = np.linspace(0, 0, 50)
    z_initial = np.linspace(-panel.width/2, panel.height/2, 50)

    x_grid, y_grid, z_grid = np.meshgrid(x_initial, y_initial, z_initial)

    coordinates = np.column_stack((x_grid.ravel(), y_grid.ravel(), z_grid.ravel()))

    rotated_coordinates = np.apply_along_axis(apply_rotational_transformation, axis=1, arr=coordinates, angle=panel.angle)
    transformed_coordinates = np.apply_along_axis(apply_translation_transformation, axis=1, arr=rotated_coordinates, translation=panel.position)
    equi_coordinates = np.apply_along_axis(cartesian_to_equirectangular, axis=1, arr=transformed_coordinates)

    lon = equi_coordinates[:, 0]
    lat = equi_coordinates[:, 1]
    plt.scatter(lon, lat, marker='.', label='Cube Map', c=panel.image_path)

plt.axis('off')
plt.ylim([-90, 90])
plt.xlim([-180, 180])
plt.margins(0)
plt.savefig('image.png', bbox_inches='tight', pad_inches=0)
plt.show()
