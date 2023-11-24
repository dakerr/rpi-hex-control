from loguru import logger

from app.services.hex_lights.color import Color

class Board:
  rainbow_step_num = 0

  @classmethod
  def fill(cls, color: Color) -> None:
    logger.debug(f"Fill Board Color: {color}")

  @classmethod
  def rainbow_step_num(cls)-> None:
    cls.rainbow_step_num += 1
    if cls.rainbow_step_num == 255:
      cls.rainbow_step_num = 0
    logger.debug(f"Rainbow Step: {cls.rainbow_step_num}")