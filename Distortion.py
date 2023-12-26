from PIL import Image

image = Image.open("path/to/image.jpg")
new_size = (2000, 1000)
resized_image = image.resize(new_size)
