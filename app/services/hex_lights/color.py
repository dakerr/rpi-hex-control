from pydantic import BaseModel, Extra, Field

class Color(BaseModel):
  r: int = Field(0, ge=0, le=255, title="Red")
  g: int = Field(0, ge=0, le=255, title="Green")
  b: int = Field(0, ge=0, le=255, title="Blue")
  w: int = Field(0, ge=0, le=255, title="White")
  brightness: float = Field(0, ge=0, le=1)

  class Config:
    frozen = True
    validate_all = True
    extra = Extra.forbid

  @property
  def hex(self) -> str:
    return "#{:02x}{:02x}{:02x}{:02x}".format(self.r, self.g, self.b, self.w)

  def __str__(self) -> str:
    return f"({self.r}, {self.g}, {self.b}, {self.w}, {self.brightness})"
