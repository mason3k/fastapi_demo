from fastapi import FastAPI, HTTPException, status

from .db import MockDb
from .model import HotSauce

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
    return list(DB.items_by_id.values())


@app.get("/sauces/{sauce_id}")
async def read_item(sauce_id: int) -> HotSauce:
    if not (sauce := DB.items_by_id.get(sauce_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sauce with id {sauce_id} does not exist",
        )
    return sauce


@app.put("/sauces/{sauce_id}")
async def update_item(sauce_id: int, new_sauce: HotSauce) -> HotSauce:
    if not (existing_sauce := DB.items_by_id.get(sauce_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sauce with id {sauce_id} does not exist",
        )
    updated_sauce = existing_sauce.model_copy(update=new_sauce.model_dump(exclude_defaults=True))
    DB.items_by_id[sauce_id] = updated_sauce

    return updated_sauce


@app.delete("/sauces/{sauce_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(sauce_id: int) -> dict:
    if sauce_id not in DB.items_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"sauce with id {sauce_id} does not exist",
        )
    del DB.items_by_id[sauce_id]
    return {}
