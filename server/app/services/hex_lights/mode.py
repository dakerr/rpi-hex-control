from enum import Enum
from pydantic import BaseModel, Extra, Field

class ModeEnum(str, Enum):
  default = "default"
  rainbow = "rainbow"

class Mode(BaseModel):
  mode: ModeEnum = Field(ModeEnum.default, title="Mode")

  class Config:
    frozen = True
    validate_all = True
    extra = Extra.forbid

  def __str__(self) -> str:
    return f"({self.mode.value})"  