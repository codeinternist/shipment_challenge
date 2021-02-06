from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, Set
from uuid import UUID

class Item(BaseModel):
    id: UUID
    shipment_id: UUID
    data: dict
    tags: Set[str] = set()
    created: datetime = datetime.now()
    updated: Optional[datetime] = None
    deleted: Optional[datetime] = None


class Shipment(BaseModel):
    id: UUID
    recipient: str
    address: str
    message: Optional[str] = None
    due: date
    shipped: Optional[date] = None
    tags: Set[str] = set()
    created: datetime = datetime.now()
    updated: Optional[datetime] = None
    deleted: Optional[datetime] = None