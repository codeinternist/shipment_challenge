import json
from asyncpg import Record
from fastapi import HTTPException

from models.domain import Item, Shipment

def toShipment(rec: Record) -> Shipment:
    props = dict(rec)

    for prop in {"id","recipient","address","message","due","shipped","tags","created","updated","deleted"}:
        if not prop in props:
            raise HTTPException(status_code=500, detail=f"failed to unmarshal database row: no field '{prop}'")
    
    return Shipment(
        id=props["id"],
        recipient=props["recipient"],
        address=props["address"],
        message=props["message"],
        due=props["due"],
        shipped=props["shipped"],
        tags=props["tags"],
        created=props["created"],
        updated=props["updated"],
        deleted=props["deleted"]
    )


def toItem(rec: Record) -> Item:
    props = dict(rec)

    for prop in {"id","shipment_id","data","tags","created","updated","deleted"}:
        if not prop in props:
            raise HTTPException(status_code=500, detail=f"failed to unmarshal database row: no field '{prop}'")
    
    data = json.loads(props["data"])

    return Item(
        id=props["id"],
        shipment_id=props["shipment_id"],
        data=data,
        tags=props["tags"],
        created=props["created"],
        updated=props["updated"],
        deleted=props["deleted"]
    )