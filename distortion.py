from PIL import Image
import numpy as np
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt

from src.cube import Cube
from src.panel import Panel


def cartesian_to_equirectangular(coordinate):
    """

    :param coordinate:
    :return: np.array([lon, lat])
    """
    lon = np.degrees(np.arctan2(coordinate[0], coordinate[2]))
    lat = np.degrees(np.arcsin(
        np.clip(coordinate[1] / np.sqrt(coordinate[0] ** 2 + coordinate[1] ** 2 + coordinate[2] ** 2), -1, 1)))
    return np.array([lon, lat])


def apply_rotational_transformation(coordinate, angle):
    """

    :param coordinate:
    :param angle:
    :return: rotated_coordinate
    """
    rotation_matrix = Rotation.from_euler('zxy', np.array([angle]), degrees=True)
    rotated_coordinate = rotation_matrix.apply(coordinate).flatten()
    return rotated_coordinate


def apply_translation_transformation(coordinate, translation):
    """

    :param coordinate:
    :param translation:
    :return: coordinate + translation

    """
    return coordinate + translation


def generate_coordinates(panel):
    """

    :param panel:
    :return: coordinates
    """
    x_initial = np.linspace(-panel.width / 2, panel.width / 2, 50)
    y_initial = np.linspace(0, 0, 50)
    z_initial = np.linspace(-panel.width / 2, panel.height / 2, 50)

    x_grid, y_grid, z_grid = np.meshgrid(x_initial, y_initial, z_initial)
    coordinates = np.column_stack((x_grid.ravel(), y_grid.ravel(), z_grid.ravel()))
    return coordinates


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


def plot_panels(panels):
    """

    :param panels:
    """
    plt.figure(figsize=(20, 10))

    for panel in panels:
        coordinates = generate_coordinates(panel)
        equi_coordinates = apply_transformations(coordinates, panel.angle, panel.position)

        lon = equi_coordinates[:, 0]
        lat = equi_coordinates[:, 1]
        plt.scatter(lon, lat, marker='.', label='Cube Map', c=panel.image_path)

    plt.axis('off')
    plt.ylim([-90, 90])
    plt.xlim([-180, 180])
    plt.margins(0)
    plt.savefig('image.png', bbox_inches='tight', pad_inches=0)
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

plot_panels(panels)
