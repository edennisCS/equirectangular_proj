import numpy as np
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt
import matplotlib.path as mpath

from src.cube import Cube
from src.octohedron import Octohedron
from src.panel import Panel

# Function to convert Cartesian coordinates to equirectangular
def cartesian_to_equirectangular(coordinate):
    """

    :param coordinate:
    :return: np.array([lon, lat])
    """
    lon = np.degrees(np.arctan2(coordinate[0], coordinate[2]))
    lat = np.degrees(np.arcsin(
        np.clip(coordinate[1] / np.sqrt(coordinate[0] ** 2 + coordinate[1] ** 2 + coordinate[2] ** 2), -1, 1)))
    return np.array([lon, lat])

# Function to return the rotated coordinates using euler
def apply_rotational_transformation(coordinate, angle):
    """

    :param coordinate:
    :param angle:
    :return: rotated_coordinate
    """
    rotation_matrix = Rotation.from_euler('zxy', np.array([angle]), degrees=True)
    rotated_coordinate = rotation_matrix.apply(coordinate).flatten()
    return rotated_coordinate

# Function to apply translation
def apply_translation_transformation(coordinate, translation):
    """

    :param coordinate:
    :param translation:
    :return: coordinate + translation

    """
    return coordinate + translation

# Function to generate coordinates using panel
def generate_coordinates(panel, face_geometry):
    """

    :param panel:
    :return: coordinates
    """
    x_initial = np.linspace(-panel.width / 2, panel.width / 2, 50)
    z_initial = np.linspace(-panel.height / 2, panel.height / 2, 50)

    x_grid, z_grid = np.meshgrid(x_initial, z_initial)
    grid_array = np.column_stack((x_grid.ravel(), z_grid.ravel()))

    cut_grid_array = cut_meshgrid_to_triangle(grid_array, panel) if face_geometry == "TRIANGLE" else grid_array 
    coordinates = np.insert(cut_grid_array, 1, 0, axis=1)
    return coordinates

# Function to cut a meshgrid to tesselation's face triangle geometry
def cut_meshgrid_to_triangle(points, panel):
   polygon_path = triangle_vertex_path(panel.width, panel.height)
   points_mask = polygon_path.contains_points(points)

   return points[points_mask]

# Function to get the path of a polygon for a type of face geometryy
def triangle_vertex_path(width, height):
    polygon_vertices = np.array([[-width/2, -height/4], [width/2, -height/4], [0, height/2.85]])

    return mpath.Path(polygon_vertices)

# Function to apply transforms onto the coordinates
def apply_transformations(coordinates, angle, translation):
    """

    :param coordinates:
    :param angle:
    :param translation:
    :return: equi_coordinates
    """
    rotated_coordinates = np.apply_along_axis(apply_rotational_transformation, axis=1, arr=coordinates, angle=angle)
    transformed_coordinates = np.apply_along_axis(apply_translation_transformation, axis=1, arr=rotated_coordinates,
                                                  translation=translation)
    equi_coordinates = np.apply_along_axis(cartesian_to_equirectangular, axis=1, arr=transformed_coordinates)
    return equi_coordinates

# The main logic of plotting the panels
def plot_panels(panels, face_geometry):
    """

    :param panels:
    """
    plt.figure(figsize=(20, 10))

    for panel in panels:
        coordinates = generate_coordinates(panel, face_geometry)
        equi_coordinates = apply_transformations(coordinates, panel.angle, panel.position)

        lon = equi_coordinates[:, 0]
        lat = equi_coordinates[:, 1]
        plt.scatter(lon, lat, marker='.', label='Cube Map')

    plt.axis('off')
    plt.ylim([-90, 90])
    plt.xlim([-180, 180])
    plt.margins(0)
    plt.savefig('equirectangular.png', bbox_inches='tight', pad_inches=0)
    plt.show()


# Main script
panels = [
    Panel("r", [0, 0, 0], [0, -1, 0], 2, 2),
    Panel("g", [180, 0, 0], [0, 1, 0], 2, 2),
    Panel("b", [90, -90, 0], [1, 0, 0], 2, 2),
    Panel("b", [90, 90, 0], [-1, 0, 0], 2, 2),
    Panel("y", [0, 90, 0], [0, 0, 1], 2, 2),
    Panel("y", [0, 90, 0], [0, 0, -1], 2, 2)
]

cube_instance = Cube(colours=['r', 'g', 'b', 'b', 'y', 'y', 'r', 'r'])

for panel in cube_instance.panels:
    print(f"Colour {panel.colour} Position: {panel.position}, Angle: {panel.angle}, Width: {panel.width}, Height: {panel.height}")

# plot_panels(panels)
plot_panels(cube_instance.panels, cube_instance.face_geometry)
