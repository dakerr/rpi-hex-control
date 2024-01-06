from enum import Enum, IntEnum
from pydantic import BaseModel, Extra, Field

class StateEnum(IntEnum):
  stopped = 1
  running = 2

class State(BaseModel):
  state: StateEnum = Field(StateEnum.running, title="State")

  class Config:
    frozen = True
    validate_all = True
    extra = Extra.forbid

  def __str__(self) -> str:
    return f"({self.state.value})"
