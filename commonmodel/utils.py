from pydantic import BaseModel


class PydanticBase(BaseModel):
    class Config:
        extra = "forbid"
        use_enum_values = True
        allow_population_by_field_name = True


class FrozenPydanticBase(PydanticBase):
    class Config:
        frozen = True
