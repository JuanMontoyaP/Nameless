"""
Here you will find the models for items.
"""
from enum import Enum

from pydantic import BaseModel


class ItemType(str, Enum):
    """
    This class represents the type of an item.
    """
    BOOK = "book"
    FOOD = "food"
    MEDICAL = "medical"
    OTHER = "other"


class Item(BaseModel):
    """
    This class represents an item.
    """
    name: str
    description: str
    type: ItemType
