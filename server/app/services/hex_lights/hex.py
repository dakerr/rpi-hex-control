import time

from app.core.config import Settings
from app.core.settings import get_settings
from app.services.hex_lights.state import State, StateEnum
from app.services.hex_lights.color import Color
from app.services.hex_lights.mode import Mode, ModeEnum
from app.api.routes.api import find_items_by_tags
from app.api.models.polyhex import PolyhexCollection


if get_settings().environment == "prod":
  import app.services.hex_lights.board as board
else:
  import app.services.hex_lights.fake_board as board


class Hex:
  _board: board.Board
  _state: State
  _color: Color
  _mode: Mode
  _tags: list = ["blue", "green"]

  def __init__(self):
    self._board = board.Board()
    self._state = State(state=StateEnum.running)
    self._mode = Mode(mode=ModeEnum.default)
    self._cycle_colors = find_items_by_tags()
  
  @property
  def color(self):
    return self._color
  
  @property
  def state(self):
    return self._state

  @property
  def mode(self):
    return self._mode

  def set_state(self, state: State):
    self._state = state

  def set_mode(self, mode: Mode):
    self._mode = mode

  def set_hex(self, index: int, color: Color):
    self._board.fill_hex(index, color)

  def set_fill(self, color: Color):
    self._board.fill(color)

  def get_

  def run(self, settings: Settings = get_settings()) -> None:
    while self.state.state == StateEnum.running:
      if self.mode.mode == ModeEnum.rainbow:
        self._board.rainbow_hex_step()
        time.sleep(settings.rainbow_sleep_ms / 1000)
      if self.mode.mode == ModeEnum.cycle:
        self._board.cycle_hex_step()
        time.sleep(settings.cycle_sleep_ms / 1000)
      time.sleep(settings.sleep_ms / 1000)