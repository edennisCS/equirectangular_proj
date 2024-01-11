from src.panel import Panel

class Tesselation:
  def __init__(self, image_paths):
      for config in self.panel_configuration:
        self.panels = map(self.createPanel, self.panel_configuration, image_paths)

  def createPanel(_self, config, image_path):
    return Panel(image_path, config['angle'], config['position'], config['width'], config['height'])

