from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, Set
from uuid import UUID

class CreateShipmentRequest(BaseModel):
    recipient: str
    address: str
    message: Optional[str] = None
    due: date
    shipped: Optional[date] = None
    tags: Optional[Set[str]] = set()


class UpdateShipmentRequest(BaseModel):
    recipient: Optional[str] = None
    address: Optional[str] = None
    message: Optional[str] = None
    due: Optional[date] = None
    shipped: Optional[date] = None
    tags: Optional[Set[str]] = None


class CreateItemRequest(BaseModel):
    data: dict
    tags: Optional[Set[str]] = set()


class UpdateItemRequest(BaseModel):
    data: Optional[dict] = None
    tags: Optional[Set[str]] = None