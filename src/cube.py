from src.tesselation import Tesselation

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
              'angle': [90, 180, 0],
              'width': 2,
              'height': 2
          },
          {
              'position': [0, 0, -1],
              'angle': [90, 0, 0],
              'width': 2,
              'height': 2
          }
  ]
