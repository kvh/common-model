from pydantic import BaseModel


class PydanticBase(BaseModel):
    class Config:
        extra = "forbid"


class FrozenPydanticBase(PydanticBase):
    class Config:
        frozen = True
