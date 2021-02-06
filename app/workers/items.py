import json
import logging as log
from asyncpg import Connection
from datetime import datetime
from fastapi import HTTPException
from typing import List
from uuid import UUID, uuid4

from models.domain import Item
from models.request import CreateItemRequest, UpdateItemRequest
from utils.converters import toItem

async def list_shipment_items(shipment_id: UUID, db: Connection) -> List[UUID]:
    log.info("worker: list_shipment_items")
    
    sql = "select id from items where shipment_id = $1;"

    rows = await db.fetch(sql, shipment_id)

    out = []
    for row in rows:
        data = dict(row)
        if not "id" in row:
            raise HTTPException(status_code=500, detail="failed to unmarshal database row: no field 'id'")
        out.append(row["id"])

    return out

async def get_shipment_item(shipment_id: UUID, item_id: UUID, db: Connection) -> Item:
    log.debug("worker: get_shipment_item")

    sql = "select * from items where id = $1 and shipment_id = $2;"

    row = await db.fetchrow(sql, item_id, shipment_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"no item found for id '{item_id}' on shipment '{shipment_id}'")

    return toItem(row)

async def create_shipment_item(shipment_id: UUID, req: CreateItemRequest, db: Connection) -> Item:
    log.debug("worker: create_shipment_item")

    item = Item(
        id=uuid4(),
        shipment_id=shipment_id,
        data=req.data,
        tags=req.tags,
        created=datetime.now()
    )

    sql = "insert into items (id, shipment_id, data, tags, created) values ($1, $2, $3, $4, $5);"

    res = await db.execute(
        sql,
        item.id,
        item.shipment_id,
        json.dumps(item.data),
        item.tags,
        item.created
    )
    if res.endswith("0"):
        raise HTTPException(status_code=500, detail=f"error inserting record; response was {res}")

    return item

async def update_shipment_item(shipment_id: UUID, item_id: UUID, req: UpdateItemRequest, db: Connection):
    log.debug("worker: update_shipment_item")

    item = await get_shipment_item(shipment_id, item_id, db)

    sql = "update items set data = $3, tags = $4, updated = $5 where id = $1 and shipment_id = $2;"
    if req.data:
        item.data = req.data
    if req.tags:
        item.tags = req.tags

    res = await db.execute(
        sql,
        item.id,
        item.shipment_id,
        json.dumps(item.data),
        item.tags,
        item.updated
    )
    if res.endswith("0"):
        raise HTTPException(status_code=500, detail=f"error updating record; response was {res}")

    return

async def delete_shipment_item(shipment_id: UUID, item_id: UUID, db: Connection):
    log.debug("worker: delete_shipment_item")

    sql = "delete from items where id = $1 and shipment_id = $2;"

    res = await db.execute(sql, item_id, shipment_id)
    if res.endswith("0"):
        raise HTTPException(status_code=500, detail=f"error deleting record; response was {res}")

    return