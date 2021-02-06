import logging as log
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import date
from uuid import UUID

from models.domain import Shipment
from models.request import CreateShipmentRequest, UpdateShipmentRequest
from services.db import connect
from workers import shipment as worker

router = APIRouter()

@router.get("/shipments/", response_model=List[UUID], status_code=200)
async def list_shipments(db=Depends(connect)):
    log.debug("endpoint: list_shipments")
    return await worker.list_shipments(db)

@router.get("/shipments/{shipment_id}", response_model=Shipment, status_code=200)
async def get_shipment(shipment_id: UUID, db=Depends(connect)):
    log.debug("endpoint: get_shipment")
    return await worker.get_shipment(shipment_id, db)

@router.post("/shipments/", response_model=Shipment, status_code=201)
async def create_shipment(req: CreateShipmentRequest, db=Depends(connect)):
    log.debug("endpoint: create_shipment")
    if req.due < date.today():
        raise HTTPException(status_code=400, detail="due date has already expired")

    return await worker.create_shipment(req, db)

@router.put("/shipments/{shipment_id}", status_code=204)
async def update_shipment(shipment_id: UUID, req: UpdateShipmentRequest, db=Depends(connect)):
    log.debug("endpoint: update_shipment")
    if not (req.recipient or req.address or req.message or req.due or req.shipped or req.tags):
        raise HTTPException(status_code=400, detail="nothing to update")

    return await worker.update_shipment(shipment_id, req, db)

@router.delete("/shipments/{shipment_id}", status_code=204)
async def delete_shipment(shipment_id: UUID, db=Depends(connect)):
    log.debug("endpoint: delete_shipment")
    return await worker.delete_shipment(shipment_id, db)