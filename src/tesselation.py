from src.panel import Panel

class Tesselation:
  def __init__(self, colours):
      for config in self.panel_configuration:
        self.panels = map(self.createPanel, self.panel_configuration, colours)

  def createPanel(_self, config, colour):
    return Panel(colour, config['angle'], config['position'], config['width'], config['height'])

