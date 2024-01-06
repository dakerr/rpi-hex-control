import threading
from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.core.config import Settings
from app.core.hex import get_hex
from app.core.settings import get_settings
from app.services.hex_lights.mode import Mode, ModeEnum


def create_start_app_handler(
  app: FastAPI, settings: Settings = get_settings()
) -> Callable:
  async def start_app() -> None:
    # get_hex().set_mode(Mode(ModeEnum.default))
    threading.Thread(target=get_hex().run, daemon=True).start()

  return start_app

def create_stop_app_handler(app: FastAPI) -> Callable:
  @logger.catch
  async def stop_app() -> None:
    pass

  return stop_app

