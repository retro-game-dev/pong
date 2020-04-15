import pyxel


SCREEN_WIDTH = 255
SCREEN_HEIGHT = 120


class App:
  def __init__(self):
    pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
    pyxel.run(self.update, self.draw)

App()
