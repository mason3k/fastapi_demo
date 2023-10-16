from pydantic import BaseModel, field_validator, ValidationInfo
from pydantic.types import PositiveFloat, NonNegativeInt
from decimal import Decimal


class HotSauce(BaseModel):
    id: int
    name: str
    brand: str
    scoville_scale: NonNegativeInt | None = None
    ingredients: list[str] | None = None
    flavor_notes: list[str] | None = None
    bottle_size: PositiveFloat | None = None
    price: Decimal | None = None

    @field_validator("ingredients", "flavor_notes", mode="before")
    @classmethod
    def split_list(cls, v: str, info: ValidationInfo) -> list[str]:
        if v is None:
            return v
        if isinstance(v, str):
            return [item.strip() for item in v.split(",")]
        else:
            raise ValueError(f"{info.field_name} must be a comma-delimited list")
