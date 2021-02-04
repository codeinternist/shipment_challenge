from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, Set
from uuid import UUID

class Metadata(BaseModel):
    created: datetime
    updated: datetime
    deleted: datetime


class Item(BaseModel):
    id: UUID
    data: dict
    tags: Set[str] = set()
    meta: Metadata


class Shipment(BaseModel):
    id: UUID
    recipient: str
    address: str
    message: Optional[str] = None
    due: date
    shipped: Optional[date] = None
    tags: Set[str] = set()
    meta: Metadata