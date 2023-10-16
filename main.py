from fastapi import FastAPI, status, HTTPException
from pathlib import Path
import csv
from pydantic import BaseModel, field_validator, ValidationInfo
from pydantic.types import PositiveFloat, NonNegativeInt
from decimal import Decimal
from contextlib import suppress
from dataclasses import dataclass, field
app = FastAPI()

class HotSauce(BaseModel):
    id: int
    name: str
    brand: str
    scoville_scale: NonNegativeInt | None = None
    ingredients: list[str] | None = None
    flavor_notes: list[str]| None = None
    bottle_size: PositiveFloat| None = None
    price: Decimal| None = None

    @field_validator('ingredients', 'flavor_notes', mode='before')
    @classmethod
    def split_list(cls, v: str, info: ValidationInfo) -> list[str]:
        if v is None:
            return v
        if isinstance(v, str):
            return [item.strip() for item in v.split(',')]
        else:
            raise ValueError(f'{info.field_name} must be a comma-delimited list')
@dataclass
class MockDb:
    items: list[HotSauce] = field(init=False)
    items_by_id: dict[int, HotSauce] = field(init=False)

    def __post_init__(self):
        self.items = self._load_data()
        self.items_by_id = {entry.id: entry for entry in self.items}

    def _load_data(self) -> list[HotSauce]:
        sauces = []
        with Path('data.csv').open() as f:
            reader = csv.reader(f)
            next(reader, None) # skip header
            for row in reader:
                with suppress(Exception):
                    sauces.append(HotSauce(**dict(zip(HotSauce.model_fields, row))))
        return sauces
    
    def add(self, sauce: HotSauce):
        if self.items_by_id.get(sauce.id):
            raise ValueError(f"Error: id {sauce.id} is already in use")
        self.items.append(sauce)
        self.items_by_id[sauce.id] = sauce

DB = MockDb()
    
@app.post("/sauces/", status_code=status.HTTP_201_CREATED)
async def create_item(sauce: HotSauce) -> HotSauce:
    if sauce.id in DB.items_by_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Sauce with id {sauce.id} already exists")
    DB.add(sauce)
    return sauce

@app.get("/sauces/")
async def read_items() -> list[HotSauce]:
    return DB.items

@app.get("/sauces/{sauce_id}/")
async def read_item(sauce_id: int):
    if sauce_id not in DB.items_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sauce with id {sauce_id} does not exist")
    return DB.items_by_id[sauce_id]

@app.put("/sauces/{sauce_id}/")
async def update_item(sauce_id, sauce) -> HotSauce:
    ...

@app.delete("/sauces/{sauce_id}")
async def delete_item(sauce_id):
    ...
