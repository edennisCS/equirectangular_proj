class Panel:
  def __init__(self, image_path, angle, position, width, height):
    self.image_path = image_path
    self.angle = angle
    self.position = position
    self.width = width
    self.height = height

  def cartesian_to_equirectangular(x, y, z):
    lon = np.degrees(np.arctan2(x, y))
    lat = np.degrees(np.arcsin(np.clip(z / np.sqrt(x**2 + y**2 + z**2), -1, 1)))
    return lon, lat

  def generate_cartesian_meshgrid(self):
    # place holder for cartesian meshgrid generation
    print('will generate cartesian meshgrid')

  def generate_equirectangular_meshgrid(self):
    # convert cartesian meshgrid to equirectangular
    print('will generate equirectangular meshgrid')

  def render_equirectangular_meshgrid(self, plot):
    # render equirectangular meshgrid to plot
    print('will generate equirectangular meshgrid')

  def render(self, plot):
    print(self.image_path)
    print(self.angle)
    print(self.position)
    print(self.width)
    print(self.height)
    # add steps for rendering panel
    self.generate_cartesian_meshgrid()
    self.generate_equirectangular_meshgrid()
    self.render_equirectangular_meshgrid(plot)
