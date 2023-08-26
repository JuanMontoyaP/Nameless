"""
This section handles all item endpoints.
"""

from fastapi import APIRouter

from ..models import item_models

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@router.get("/{item_type}")
async def get_item_type(item_type: item_models.ItemType):
    return {"item_type": item_type}


@router.post("/")
async def create_item(item: item_models.Item):
    return item
