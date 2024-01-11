from PIL import Image
import numpy as np
from src.cube import Cube
from src.panel import Panel
import matplotlib.pyplot as plt


# Plot figure plt width 2000 height 1000


# Define our panel (instantiate panel)


# Do a function to create a mesh grid from that panel - flat to start


# Then transform to cartesian space at the angle of object


# Then equirectangular point is the same, 






# Function to convert Cartesian coordinates to equirectangular
def cartesian_to_equirectangular(x, y, z):
    lon = np.degrees(np.arctan2(x, y))
    lat = np.degrees(np.arcsin(np.clip(z / np.sqrt(x**2 + y**2 + z**2), -1, 1)))
    return lon, lat

# Placeholder formula for the distortion use equirectangular later
def generate_distorted_mesh_grid(x, y):
    distortion_factor = 0.2
    distorted_x = x + distortion_factor * np.sin(y)
    distorted_y = y + distortion_factor * np.cos(x)
    return distorted_x, distorted_y

# Loading up an image
images = ["images/example1.png", "images/example2.png", "images/example3.png", "images/example4.png",
          "images/example5.png", "images/example6.png"]
new_size = (300, 300)

# Set image size
width, height = new_size

x = np.linspace(0, 10, width)
y = np.linspace(0, 10, height)
x, y = np.meshgrid(x, y)

distorted_x, distorted_y = generate_distorted_mesh_grid(x, y)

# Panel
# panel = Panel(image_path, [0, -1, 0], [0, 0, 0], 2, 2)
# panel.render(plt)

# Create a Cube object
images = ["images/example1.png", "images/example2.png", "images/example3.png", "images/example4.png", "images/example5.png", "images/example6.png"]
cube = Cube(images)



panel = Panel("images/example1.png",  [0, 0, 0], [0, -1, 0], 2, 2)
panel.render(plt)

resized_distorted_image = Image.open(images[0]).resize(new_size)
plt.figure(figsize=(10, 10))
plt.pcolormesh(distorted_x, distorted_y, np.array(Image.open(images[0]).resize(new_size)))
plt.plot(distorted_x, distorted_y, ".k", markersize=1)  # Points on top
plt.show()

# for i, panel_config in enumerate(cube.panel_configuration):
#     panel = Panel(images[i], panel_config['angle'], panel_config['position'], panel_config['width'], panel_config['height'])
#     panel.render(plt)
#
#     resized_distorted_image = Image.open(images[0]).resize(new_size)
#     plt.figure(figsize=(10, 10))
#     plt.pcolormesh(distorted_x, distorted_y, np.array(Image.open(images[0]).resize(new_size)))
#     plt.plot(distorted_x, distorted_y, ".k", markersize=1)  # Points on top
#     plt.show()





