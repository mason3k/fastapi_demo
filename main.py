from fastapi import FastAPI, status, HTTPException
from .model import HotSauce
from .db import MockDb

DB = MockDb()

app = FastAPI()


@app.post("/sauces/", status_code=status.HTTP_201_CREATED)
async def create_item(sauce: HotSauce) -> HotSauce:
    if sauce.id in DB.items_by_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sauce with id {sauce.id} already exists",
        )
    DB.add(sauce)
    return sauce


@app.get("/sauces/")
async def read_items() -> list[HotSauce]:
    return DB.items


@app.get("/sauces/{sauce_id}/")
async def read_item(sauce_id: int):
    if sauce_id not in DB.items_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sauce with id {sauce_id} does not exist",
        )
    return DB.items_by_id[sauce_id]


@app.put("/sauces/{sauce_id}/")
async def update_item(sauce_id, sauce) -> HotSauce:
    ...


@app.delete("/sauces/{sauce_id}")
async def delete_item(sauce_id):
    ...
