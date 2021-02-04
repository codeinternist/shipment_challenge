from fastapi import APIRouter, HTTPException
from models import models
from uuid import UUID

router = APIRouter()

@router.get("/{shipment_id}/items")
async def list_shipment_items(shipment_id: UUID):
    return {"list": "shipment_items", "shipment_id": shipment_id}

@router.get("/{shipment_id}/items/{item_id}")
async def get_shipment_item(shipment_id: UUID, item_id: UUID):
    return {"get": "shipment_item", "shipment_id": shipment_id, "item_id": item_id}

@router.post("/{shipment_id}/items")
async def create_shipment_item(shipment_id: UUID, data):
    return {"list": "shipment_items", "shipment_id": shipment_id, "data": data}

@router.put("/{shipment_id}/items/{item_id}")
async def update_shipment_item(shipment_id: UUID, item_id: UUID, data):
    return {"get": "shipment_item", "shipment_id": shipment_id, "item_id": item_id, "data": data}

@router.delete("/{shipment_id}/items/{item_id}")
async def remove_shipment_item(shipment_id: UUID, item_id: UUID):
    return {"get": "shipment_item", "shipment_id": shipment_id, "item_id": item_id}