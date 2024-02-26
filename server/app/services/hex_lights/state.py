from enum import Enum, IntEnum
from pydantic import BaseModel, Extra, Field

class StateEnum(IntEnum):
  stopped = 1
  running = 2

class State(BaseModel):
  state: StateEnum = Field(StateEnum.running, title="State")
  cycle_inter_step_num = 0
  cycle_step_num = 0

  class Config:
    frozen = True
    validate_default = True
    extra = Extra.forbid

  @property
  def cycle_step_num(self):
    return self.cycle_step_num

  @cycle_step_num.setter
  def cycle_step_num(self, step):
    if (step > 9):
      self.cycle_step_num = 0
    else:
      self.cycle_step_num += step

  def __str__(self) -> str:
    return f"({self.state.value})"
