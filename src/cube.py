from src.tesselation import Tesselation
from src.panel import Panel

class Cube(Tesselation):
  panel_configuration = [
          {
              'position': [0, -1, 0],
              'angle': [0, 0, 0],
              'width': 2,
              'height': 2
          },
          {
              'position': [0, 1, 0],
              'angle': [180, 0, 0],
              'width': 2,
              'height': 2
          },
          {
              'position': [1, 0, 0],
              'angle': [90, -90, 0],
              'width': 2,
              'height': 2
          },
          {
              'position': [-1, 0, 0],
              'angle': [90, 90, 0],
              'width': 2,
              'height': 2
          },
          {
              'position': [0, 0, 1],
              'angle': [0, 90, 0],
              'width': 2,
              'height': 2
          },
          {
              'position': [0, 0, -1],
              'angle': [0, 90, 0],
              'width': 2,
              'height': 2
          }
  ]
  def __init__(self):
      super().__init__()
      self.panels = [Panel(colour, config['position'], config['angle'], config['width'], config['height'])
                       for colour, config in zip(['r', 'g', 'b', 'b', 'y', 'y'], self.panel_configuration)]
