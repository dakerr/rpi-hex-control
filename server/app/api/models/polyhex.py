from pydantic import BaseModel, Field, conlist
from pydantic.functional_validators import BeforeValidator

from typing import Optional, Union, List
from typing_extensions import Annotated

from app.services.hex_lights.color import Color

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class Polyhex(BaseModel):
  """
  Container for all hexagons.
  """
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  description: Optional[str] = Field(...)
  tags: list = Field(..., min_length=1)
  hexes: conlist(Color) = Field(..., max_length=7)

  class Config:
    json_schema_extra = {
      "example": {
        "description": "set no.1",
        "tags": ["blue", "green"],
        "hexes" : [
          {"r": 0, "g": 0, "b": 0, "w": 0, "brightness": 0.2 },
          {"r": 0, "g": 0, "b": 0, "w": 0, "brightness": 0.2 },
          {"r": 0, "g": 0, "b": 0, "w": 0, "brightness": 0.2 },
          {"r": 0, "g": 0, "b": 0, "w": 0, "brightness": 0.2 },
          {"r": 0, "g": 0, "b": 0, "w": 0, "brightness": 0.2 },
          {"r": 0, "g": 0, "b": 0, "w": 0, "brightness": 0.2 },
          {"r": 0, "g": 0, "b": 0, "w": 0, "brightness": 0.2 },
        ]
      }
    }

class PolyhexCollection(BaseModel):
  """
  A container holding a list of `Polyhex` instances.
  
  This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
  """
  polyhexes: List[Polyhex]