from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.services.hex_lights.color import Color
from app.services.hex_lights.hex import Hex
from app.core.hex import get_hex

router = APIRouter()


@router.get(
  "/color",
  response_model=Color,
  summary="Get the current color",
  response_description="The current color",
)
def color(hex: Hex = Depends(get_hex)) -> Color:
  return hex.color