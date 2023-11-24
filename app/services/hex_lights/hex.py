import time

from app.core.config import Settings
from app.core.settings import get_settings
from app.services.hex_lights.state import State
from app.services.hex_lights.color import Color

if get_settings().environment == "prod":
  import app.services.hex_lights.board as board
else:
  import app.services.hex_lights.fake_board as board


class Hex:
  _board: board.Board
  _state: State
  _color: Color

  def __init__(self):
    self._board = board.Board()
    self._state = State.RUNNING
    self._color = Color()
  
  @property
  def color(self):
    return self._color
  
  def state(self):
    return self._state

  def run(self, settings: Settings = get_settings()) -> None:
    while self.state() == State.RUNNING:
      self._board.fill(self.color)
      time.sleep(settings.sleep_ms / 1000)