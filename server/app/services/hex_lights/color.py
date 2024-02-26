import string
import secrets

from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Annotated
from typing import Optional
from pydantic.functional_validators import BeforeValidator
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class Color(BaseModel):
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  r: int = Field(0, ge=0, le=255, title="Red")
  g: int = Field(0, ge=0, le=255, title="Green")
  b: int = Field(0, ge=0, le=255, title="Blue")
  w: int = Field(0, ge=0, le=255, title="White")
  brightness: float = Field(0, ge=0, le=1)

  class Config:
    populate_by_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}
    json_schema_extra = {
      'example': {
        'r': 200,
        'g': 0,
        'b': 0,
        'w': 0,
        'brightness': 0.3
      },
      'title': 'Color',
      'description': 'A model representing a RGBW color with a key',
    }

  @property
  def hex(self) -> str:
    return "#{:02x}{:02x}{:02x}{:02x}".format(self.r, self.g, self.b, self.w)

  def __str__(self) -> str:
    return f"({self.r}, {self.g}, {self.b}, {self.w}, {self.brightness})"

