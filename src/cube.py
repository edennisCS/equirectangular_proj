from src.tesselation import Tesselation
from src.panel import Panel

class Cube(Tesselation):
  face_geometry = "SQUARE"

  # 6 sides of a cube
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
