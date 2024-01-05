from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.services.hex_lights.color import Color
from app.services.hex_lights.state import State
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

# test
@router.get(
  "/stop",
  response_model=Color,
  summary="Set the state to STOP",
  response_description="The current state",
)
def stop(hex: Hex = Depends(get_hex)) -> Color:
  hex.set_state(State.STOPPED)
  return hex.color

@router.post(
  "/hex/{hex_id}",
  summary="Set a color to the target hexagon",
)
def set_hex_color(hex_id: int, color: Color = Body(...), hex: Hex = Depends(get_hex)) -> None:
  hex.set_hex(hex_id, color)

@router.post(
  "/fill",
  summary="Set a color to all hexagons",
)
def set_color(color: Color = Body(...), hex: Hex = Depends(get_hex)) -> None:
  hex.set_fill(color)