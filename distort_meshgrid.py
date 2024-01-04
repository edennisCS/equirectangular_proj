from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Function to convert Cartesian coordinates to equirectangular
def cartesian_to_equirectangular(x, y, z):
    lon = np.degrees(np.arctan2(x, y))
    lat = np.degrees(np.arcsin(np.clip(z / np.sqrt(x**2 + y**2 + z**2), -1, 1)))
    return lon, lat

# Placeholder formula for the distortion we will want to use equirectangular one
def generate_distorted_mesh_grid(x, y):
    distortion_factor = 0.2
    distorted_x = x + distortion_factor * np.sin(y)
    distorted_y = y + distortion_factor * np.cos(x)
    return distorted_x, distorted_y

# Loading up an image
image = Image.open("dwswes.png")
new_size = (300, 300)
resized_image = image.resize(new_size)

# Set image size
width, height = new_size

x = np.linspace(0, 10, width)
y = np.linspace(0, 10, height)
x, y = np.meshgrid(x, y)


distorted_x, distorted_y = generate_distorted_mesh_grid(x, y)

plt.figure(figsize=(10, 10))
plt.pcolormesh(distorted_x, distorted_y, np.array(resized_image))
plt.plot(distorted_x, distorted_y, ".k", markersize=1)  # Points on top
plt.show()