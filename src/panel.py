class Panel:
  def __init__(self, image_path, angle, position, width, height):
    self.image_path = image_path
    self.angle = angle
    self.position = position
    self.width = width
    self.height = height

  def render(self, plot):
    print(self.image_path)
    print(self.angle)
    print(self.position)
    print(self.width)
    print(self.height)
    # add steps for rendering panel
