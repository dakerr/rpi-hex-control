import numpy as np
from loguru import logger

from app.services.hex_lights.color import Color
from app.core.settings import get_settings
class Board:
  rainbow_step_num = 0
  hexagons = 7

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
  def rainbow_hex_step(cls)-> None:
    for i in range(cls.hexagons):
      pixel_index = (i * 256 // cls.hexagons) + cls.rainbow_step_num
      hex_color = cls._wheel(pixel_index & 255)
      cls.fill_hex(i, hex_color)
      logger.debug(f"Fill hex: {i} color:{hex_color}")
    cls.rainbow_step_num += 1
    if cls.rainbow_step_num == 255:
      cls.rainbow_step_num = 0

  @staticmethod
  def _wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    w = 0
    brightness = 0.3
    
    if pos < 0 or pos > 255:
      r = g = b = 0
    elif pos < 85:
      r = int(pos * 3)
      g = int(255 - pos * 3)
      b = 0
    elif pos < 170:
      pos -= 85
      r = int(255 - pos * 3)
      g = 0
      b = int(pos * 3)
    else:
      pos -= 170
      r = 0
      g = int(pos * 3)
      b = int(255 - pos * 3)
    
    return Color(
      r=r,
      g=g,
      b=b,
      w=w,
      brightness=brightness
    )