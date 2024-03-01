# app/api/endpoints/item.py
from fastapi import APIRouter

items_router = APIRouter(
    prefix="/items"
)


@items_router.get(path="/", response_model=dict[str, str])
async def read_items():

    return {"message": "Read items"}
