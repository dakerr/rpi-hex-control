import numpy as np
from loguru import logger

from app.services.hex_lights.color import Color
from app.core.settings import get_settings
from app.api.routes.api import find_items_by_tags
from app.api.models.polyhex import PolyhexCollection


class Board:
  rainbow_step_num = 0
  cycle_step_num = 0
  cycle_interpolation_step_num = 0
  hexagon_indices = [0,1,2,3,4,5,6]

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
  def rainbow_hex_step(cls) -> None:
    for hex_index in cls.hexagon_indices:
      pixel_index = (hex_index * 256 // len(cls.hexagon_indices)) + cls.rainbow_step_num
      hex_color = cls._wheel(pixel_index & 255)
      cls.fill_hex(hex_index, hex_color)
      logger.debug(f"Fill hex: {hex_index} color:{hex_color}")
    cls.hexagon_indices = np.roll(cls.hexagon_indices, 1)
    cls.rainbow_step_num += 1
    if cls.rainbow_step_num == 255:
      cls.rainbow_step_num = 0

  @classmethod
  def cycle_hex_step(cls) -> None:
    #todo: set/get the tags
    tags: list = ["blue","green"]
    
    # up to 10 "polyhexes" consisting of 7 colors - one color per hex
    polyhexes: PolyhexCollection = find_items_by_tags(tags)

    for polyhex in polyhexes:
      for ndx, color in enumerate(polyhex.hexes):

        # get the interpolated set 

        # set the hex
        logger.debug(f"fill hex: {ndx} color: {color}")
        # wait a bit...

  @staticmethod
  def interpolate_color(start_color, end_color, steps):
    """
    Interpolate between two RGBW colors
    """
    start_color = start_color.astype(np.float32)
    end_color = end_color.astype(np.float32)

    #create an array of interpolated colors
    interpolated_colors = [start_color + (i / steps) * (end_color - start_color) for i in range(steps)]

    #round the values to integers
    interpolated_colors = [np.round(color).astype(np.int8) for color in interpolated_colors]

    return interpolated_colors

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