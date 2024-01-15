from src.tesselation import Tesselation
from src.panel import Panel
import numpy as np

class Octohedron(Tesselation):
  face_geometry = "TRIANGLE" 

  panel_configuration = [
          {
              'position': [1, 1, 1],
              'angle': [0, 225, 45],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [-1, 1, 1],
              'angle': [0, 225, -45],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [1, -1, 1],
              'angle': [0, -225, 45],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [1, 1, -1],
              'angle': [0, 225, 135],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [1, -1, -1],
              'angle': [0, -225, 135],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [-1, 1, -1],
              'angle': [0, 225, -135],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [-1, -1, 1],
              'angle': [0, -225, -45],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [-1, -1, -1],
              'angle': [0, -225, -135],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          }
  ]
