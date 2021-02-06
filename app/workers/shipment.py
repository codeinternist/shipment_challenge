import logging as log
from asyncpg import Connection
from datetime import date, datetime
from fastapi import HTTPException
from typing import List
from uuid import UUID, uuid4

from models.domain import Shipment
from models.request import CreateShipmentRequest, UpdateShipmentRequest
from utils.converters import toShipment

async def list_shipments(db: Connection) -> List[UUID]:
    log.info("worker: list_shipments")
    
    sql = "select id from shipments;"

    rows = await db.fetch(sql)

    out = []
    for row in rows:
        data = dict(row)
        if not "id" in row:
            raise HTTPException(status_code=500, detail="failed to unmarshal database row: no field 'id'")
        out.append(row["id"])

    return out

async def get_shipment(shipment_id: UUID, db: Connection) -> Shipment:
    log.debug("worker: get_shipment")

    sql = "select * from shipments WHERE id = $1;"

    row = await db.fetchrow(sql, shipment_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"no shipment found for id '{shipment_id}'")

    return toShipment(row)

async def create_shipment(req: CreateShipmentRequest, db: Connection) -> Shipment:
    log.debug("worker: create_shipment")

    shipment = Shipment(
        id=uuid4(),
        recipient=req.recipient,
        address=req.address,
        message=req.message,
        due=req.due,
        shipped=req.shipped,
        tags=req.tags,
        created=datetime.now()
    )

    sql = "insert into shipments (id, recipient, address, message, due, shipped, tags, created) values ($1, $2, $3, $4, $5, $6, $7, $8);"

    res = await db.execute(
        sql,
        shipment.id,
        shipment.recipient,
        shipment.address,
        shipment.message,
        shipment.due,
        shipment.shipped,
        shipment.tags,
        shipment.created
    )
    if res.endswith("0"):
        raise HTTPException(status_code=500, detail=f"error inserting record; response was {res}")

    return shipment

async def update_shipment(shipment_id: UUID, req: UpdateShipmentRequest, db: Connection):
    log.debug("worker: update_shipment")

    shipment = await get_shipment(shipment_id, db)

    sql = "update shipments set recipient = $2, address = $3, message = $4, due = $5, shipped = $6, tags = $7, updated = $8 where id = $1;"
    if req.recipient:
        shipment.recipient = req.recipient
    if req.address:
        shipment.address = req.address
    if req.message:
        shipment.message = req.message
    if req.due:
        shipment.due = req.due
    if req.shipped:
        shipment.shipped = req.shipped
    if req.tags:
        shipment.tags = req.tags

    shipment.updated = datetime.now()

    res = await db.execute(
        sql,
        shipment.id,
        shipment.recipient,
        shipment.address,
        shipment.message,
        shipment.due,
        shipment.shipped,
        shipment.tags,
        shipment.updated
    )
    if res.endswith("0"):
        raise HTTPException(status_code=500, detail=f"error updating record; response was {res}")

    return

async def delete_shipment(shipment_id: UUID, db: Connection):
    log.debug("worker: delete_shipment")

    sql = "delete from shipments where id = $1;"

    res = await db.execute(sql, shipment_id)
    if res.endswith("0"):
        raise HTTPException(status_code=500, detail=f"error deleting record; response was {res}")

    return