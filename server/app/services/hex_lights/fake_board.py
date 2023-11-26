import numpy as np
from loguru import logger

from app.services.hex_lights.color import Color
from app.core.settings import get_settings
class Board:
  rainbow_step_num = 0

  @classmethod
  def fill(cls, color: Color) -> None:
    logger.debug(f"Fill Board Color: {color}")

  @classmethod
  def fill_hex(cls, index: int, color: Color) -> None:
    color_tile = np.array([color.r, color.g, color.b, color.w], dtype=np.int8)
    hex_leds = np.tile(color_tile, (48, 1))
    for ndx, led in enumerate(hex_leds):
      logger.debug(f"Fill hex {ndx + (48 * index)} {led}")


  @classmethod
  def rainbow_step_num(cls)-> None:
    cls.rainbow_step_num += 1
    if cls.rainbow_step_num == 255:
      cls.rainbow_step_num = 0
    logger.debug(f"Rainbow Step: {cls.rainbow_step_num}")