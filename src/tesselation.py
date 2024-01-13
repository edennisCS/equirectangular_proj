from src.panel import Panel

class Tesselation:
  def __init__(self):
      for config in self.panel_configuration:
        self.panels = map(self.createPanel, self.panel_configuration)

  def createPanel(_self, config):
    return Panel(config['angle'], config['position'], config['width'], config['height'])

