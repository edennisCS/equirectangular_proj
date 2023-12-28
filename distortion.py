from PIL import Image
import math

# Function to convert Cartesian coordinates to equirectangular
def cartesian_to_equirectangular(x, y, z):
    lon = math.degrees(math.atan2(x, y))
    lat = math.degrees(math.asin(min(max(z / math.sqrt(x**2 + y**2 + z**2), -1), 1)))
    return lon, lat

image = Image.open("path/to/image.jpg")
new_size = (2000, 1000)
resized_image = image.resize(new_size)

# Set image size
width, height = new_size

# Store coordinates
pixel_coordinates = []

# Loop through the pixels
for y in range(height):
    for x in range(width):
        # Print coordinates
        print(f"Coordinates: ({x}, {y})")