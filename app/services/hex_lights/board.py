import board
import neopixel

from app.core.settings import get_settings
from app.services.hex_lights.color import Color


class Board:
  pixels = neopixel.NeoPixel(
    board.D18, 
    get_settings().led_count, 
    brightness=get_settings().default_brightness, 
    pixel_order=neopixel.GRBW
  )
  rainbox_step_num = 0

  @classmethod
  def fill(cls, color: Color) -> None:
    cls.pixels.brightness = color.brightness
    cls.pixels.fill((color.r, color.g, color.b, color.w))
