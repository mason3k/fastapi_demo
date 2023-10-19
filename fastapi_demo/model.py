from decimal import Decimal

from pydantic import BaseModel, ValidationInfo, field_validator
from pydantic.types import NonNegativeInt, PositiveFloat


class HotSauce(BaseModel):
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
        if v is None or isinstance(v, list):
            return v
        if isinstance(v, str):
            return [item.strip() for item in v.split(",")]
        else:
            raise ValueError(f"{info.field_name} must be a comma-delimited list")


class HotSauceUpdate(HotSauce):
    """A model with no required fields besides id for sending updates"""

    name: str | None = None
    brand: str | None = None
