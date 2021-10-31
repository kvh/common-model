from pydantic import BaseModel


class PydanticBase(BaseModel):
    pass
    # class Config:
    #     extra = "forbid"


class FrozenPydanticBase(PydanticBase):
    class Config:
        frozen = True
