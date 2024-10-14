from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.services.hex_lights.color import Color
from app.services.hex_lights.state import State
from app.services.hex_lights.mode import Mode
from app.services.hex_lights.hex import Hex
from app.core.hex import get_hex

router = APIRouter()

@router.get(
  "/state",
  response_model=State,
  summary="Get the current state",
  response_description="The current state",
)
def state(hex: Hex = Depends(get_hex)) -> State:
  return hex.state

@router.put(
  "/state",
  summary="Set the state to either STOPPED or RUNNING",
)
def set_state(state: State = Body(...), hex: Hex = Depends(get_hex)) -> None:
  hex.set_state(state)

@router.get(
  "/mode",
  response_model=Mode,
  summary="Get the current mode",
  response_description="The current mode"
)
def mode(hex: Hex = Depends(get_hex)) -> Mode:
  return hex.mode

@router.put(
  "/mode",
  summary="Set the mode to either DEFAULT or RAINBOW"
)
def set_mode(mode: Mode = Body(...), hex: Hex = Depends(get_hex)) -> None:
  hex.set_mode(mode)

@router.put(
  "/color",
  summary="Set a color to all hexagons",
)
def set_all_hex_color(color: Color = Body(...), hex: Hex = Depends(get_hex)) -> None:
  hex.set_fill(color)

@router.put(
  "/color/{hex_id}",
  summary="Set a color to the target hexagon",
)
def set_hex_color(hex_id: int, color: Color = Body(...), hex: Hex = Depends(get_hex)) -> None:
  hex.set_hex(hex_id, color)

@router.put(
  "/color/{hex_id}/{segment_id}",
  summary="Set color to the target segment in the hexagon",
)
def set_hex_segment_color(hex_id: int, segment_id: int, color: Color = Body(...), hex: Hex = Depends(get_hex)) -> None:
  hex.set_hex_segment_color(hex_id, segment_id, color)