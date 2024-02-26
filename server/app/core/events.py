import threading
import os

from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.core.config import Settings
from app.core.hex import get_hex
from app.core.settings import get_settings
from app.services.hex_lights.mode import Mode, ModeEnum
from app.api.routes.api import startup_event, shutdown_event

def create_start_app_handler(
  app: FastAPI, settings: Settings = get_settings()
) -> Callable:
  async def start_app() -> None:
    # get_hex().set_mode(Mode(ModeEnum.default))
    await startup_event()
    threading.Thread(target=get_hex().run, daemon=True).start()

  return start_app

def create_stop_app_handler(app: FastAPI) -> Callable:
  @logger.catch
  async def stop_app() -> None:
    await shutdown_event()
    pass

  return stop_app

