import logging as log
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID

from models.domain import Item
from models.request import CreateItemRequest, UpdateItemRequest
from services.db import connect
from workers import items as worker

router = APIRouter()

@router.get("/shipments/{shipment_id}/items", response_model=List[UUID], status_code=200)
async def list_shipment_items(shipment_id: UUID, db=Depends(connect)):
    log.debug("endpoint: list_items")
    return await worker.list_shipment_items(shipment_id, db)

@router.get("/shipments/{shipment_id}/items/{item_id}", response_model=Item, status_code=200)
async def get_shipment_item(shipment_id: UUID, item_id: UUID, db=Depends(connect)):
    log.debug("endpoint: get_item")
    return await worker.get_shipment_item(shipment_id, item_id, db)

@router.post("/shipments/{shipment_id}/items", response_model=Item, status_code=201)
async def create_shipment_item(shipment_id: UUID, req: CreateItemRequest, db=Depends(connect)):
    log.debug("endpoint: create_item")
    return await worker.create_shipment_item(shipment_id, req, db)

@router.put("/shipments/{shipment_id}/items/{item_id}", status_code=204)
async def update_shipment_item(shipment_id: UUID, item_id: UUID, req: UpdateItemRequest, db=Depends(connect)):
    log.debug("endpoint: update_item")
    if not (req.data or req.tags):
        raise HTTPException(status_code=400, detail="nothing to update")
    
    return await worker.update_shipment_item(shipment_id, item_id, req, db)

@router.delete("/shipments/{shipment_id}/items/{item_id}", status_code=204)
async def delete_shipment_item(shipment_id: UUID, item_id: UUID, db=Depends(connect)):
    log.debug("endpoint: delete_item")
    return await worker.delete_shipment_item(shipment_id, item_id, db)