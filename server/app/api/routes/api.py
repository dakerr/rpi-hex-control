import os
import motor.motor_asyncio

from fastapi import APIRouter, Body, Depends, HTTPException, status, Query
from starlette.status import HTTP_400_BAD_REQUEST
from typing_extensions import Annotated
from typing import Union, List

from app.api.models.polyhex import Polyhex, PolyhexCollection
from app.services.hex_lights.color import Color
from app.services.hex_lights.state import State
from app.services.hex_lights.mode import Mode
from app.services.hex_lights.hex import Hex
from app.core.hex import get_hex

router = APIRouter()

client = None
db = None

async def create_unique_index(collection, *fields):
  index_fields = [(field, 1) for field in fields]
  return await collection.create_index(index_fields, unique=True)

async def startup_event():
  if "MONGODB_URL" in os.environ:
    global client
    global db
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGODB_URL"))
    db = client.color_store

    index_result = await create_unique_index(db['colors'], 'color_key')
    print(f"Unique index created or already exists: {index_result}")

    print(f"Connected to MongoDB!")

async def shutdown_event():
  if "MONGODB_URL" in os.environ:
    global client
    client.close()

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

@router.post(
  "/color",
  response_description="Add a new color",
  response_model=Color,
  status_code=status.HTTP_201_CREATED,
  response_model_by_alias=False,
)
async def set_color(color: Color = Body(...), hex: Hex = Depends(get_hex)) -> None:
  if "MONGODB_URL" in os.environ:
    color_collection =  db.get_collection("colors")
    new_color = await color_collection.insert_one(
      color.model_dump(by_alias=True, exclude=["id"])
    )
    created_color = await color_collection.find_one(
      {"_id": new_color.inserted_id}
    )
    return created_color

@router.get(
  "/polyhex",
  response_description="List all polyhexes",
  response_model=PolyhexCollection,
  response_model_by_alias=False,
)
async def list_polyhexes(tags: Annotated[Union[List[str], None], Query()] = None):
  polyhexes = find_items_by_tags(tags)
  return PolyhexCollection(polyhexes=polyhexes)

@router.post(
    "/polyhex",
    response_description="Add a set of colors",
    response_model=Polyhex,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False
)
async def add_unit(unit: Polyhex = Body(...)) -> None:
  if "MONGODB_URL" in os.environ:
    polyhex_collection = db.get_collection("polyhex")
    new_unit = await polyhex_collection.insert_one(
      unit.model_dump(by_alias=True, exclude=["id"])
    )
    created_unit = await polyhex_collection.find_one(
      {"_id": new_unit.inserted_id}
    )
    return created_unit

@router.put(
  "/color/{hex_id}",
  summary="Set a color to the target hexagon",
)
def set_hex_color(hex_id: int, color: Color = Body(...), hex: Hex = Depends(get_hex)) -> None:
  hex.set_hex(hex_id, color)

async def find_items_by_tags(tags) -> PolyhexCollection:
  polyhexes: list = []
  polyhex_collection = db.get_collection("polyhex")
  cursor = polyhex_collection.find({"tags": {"$in": tags}})
  for document in await cursor.to_list(length=10):
    polyhexes.append(document)
  
  return polyhexes
