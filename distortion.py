import numpy as np
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt
import matplotlib.path as mpath

from src.panel import Panel

PANEL_RESOLUTION=50
PLOT_WIDTH=20
PLOT_HEIGHT=10

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
def apply_rotational_transformation(coordinate, rotation_matrix):
    """

    :param coordinate:
    :param angle:
    :return: rotated_coordinate
    """

    return rotation_matrix.apply(coordinate).flatten()

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

    # Create initial meshgrid in xz plane with panel width and height
    x_initial = np.linspace(-panel.width / 2, panel.width / 2,  PANEL_RESOLUTION)
    z_initial = np.linspace(-panel.height / 2, panel.height / 2, PANEL_RESOLUTION)

    # Convert meshgrid into coordinate array
    x_grid, z_grid = np.meshgrid(x_initial, z_initial)
    grid_array = np.column_stack((x_grid.ravel(), z_grid.ravel()))

    # Cut meshgrid into triangle if tessellation has triangular geometry
    cut_grid_array = cut_meshgrid_to_triangle(grid_array, panel) if face_geometry == "TRIANGLE" else grid_array 

    # Insert zero value for Y coordinate in all coordinates
    coordinates = np.insert(cut_grid_array, 1, 0, axis=1)
    return coordinates

# Function to cut a meshgrid to tessellation's face triangle geometry
def cut_meshgrid_to_triangle(points, panel):
   """

   :param points:
   :param panel:
   :return: points[points_mask]
   """
 
   # create path around triangle with width and height of panel
   polygon_path = triangle_vertex_path(panel.width, panel.height)

   # create mask to remove all coordinates outside triangle
   points_mask = polygon_path.contains_points(points)

   # filter points to those within triangle
   return points[points_mask]

# Function to generate vertex path of an equilateral triangle
def triangle_vertex_path(width, height):
    """

    :param width:
    :param height:
    :return: mpath.Path(polygon_vertices)
    """

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

    # Apply Euler rotations to rotate coordinates to angle of the panel 
    rotation_matrix = Rotation.from_euler('zxy', np.array([angle]), degrees=True)
    rotated_coordinates = np.apply_along_axis(apply_rotational_transformation, axis=1, arr=coordinates, rotation_matrix=rotation_matrix)

    # Translate coordinates to position of the panel
    transformed_coordinates = np.apply_along_axis(apply_translation_transformation, axis=1, arr=rotated_coordinates,
                                                  translation=translation)

    # Generate equirectangular coordinates from cartesian
    equi_coordinates = np.apply_along_axis(cartesian_to_equirectangular, axis=1, arr=transformed_coordinates)
    return equi_coordinates

# The main logic of plotting the panels
def plot_panels(panels, face_geometry):
    """

    :param panels:
    :param face_geometry:
    """
    plt.figure(figsize=(PLOT_WIDTH, PLOT_HEIGHT))

    for panel in panels:
        # Generate initial untransformed coordinates of panel
        coordinates = generate_coordinates(panel, face_geometry)

        # Transform coordinates to equirectangular
        equi_coordinates = apply_transformations(coordinates, panel.angle, panel.position)

        # Plot coordinates to graph with panel colour
        lon = equi_coordinates[:, 0]
        lat = equi_coordinates[:, 1]
        plt.scatter(lon, lat, marker='.', label='Cube Map', c=panel.colour)

    # remove avis from rendering
    plt.axis('off')

    # Axis range equal to range of equirectangular coordinates
    plt.ylim([-90, 90])
    plt.xlim([-180, 180])

    # Remove margins to generate equirectangular 
    plt.margins(0)

    # Save a rendering of equirectangular
    plt.savefig('equirectangular.png', bbox_inches='tight', pad_inches=0)
    plt.show()

# Produces one iteration of sierpinksi gasket tessellation of panels
def sierpinski_triangle_panel_iteration(panels):
    """

    :param panels:
    :return: generated_panels
    """

    # Empty list of new panels
    generated_panels = []

    for panel in panels:
        # Displacement of centre points of panels in next iteration from original panel centre point
        centre_displacements = np.array([[0, 0, (1/2)*panel.height/2.75], [panel.width/4, 0, -panel.height/8], [-panel.width/4, 0, -panel.height/8]])
        # Transform displacements along the orientation of the panel 
        rotated_displacements = np.apply_along_axis(apply_rotational_transformation, axis=1, arr=centre_displacements, angle=panel.angle)

        # Initialise new panel for each displacement scaled by 1/2 
        for displacement in transformed_displacements:
            generated_panels.append(Panel(panel.colour, panel.angle, panel.position + displacement, panel.width/2, panel.height/2))

    return generated_panels
