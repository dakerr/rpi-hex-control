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
    pixel_order=neopixel.GRBW
  )
  rainbox_step_num = 0

  @classmethod
  def fill_hex(cls, index: int, color: Color) -> None:
    color_tile = np.array([color.r, color.g, color.b, color.w], dtype=np.int8)
    hex_leds = np.tile(color_tile, (48, 1))
    for ndx, led in enumerate(hex_leds):
      cls.pixels[ndx + (48 * index)] = [color.r, color.g, color.b, color.w]
      # logger.debug(f"Fill hex {ndx + (48 * index)} {led}")

  @classmethod
  def fill(cls, color: Color) -> None:
    cls.pixels.brightness = color.brightness
    cls.pixels.fill((color.r, color.g, color.b, color.w))
