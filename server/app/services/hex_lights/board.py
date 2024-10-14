import board
import neopixel
import numpy as np

from app.core.settings import get_settings
from app.services.hex_lights.color import Color
from loguru import logger

class Board:
  pixels = neopixel.NeoPixel(
    board.D18, 
    get_settings().led_count, 
    brightness=get_settings().default_brightness, 
    pixel_order=neopixel.GRBW,
    auto_write = False
  )
  rainbow_step_num = 0
  hexagon_indices = [0,1,2,3,4,5,6]

  @classmethod
  def fill_hex_segment(cls, hex_ndx, seg_ndx, color: Color) -> None:
    color_tile = np.array([color.r, color.g, color.b, color.w], dtype=np.int8)
    hex_leds = np.tile(color_tile, (8,1))
    for ndx in enumerate(hex_leds):
      pixel_ndx = (48 * hex_ndx) + seg_ndx
      cls.pixels[ndx + pixel_ndx] = [color.r, color.g, color.b, color.w]
    cls.pixels.show()

  @classmethod
  def fill_hex(cls, index: int, color: Color) -> None:
    color_tile = np.array([color.r, color.g, color.b, color.w], dtype=np.int8)
    hex_leds = np.tile(color_tile, (48, 1))
    for ndx, led in enumerate(hex_leds):
      cls.pixels[ndx + (48 * index)] = [color.r, color.g, color.b, color.w]
      # logger.debug(f"Fill hex {ndx + (48 * index)} {led}")
    cls.pixels.show()


  @classmethod
  def fill(cls, color: Color) -> None:
    cls.pixels.brightness = color.brightness
    cls.pixels.fill((color.r, color.g, color.b, color.w))
    cls.pixels.show()

  @classmethod
  def rainbow_hex_step(cls) -> None:
    for i in cls.hexagon_indices:
      hex_index = (i * 256 // len(cls.hexagon_indices)) + cls.rainbow_step_num
      hex_color = cls._wheel(hex_index & 255)
      cls.fill_hex(i, hex_color)
    cls.hexagon_indices = np.roll(cls.hexagon_indices, 1)
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