from functools import lru_cache

from app.services.hex_lights.hex import Hex


@lru_cache()
def get_hex() -> Hex:
  return Hex()