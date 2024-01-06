from PIL import Image
import numpy as np
from src.cube import Cube
from src.panel import Panel
import matplotlib.pyplot as plt


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
image_path = "images/example1.png"
new_size = (300, 300)
resized_image = Image.open(image_path).resize(new_size)

# Set image size
width, height = new_size

x = np.linspace(0, 10, width)
y = np.linspace(0, 10, height)
x, y = np.meshgrid(x, y)

distorted_x, distorted_y = generate_distorted_mesh_grid(x, y)

# Panel
panel = Panel(image_path, [0, -1, 0], [0, 0, 0], 2, 2)
panel.render(plt)

# images = [f"images/example{i}.png" for i in range(1, 7)]
# cube = Cube(images)
# cube.render(plt)

plt.figure(figsize=(10, 10))
plt.pcolormesh(distorted_x, distorted_y, np.array(resized_image))
plt.plot(distorted_x, distorted_y, ".k", markersize=1)  # Points on top
plt.show()

# Can we refactor the above code to use newly created objects
# for development first try rendering single panel
# panel = Panel("images/example1.png", [0, -1, 0], [0, 0, 0], 2, 2)
# panel.render(plt)

# Then we can move on to the cube
# images = ["images/example1.png", "images/example2.png", "images/example3.png", "images/example4.png", "images/example5.png", "images/example6.png"]
# cube = Cube(images)
# cube.render(plt)

# plt.figure(figsize=(10, 10))
# plt.pcolormesh(distorted_x, distorted_y, np.array(resized_image))
# plt.plot(distorted_x, distorted_y, ".k", markersize=1)  # Points on top
# plt.show()
